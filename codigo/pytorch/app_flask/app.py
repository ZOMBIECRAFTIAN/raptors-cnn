"""
raptors-cnn — Flask Web Application
====================================

Sistema de Identificación de Aves Rapaces por Silueta y Comportamiento
de Vuelo Utilizando IA y Diseño de Lenguaje de Señas.

Backend Flask con inferencia del modelo entrenado, catálogo de 53 rapaces
diurnas de México y módulo de vocabulario en International Sign (IS).

Adaptado fielmente de raptor_australia/gui/app.py (alcance: 8 rapaces
australianas + AUSLAN) para el alcance nacional mexicano (53 especies + IS).

Rutas principales:
    GET  /                      Home + identificación (drag-drop imagen/video)
    POST /identify              Predicción CNN sobre imagen
    POST /identify_video        Multi-especie video (Faster R-CNN + CNN)
    POST /save_observation      Guardar observación confirmada (CSV)
    POST /feedback              Correcciones del usuario (active learning)
    GET  /feedback_stats        JSON contador de correcciones
    GET  /species               Catálogo de 53 especies con métricas
    GET  /data                  Dashboard observaciones + export
    GET  /set_lang/<code>       Cambiar idioma (cookie 1 año)
    GET  /export/observations.csv         CSV interno
    GET  /export/observations_dwc.csv     Darwin Core (GBIF/iNaturalist)
    GET  /export/feedback.csv             Log de correcciones (auditoría)
    GET  /is_videos/<file>      Sirve videos/SVG de señas IS
    GET  /behavior_videos/<file> Sirve videos de comportamiento

Uso:
    conda activate raptors-pt
    cd codigo/pytorch/app_flask
    python app.py
    # Abrir http://localhost:5000
"""
from __future__ import annotations
import csv
import io
import json
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from flask import (Flask, render_template, request, jsonify, redirect,
                    send_from_directory, make_response, Response)
from PIL import Image

# Imports del proyecto principal
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parents[2]  # raptors-cnn/
PYTORCH_DIR = BASE_DIR.parent       # codigo/pytorch/
# Permite tanto `python app.py` (script) como `python -m app_flask.app` (módulo)
sys.path.insert(0, str(PYTORCH_DIR))
sys.path.insert(0, str(BASE_DIR))
import config  # noqa: E402
from model import build_model  # noqa: E402
from data_loader import get_transforms  # noqa: E402

# Imports locales del Flask app (imports absolutos que funcionan en ambos modos)
from species_data import SPECIES_DETAILS    # noqa: E402
from species_info import SPECIES_INFO       # noqa: E402
from i18n import (load_translations, t, get_locale,                    # noqa: E402
                  get_languages, COOKIE_NAME, LANGUAGES)

# ─── Configuración ────────────────────────────────────
MODEL_PATH       = config.CHECKPOINT_DIR / "best_stage2.pt"
UPLOAD_DIR       = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
OBSERVATIONS_CSV = PROJECT_ROOT / "datos" / "observations" / "observations.csv"
FEEDBACK_CSV     = PROJECT_ROOT / "datos" / "feedback" / "feedback_log.csv"
OOD_LOG_CSV      = PROJECT_ROOT / "datos" / "feedback" / "out_of_domain_log.csv"
METRICS_JSON     = PROJECT_ROOT / "codigo" / "pytorch" / "outputs" / "reporte_final.json"
RAW_DIR          = config.RAW_DIR

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024  # 32 MB (videos)

# Carga traducciones e inyecta helpers a Jinja
load_translations()
app.jinja_env.globals.update(
    t=t, get_locale=get_locale, get_languages=get_languages, LANGUAGES=LANGUAGES,
)

# ─── Carga del modelo ─────────────────────────────────
device = config.DEVICE
print(f"[init] Device: {device}")

raptor_model = None
inference_tf = None


def _detect_arch_from_state(state) -> str:
    """Adivina la arquitectura inspeccionando las keys del state_dict."""
    keys = list(state.keys())
    sample = " ".join(keys[:20])
    if "layer_scale" in sample or any(".block." in k for k in keys[:50]):
        return "convnext_tiny"
    if any(k == "conv1.weight" for k in keys) and any(k.startswith("layer1.") for k in keys):
        return "resnet50"
    if any("se_layer" in k or "_se." in k for k in keys):
        return "mobilenet_v3_large"
    if any(k.startswith("features.") and "stem" not in k for k in keys[:5]):
        return "efficientnet_b3"
    raise ValueError(
        "Cannot detect architecture from checkpoint. First keys: "
        + ", ".join(keys[:8])
    )


def load_model() -> bool:
    """Carga el modelo entrenado una sola vez al iniciar la app.

    Autodetecta la arquitectura desde el state_dict; si falla esa detección,
    intenta las 4 arquitecturas conocidas hasta que alguna cargue sin errores
    de keys. La app arranca en modo demo si el checkpoint no existe o si
    ninguna arch acepta los pesos.
    """
    global raptor_model, inference_tf
    if not MODEL_PATH.exists():
        print(f"[warn] No existe el modelo en {MODEL_PATH}. "
              f"La app arranca en modo demo - entrena con "
              f"`python train.py --smoke-test` para activar predicciones.")
        return False

    state = torch.load(MODEL_PATH, map_location=device)

    candidates = []
    try:
        candidates.append(_detect_arch_from_state(state))
    except ValueError as e:
        print(f"[warn] Auto-detect fallo: {e}")
    # Fallback: probar todas las arquitecturas conocidas
    for arch in ("resnet50", "convnext_tiny", "efficientnet_b3",
                 "mobilenet_v3_large"):
        if arch not in candidates:
            candidates.append(arch)

    last_err = None
    for arch in candidates:
        try:
            model = build_model(arch).to(device)
            model.load_state_dict(state)
            model.eval()
            raptor_model = model
            raptor_model._arch_name = arch
            _, inference_tf = get_transforms(config.input_size_for_arch(arch))
            print(f"[init] Modelo cargado de {MODEL_PATH} como {arch}")
            return True
        except (RuntimeError, KeyError) as e:
            last_err = e
            continue

    print(f"[error] Ninguna arquitectura aceptó el checkpoint.")
    print(f"        Ultimo error: {str(last_err)[:200]}...")
    print(f"        La app arranca en modo demo. Re-entrena para usar predicciones:")
    print(f"        cd codigo/pytorch && python train.py --arch resnet50 --smoke-test")
    return False


_MODEL_LOADED = load_model()


# ─── Helpers ──────────────────────────────────────────
def _localized_species_info() -> dict[str, dict]:
    """
    Devuelve SPECIES_INFO localizado en el idioma actual.
    Aplica tres niveles de traduccion cuando lang='en':
      1. common_name -> common_name_en
      2. iucn_status / epbc_status -> mapeo limpio EN (sin parentesis ES)
      3. campos textuales largos (habitat, diagnostic, ...) ->
         species_data_en.SPECIES_DETAILS_EN si existe, sino fallback ES.
    """
    from species_info import (
        localized_field, _clean_iucn_status, _translate_short
    )
    lang = get_locale()
    out: dict[str, dict] = {}
    for key, base in SPECIES_INFO.items():
        merged = dict(base)
        if lang == "en":
            merged["common_name"] = base["common_name_en"]
            # IUCN/NOM-059 status: limpia parentesis ES y mapea a EN
            merged["iucn_status"] = _clean_iucn_status(
                base.get("iucn_status", "—"), "en")
            merged["epbc_status"] = _clean_iucn_status(
                base.get("epbc_status", "—"), "en")
            # Habitat se construye desde distribution; intenta version EN
            en_distribution = localized_field(key, "distribution", "en")
            if en_distribution and en_distribution != "—":
                first = en_distribution.split(".")[0]
                merged["habitat"] = first[:90].strip() + (
                    "..." if len(first) > 90 else ""
                )
            else:
                # Fallback: traduce frases cortas comunes en el ES existente
                merged["habitat"] = _translate_short(
                    base.get("habitat", "—"), "en")
            # Diagnostic (campo corto pero importante)
            merged["diagnostic"] = localized_field(
                key, "diagnostic", "en", default=base.get("diagnostic", "—")
            )
        out[key] = merged
    return out


def predict_image(img_path: Path) -> dict:
    """
    Predice especie sobre una imagen.

    Returns:
        dict con especie predicha, confianza y top-3 (todos los campos
        que el template index.html espera).
    """
    if not _MODEL_LOADED:
        return {"error": "Modelo no cargado. Entrena con train.py primero."}

    img = Image.open(img_path).convert("RGB")
    tensor = inference_tf(img).unsqueeze(0).to(device)

    with torch.no_grad():
        logits = raptor_model(tensor)
        probs = F.softmax(logits, dim=1)[0].cpu().numpy()

    top3_idx = np.argsort(probs)[::-1][:3]

    info_loc = _localized_species_info()

    top3 = []
    for idx in top3_idx:
        sci = config.SPECIES[idx]
        nfo = info_loc[sci]
        top3.append({
            "species_key":     sci,
            "common_name":     nfo["common_name"],
            "scientific_name": nfo["scientific_name"],
            "confidence":      round(float(probs[idx]) * 100, 1),
            "color":           nfo["color"],
        })

    best_key  = config.SPECIES[top3_idx[0]]
    best_info = info_loc[best_key]

    return {
        "species_key":     best_key,
        "common_name":     best_info["common_name"],
        "scientific_name": best_info["scientific_name"],
        "confidence":      round(float(probs[top3_idx[0]]) * 100, 1),
        "epbc_status":     best_info["iucn_status"],  # alias para el template
        "habitat":         best_info["habitat"],
        "wingspan_cm":     best_info["wingspan_cm"],
        "length_cm":       best_info["length_cm"],
        "diagnostic":      best_info["diagnostic"],
        "auslan_sign":     best_info["auslan_sign"],
        "auslan_video":    best_info["auslan_video"],
        "color":           best_info["color"],
        "top3":            top3,
    }


# ─── Rutas Flask ──────────────────────────────────────
@app.route("/set_lang/<code>")
def set_lang(code: str):
    """Cambia el idioma via cookie de 1 ano.

    Fix de persistencia: la cookie se establece con path="/" explicito, sin
    domain (para que valga tanto en localhost como en 127.0.0.1), y con
    samesite="Lax" para que sobreviva al redirect. Tambien se valida que el
    target del redirect sea interno para evitar open-redirect.
    """
    raw_target = request.args.get("next") or request.referrer or "/"
    # Solo aceptamos paths internos (que empiecen con "/")
    target = raw_target if raw_target.startswith("/") else "/"

    resp = make_response(redirect(target))
    if code in LANGUAGES:
        resp.set_cookie(
            COOKIE_NAME,
            code,
            max_age=60 * 60 * 24 * 365,  # 1 ano
            path="/",                     # disponible en TODAS las rutas
            samesite="Lax",               # sobrevive al redirect
            secure=False,                 # dev local sin HTTPS
            httponly=False,               # legible por JS si se quiere
        )
        # Y lo dejamos accesible en la request actual por si algun
        # template lo lee inmediatamente
        request.cookies = {**request.cookies, COOKIE_NAME: code}  # type: ignore
    return resp


@app.route("/")
def index():
    """Página principal — UI localizada."""
    return render_template("index.html",
                           species_info=_localized_species_info(),
                           num_species=len(config.SPECIES),
                           model_loaded=_MODEL_LOADED)


@app.route("/identify", methods=["POST"])
def identify():
    """Endpoint AJAX — recibe imagen, devuelve JSON con predicción."""
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    allowed = {"jpg", "jpeg", "png", "tiff", "bmp", "webp"}
    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in allowed:
        return jsonify({"error": f"Formato no soportado: {ext}"}), 400

    filename = f"{uuid.uuid4()}.{ext}"
    img_path = UPLOAD_DIR / filename

    try:
        file.save(str(img_path))
        result = predict_image(img_path)
        if "error" in result:
            return jsonify(result), 500
        result["filename"] = filename
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if img_path.exists():
            try:
                os.remove(img_path)
            except Exception:
                pass


@app.route("/save_observation", methods=["POST"])
def save_observation():
    """Guarda observación confirmada por el usuario en CSV."""
    data = request.get_json(force=True)
    OBSERVATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    file_exists = OBSERVATIONS_CSV.exists()
    with open(OBSERVATIONS_CSV, "a", newline="", encoding="utf-8") as f:
        fieldnames = [
            "timestamp", "species_key", "common_name",
            "scientific_name", "confidence", "latitude",
            "longitude", "notes", "observer_confirmed",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "timestamp":          datetime.now().isoformat(),
            "species_key":        data.get("species_key", ""),
            "common_name":        data.get("common_name", ""),
            "scientific_name":    data.get("scientific_name", ""),
            "confidence":         data.get("confidence", ""),
            "latitude":           data.get("latitude", ""),
            "longitude":          data.get("longitude", ""),
            "notes":              data.get("notes", ""),
            "observer_confirmed": data.get("confirmed", True),
        })
    return jsonify({"status": "saved"})


@app.route("/feedback", methods=["POST"])
def save_feedback():
    """Recibe corrección del usuario (active learning + retraining)."""
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "No data"}), 400

        correct_key = data.get("correct_key", "")
        is_ood = (correct_key == "other_not_listed")

        log_file = OOD_LOG_CSV if is_ood else FEEDBACK_CSV
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_exists = log_file.exists()

        feedback_id = str(uuid.uuid4())[:8]
        with open(log_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "feedback_id", "timestamp",
                "predicted_key", "predicted_name",
                "correct_key", "correct_name", "confidence",
            ])
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                "feedback_id":    feedback_id,
                "timestamp":      datetime.now().isoformat(),
                "predicted_key":  data.get("predicted_key", ""),
                "predicted_name": data.get("predicted_name", ""),
                "correct_key":    correct_key,
                "correct_name":   data.get("correct_name", ""),
                "confidence":     data.get("confidence", ""),
            })
        return jsonify({
            "status": "saved",
            "feedback_id": feedback_id,
            "out_of_domain": is_ood,
            "message": ("Reporte fuera de catálogo guardado." if is_ood
                        else "Corrección guardada exitosamente."),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/feedback_stats")
def feedback_stats():
    """Stats del log de correcciones (para banner UI 'listo para retrain')."""
    retrain_threshold = 50
    if not FEEDBACK_CSV.exists():
        return jsonify({
            "total_corrections": 0,
            "ready_to_retrain":  False,
            "threshold":         retrain_threshold,
        })
    with open(FEEDBACK_CSV, "r", encoding="utf-8") as f:
        total = sum(1 for _ in csv.DictReader(f))
    return jsonify({
        "total_corrections": total,
        "ready_to_retrain":  total >= retrain_threshold,
        "threshold":         retrain_threshold,
    })


def _load_species_metrics() -> dict:
    """Cargar métricas por especie (F1/precision/recall) + train_count."""
    metrics: dict[str, dict] = {}
    if METRICS_JSON.exists():
        try:
            with open(METRICS_JSON, "r", encoding="utf-8") as f:
                report = json.load(f)
            common_to_key = {
                base["common_name_en"]: key
                for key, base in SPECIES_INFO.items()
            }
            for common_name, m in (report.get("por_especie") or {}).items():
                key = common_to_key.get(common_name)
                if key:
                    metrics[key] = {
                        "f1":        m.get("f1"),
                        "precision": m.get("precision"),
                        "recall":    m.get("recall"),
                        "support":   m.get("support"),
                    }
        except Exception as e:
            print(f"[species] no se pudieron cargar métricas: {e}")

    # Conteo de imágenes en datos/processed/train/<species>/
    train_dir = config.PROCESSED_DIR / "train"
    for key in SPECIES_INFO:
        sp_dir = train_dir / key
        count = 0
        if sp_dir.exists():
            count = sum(1 for p in sp_dir.iterdir()
                        if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"})
        metrics.setdefault(key, {})["train_count"] = count

    return metrics


def _behavior_video_status() -> dict[str, dict]:
    """Estado del video de comportamiento por especie."""
    folder = BASE_DIR / "static" / "behavior_videos"
    out: dict[str, dict] = {}
    for key in SPECIES_INFO:
        for ext in ("mp4", "webm", "mov"):
            p = folder / f"{key}.{ext}"
            if p.exists():
                out[key] = {"exists": True, "filename": p.name,
                            "size_mb": round(p.stat().st_size / 1e6, 1)}
                break
        else:
            out[key] = {"exists": False, "filename": f"{key}.mp4", "size_mb": 0}
    return out


def _localized_species_details() -> dict[str, dict]:
    """Devuelve SPECIES_DETAILS con campos largos sustituidos por EN cuando
    el locale es 'en' y existe traduccion en species_data_en.SPECIES_DETAILS_EN.
    Cualquier campo no traducido cae a la version espanola original."""
    from species_info import (
        SPECIES_DETAILS_EN, _clean_iucn_status,
    )
    lang = get_locale()
    if lang != "en":
        return SPECIES_DETAILS
    out: dict[str, dict] = {}
    for key, es_details in SPECIES_DETAILS.items():
        en_details = SPECIES_DETAILS_EN.get(key, {})
        merged = dict(es_details)
        # Campo por campo: si hay version EN no vacia, usala
        for field, en_val in en_details.items():
            if en_val:
                merged[field] = en_val
        # Limpieza extra del iucn_status (quitar parentesis ES)
        if "iucn_status" in merged:
            merged["iucn_status"] = _clean_iucn_status(
                merged["iucn_status"], "en")
        out[key] = merged
    return out


@app.route("/species")
def species_page():
    """Catálogo: grid de las 53 especies con perfiles enriquecidos."""
    info_loc = _localized_species_info()
    return render_template(
        "species.html",
        species_info=info_loc,
        species_metrics=_load_species_metrics(),
        species_details=_localized_species_details(),
        behavior_videos=_behavior_video_status(),
    )


def _load_observations() -> list[dict]:
    if not OBSERVATIONS_CSV.exists():
        return []
    with open(OBSERVATIONS_CSV, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _to_dwc_rows(obs_rows: list[dict]) -> list[dict]:
    """
    Convierte observaciones internas → Darwin Core
    (https://dwc.tdwg.org/terms/). Listo para upload a iNaturalist/GBIF.
    """
    out: list[dict] = []
    for i, r in enumerate(obs_rows):
        ts = r.get("timestamp", "") or ""
        event_date = ts.split("T")[0] if "T" in ts else ts
        confidence = r.get("confidence", "") or ""
        confirmed = (r.get("observer_confirmed", "") or "").lower()
        verification = ("verifiedByExpert"
                        if confirmed in {"true", "1", "yes"}
                        else "unverified")
        identified_by = (
            "raptors-cnn v1.1 (México) — "
            "ResNet-50 transfer learning, 53 clases, "
            "AOS 2024 taxonomy"
        )
        out.append({
            "occurrenceID":       f"raptor-mx-{i+1:06d}",
            "basisOfRecord":      "HumanObservation",
            "eventDate":          event_date,
            "scientificName":     r.get("scientific_name", ""),
            "vernacularName":     r.get("common_name", ""),
            "decimalLatitude":    r.get("latitude", ""),
            "decimalLongitude":   r.get("longitude", ""),
            "geodeticDatum":      "WGS84",
            "country":            "Mexico",
            "countryCode":        "MX",
            "recordedBy":         "raptors-cnn — citizen science",
            "identifiedBy":       identified_by,
            "identificationVerificationStatus": verification,
            "occurrenceRemarks":  r.get("notes", ""),
            "dataGeneralizations":
                f"AI-assisted identification, confidence={confidence}%",
            "dynamicProperties":
                f"{{\"model_confidence\":{confidence},"
                f"\"observer_confirmed\":{confirmed}}}",
        })
    return out


def _csv_response(rows: list[dict], fieldnames: list[str], filename: str) -> Response:
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for r in rows:
        writer.writerow(r)
    return Response(
        buf.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.route("/data")
def data_dashboard():
    """Dashboard de observaciones + descargas (CSV interno, Darwin Core, feedback)."""
    rows = _load_observations()
    by_species: dict[str, int] = {}
    for r in rows:
        key = r.get("species_key") or "unknown"
        by_species[key] = by_species.get(key, 0) + 1

    feedback_count = 0
    if FEEDBACK_CSV.exists():
        with open(FEEDBACK_CSV, "r", encoding="utf-8") as f:
            feedback_count = sum(1 for _ in csv.DictReader(f))

    recent = list(reversed(rows))[:10]
    return render_template(
        "data.html",
        species_info=_localized_species_info(),
        total_observations=len(rows),
        observations_by_species=by_species,
        feedback_count=feedback_count,
        recent_observations=recent,
    )


@app.route("/export/observations.csv")
def export_observations():
    rows = _load_observations()
    fieldnames = [
        "timestamp", "species_key", "common_name",
        "scientific_name", "confidence", "latitude",
        "longitude", "notes", "observer_confirmed",
    ]
    return _csv_response(rows, fieldnames, "raptors_mx_observations.csv")


@app.route("/export/observations_dwc.csv")
def export_observations_dwc():
    rows = _to_dwc_rows(_load_observations())
    fieldnames = [
        "occurrenceID", "basisOfRecord", "eventDate",
        "scientificName", "vernacularName",
        "decimalLatitude", "decimalLongitude", "geodeticDatum",
        "country", "countryCode",
        "recordedBy", "identifiedBy",
        "identificationVerificationStatus",
        "occurrenceRemarks", "dataGeneralizations",
        "dynamicProperties",
    ]
    return _csv_response(rows, fieldnames, "raptors_mx_observations_dwc.csv")


@app.route("/export/feedback.csv")
def export_feedback():
    if not FEEDBACK_CSV.exists():
        return Response("feedback log is empty", status=404)
    with open(FEEDBACK_CSV, "r", encoding="utf-8") as f:
        content = f.read()
    return Response(
        content, mimetype="text/csv",
        headers={"Content-Disposition":
                 'attachment; filename="raptors_mx_feedback_log.csv"'},
    )


# ─── Endpoints de media (señas IS + comportamiento) ─────────────────────
@app.route("/auslan_videos/<filename>")  # mantengo nombre por compatibilidad
@app.route("/is_videos/<filename>")
def is_video(filename):
    """Sirve videos/SVG de señas en International Sign."""
    folder = BASE_DIR / "static" / "is_videos"
    if not (folder / filename).exists():
        folder = BASE_DIR / "static" / "auslan_videos"  # fallback
    return send_from_directory(str(folder), filename)


@app.route("/behavior_videos/<filename>")
def behavior_video(filename):
    """Sirve videos de comportamiento por especie."""
    return send_from_directory(
        str(BASE_DIR / "static" / "behavior_videos"), filename)


# ─── Video analysis (multi-species, multi-bird) ─────────────────────────
_video_detector = None


def _lazy_video_detector():
    """Faster R-CNN detector cargado al primer uso."""
    global _video_detector
    if _video_detector is None:
        from torchvision.models.detection import (
            fasterrcnn_resnet50_fpn,
            FasterRCNN_ResNet50_FPN_Weights,
        )
        weights = FasterRCNN_ResNet50_FPN_Weights.DEFAULT
        m = fasterrcnn_resnet50_fpn(weights=weights, box_score_thresh=0.45)
        m.eval().to(device)
        m._ra_categories = weights.meta["categories"]
        _video_detector = m
    return _video_detector


def _classify_crop(crop_pil) -> dict:
    """Clasifica una sola crop del detector sobre la CNN entrenada."""
    info_loc = _localized_species_info()
    tensor = inference_tf(crop_pil.convert("RGB")).unsqueeze(0).to(device)
    with torch.no_grad():
        probs = F.softmax(raptor_model(tensor), dim=1)[0].cpu().numpy()
    idx = int(np.argmax(probs))
    sp = config.SPECIES[idx]
    nfo = info_loc[sp]
    return {
        "species_key": sp,
        "common_name": nfo["common_name"],
        "scientific":  nfo["scientific_name"],
        "color":       nfo["color"],
        "confidence":  round(float(probs[idx]) * 100, 1),
    }


@app.route("/identify_video", methods=["POST"])
def identify_video():
    """
    Pipeline multi-especie sobre video:
    1. Muestrea frames a ~1 fps con OpenCV.
    2. Faster R-CNN para detectar pájaros.
    3. CNN especifica para cada crop.
    4. Devuelve timeline por frame + resumen por especie.
    """
    if not _MODEL_LOADED:
        return jsonify({"error": "Modelo no cargado"}), 500

    try:
        import cv2
    except Exception:
        return jsonify({"error": "OpenCV (cv2) no instalado. "
                                  "Instala: pip install opencv-python"}), 500

    if "video" not in request.files:
        return jsonify({"error": "No video uploaded"}), 400
    file = request.files["video"]
    if not file.filename:
        return jsonify({"error": "No file selected"}), 400

    allowed_ext = {"mp4", "mov", "webm", "mkv", "avi"}
    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in allowed_ext:
        return jsonify({"error": f"Formato no soportado: {ext}"}), 400

    tmp_path = UPLOAD_DIR / f"{uuid.uuid4()}.{ext}"
    file.save(str(tmp_path))

    try:
        cap = cv2.VideoCapture(str(tmp_path))
        if not cap.isOpened():
            return jsonify({"error": "No se pudo abrir el video"}), 500

        fps      = cap.get(cv2.CAP_PROP_FPS) or 30.0
        n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        duration = n_frames / fps if fps > 0 else 0
        step     = max(1, int(round(fps)))
        max_frames = 60
        sampled  = 0

        from torchvision.transforms.functional import to_tensor
        detector = _lazy_video_detector()
        cats     = detector._ra_categories

        timeline: list[dict] = []
        per_species: dict[str, int] = {}
        info_loc = _localized_species_info()
        frame_idx = 0

        while sampled < max_frames:
            ret, bgr = cap.read()
            if not ret:
                break
            if frame_idx % step != 0:
                frame_idx += 1
                continue

            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            pil = Image.fromarray(rgb)
            W, H = pil.size

            with torch.no_grad():
                out = detector([to_tensor(pil).to(device)])[0]

            birds: list[dict] = []
            for i in range(len(out["labels"])):
                if cats[int(out["labels"][i])] != "bird":
                    continue
                if float(out["scores"][i]) < 0.5:
                    continue
                x0, y0, x1, y1 = [float(v) for v in out["boxes"][i]]
                m = 0.05 * min(W, H)
                cx0 = max(0, int(x0 - m))
                cy0 = max(0, int(y0 - m))
                cx1 = min(W, int(x1 + m))
                cy1 = min(H, int(y1 + m))
                crop = pil.crop((cx0, cy0, cx1, cy1))
                if min(crop.size) < 32:
                    continue
                pred = _classify_crop(crop)
                pred["bbox"] = [cx0, cy0, cx1, cy1]
                pred["bbox_score"] = round(float(out["scores"][i]), 3)
                birds.append(pred)
                per_species[pred["species_key"]] = \
                    per_species.get(pred["species_key"], 0) + 1

            timeline.append({
                "t_seconds":  round(frame_idx / fps, 2),
                "frame_idx":  frame_idx,
                "n_birds":    len(birds),
                "detections": birds,
            })
            sampled += 1
            frame_idx += 1
            for _ in range(step - 1):
                cap.grab()
                frame_idx += 1

        cap.release()

        summary = sorted(
            [{
                "species_key": k,
                "common_name": info_loc[k]["common_name"],
                "scientific":  info_loc[k]["scientific_name"],
                "color":       info_loc[k]["color"],
                "frames_with_species": per_species[k],
            } for k in per_species],
            key=lambda x: -x["frames_with_species"],
        )

        return jsonify({
            "duration_seconds": round(duration, 2),
            "video_fps":        round(fps, 2),
            "frames_sampled":   sampled,
            "timeline":         timeline,
            "summary":          summary,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            tmp_path.unlink()
        except Exception:
            pass


# ─── Main ─────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🦅 raptors-cnn — Identificación de Rapaces de México")
    print(f"   Modelo: {MODEL_PATH.name} ({'cargado' if _MODEL_LOADED else 'NO cargado'})")
    print(f"   Especies: {len(config.SPECIES)}")
    print(f"   Dispositivo: {device}")
    print(f"   URL: http://localhost:5000\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
