"""
raptors-cnn — Flask Web Application
Adaptado de raptor_australia/gui/app.py para el corredor de Veracruz.

Backend con inferencia del modelo entrenado, catálogo de 23 especies
y módulo de vocabulario en International Sign (IS).

Uso:
    conda activate raptors-pt
    cd codigo/pytorch/app_flask
    python app.py
    # Abrir http://localhost:5000
"""
from __future__ import annotations
import csv
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
                    send_from_directory, make_response, url_for)
from PIL import Image

# Imports del proyecto principal
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parents[2]  # raptors-cnn/
PYTORCH_DIR = BASE_DIR.parent       # codigo/pytorch/
sys.path.insert(0, str(PYTORCH_DIR))
import config
from model import build_model
from data_loader import get_transforms

# Imports locales del Flask app
from .species_data import SPECIES_DETAILS
from .i18n import (load_translations, t, get_locale,
                    get_languages, COOKIE_NAME, LANGUAGES)

# ─── Configuración ────────────────────────────────────
MODEL_PATH   = config.CHECKPOINT_DIR / "best_stage2.pt"
UPLOAD_DIR   = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
OBSERVATIONS_CSV = PROJECT_ROOT / "datos" / "observations" / "observations.csv"
FEEDBACK_CSV     = PROJECT_ROOT / "datos" / "feedback" / "feedback_log.csv"

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB

# Cargar traducciones e inyectar helpers a Jinja
load_translations()
app.jinja_env.globals.update(
    t=t, get_locale=get_locale, get_languages=get_languages, LANGUAGES=LANGUAGES,
)

# ─── Carga del modelo ─────────────────────────────────
device = config.DEVICE
print(f"[init] Device: {device}")

raptor_model = None
inference_tf = None


def load_model():
    global raptor_model, inference_tf
    if not MODEL_PATH.exists():
        print(f"[warn] No existe el modelo en {MODEL_PATH}. "
              f"Entrena con `python train.py --smoke-test` antes.")
        return False
    raptor_model = build_model("resnet50").to(device)
    raptor_model._arch_name = "resnet50"
    state = torch.load(MODEL_PATH, map_location=device)
    raptor_model.load_state_dict(state)
    raptor_model.eval()
    _, inference_tf = get_transforms()
    print(f"[init] Modelo cargado de {MODEL_PATH}")
    return True


_MODEL_LOADED = load_model()


# ─── Helpers ──────────────────────────────────────────
def predict_pil(pil_image: Image.Image, top_k: int = 3) -> dict:
    """Predice especie con top-k y devuelve dict listo para template."""
    if not _MODEL_LOADED:
        return {"error": "Modelo no cargado. Entrena primero con train.py --smoke-test."}

    x = inference_tf(pil_image.convert("RGB")).unsqueeze(0).to(device)
    with torch.no_grad():
        logits = raptor_model(x)
        probs = F.softmax(logits, dim=1).cpu().numpy()[0]

    top_idx = probs.argsort()[::-1][:top_k]
    top_results = []
    for i, idx in enumerate(top_idx):
        sci = config.SPECIES[idx]
        details = SPECIES_DETAILS.get(sci, {})
        top_results.append({
            "rank": i + 1,
            "scientific_name": sci.replace("_", " "),
            "scientific_underscored": sci,
            "code": config.SPECIES_CODE[idx],
            "common_en": config.SPECIES_COMMON[idx],
            "common_es": config.SPECIES_COMMON_ES[idx],
            "confidence_pct": round(float(probs[idx]) * 100, 1),
            **{k: details.get(k, "—") for k in
                ["iucn_status", "habitat", "length_cm", "wingspan_cm",
                 "diagnostic", "best_months", "did_you_know",
                 "distribution", "diet", "behavior", "migration"]},
        })

    return {
        "ok": True,
        "best": top_results[0],
        "top_k": top_results,
        "low_confidence": top_results[0]["confidence_pct"] < 50.0,
    }


# ─── Rutas ────────────────────────────────────────────
@app.route("/set_lang/<code>")
def set_lang(code: str):
    """Cambia el idioma vía cookie de 1 año."""
    target = request.args.get("next") or request.referrer or "/"
    resp = make_response(redirect(target))
    if code in LANGUAGES:
        resp.set_cookie(COOKIE_NAME, code, max_age=60 * 60 * 24 * 365, samesite="Lax")
    return resp


@app.route("/")
def index():
    """Página principal — hero con drag-drop y upload."""
    return render_template("index.html",
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

    # Guardar temporalmente
    img_id = str(uuid.uuid4())[:8]
    ext = Path(file.filename).suffix.lower() or ".jpg"
    upload_path = UPLOAD_DIR / f"{img_id}{ext}"
    file.save(upload_path)

    try:
        pil = Image.open(upload_path)
        result = predict_pil(pil, top_k=3)
        if "error" in result:
            return jsonify(result), 500
        result["upload_id"] = img_id
        result["upload_filename"] = f"{img_id}{ext}"
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/uploads/<path:filename>")
def serve_upload(filename: str):
    """Sirve las imágenes recién subidas para mostrarlas en la UI."""
    return send_from_directory(UPLOAD_DIR, filename)


@app.route("/species")
def species_page():
    """Catálogo: grid de las 23 especies."""
    cards = []
    for sci in config.SPECIES:
        details = SPECIES_DETAILS.get(sci, {})
        cards.append({
            "scientific_name": sci.replace("_", " "),
            "scientific_underscored": sci,
            "code": config.SPECIES_CODE[config.SPECIES.index(sci)],
            "common_en": config.SPECIES_COMMON[config.SPECIES.index(sci)],
            "common_es": config.SPECIES_COMMON_ES[config.SPECIES.index(sci)],
            **details,
        })
    return render_template("species.html", species=cards)


@app.route("/data")
def data_page():
    """Dashboard de observaciones + corrections + descargas."""
    n_obs = 0
    species_seen = set()
    if OBSERVATIONS_CSV.exists():
        with open(OBSERVATIONS_CSV, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                n_obs += 1
                species_seen.add(row.get("species_scientific", ""))

    n_feedback = 0
    if FEEDBACK_CSV.exists():
        with open(FEEDBACK_CSV, "r", encoding="utf-8") as f:
            n_feedback = sum(1 for _ in csv.DictReader(f))

    return render_template("data.html",
                           total_observations=n_obs,
                           species_recorded=len(species_seen),
                           total_corrections=n_feedback)


@app.route("/feedback", methods=["POST"])
def feedback():
    """Recibe correcciones del usuario (active learning)."""
    data = request.get_json(force=True)
    # Esquema mínimo: { upload_id, decision: 'correct'|'incorrect', true_code?, notes? }
    FEEDBACK_CSV.parent.mkdir(parents=True, exist_ok=True)
    write_header = not FEEDBACK_CSV.exists()
    with open(FEEDBACK_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(["timestamp_utc", "upload_id", "decision",
                        "predicted_code", "predicted_species",
                        "true_code", "true_species", "notes"])
        w.writerow([
            datetime.utcnow().isoformat(timespec="seconds"),
            data.get("upload_id", ""),
            data.get("decision", ""),
            data.get("predicted_code", ""),
            data.get("predicted_species", ""),
            data.get("true_code", ""),
            data.get("true_species", ""),
            data.get("notes", ""),
        ])
    return jsonify({"ok": True})


@app.route("/save_observation", methods=["POST"])
def save_observation():
    """Guarda una observación científica con coordenadas opcionales."""
    data = request.get_json(force=True)
    OBSERVATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    write_header = not OBSERVATIONS_CSV.exists()
    obs_id = str(uuid.uuid4())[:8]
    with open(OBSERVATIONS_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(["observation_id", "timestamp_utc",
                        "species_scientific", "species_common", "species_code",
                        "confidence", "image_filename",
                        "latitude", "longitude", "location_name",
                        "country", "stateProvince", "notes"])
        w.writerow([
            obs_id, datetime.utcnow().isoformat(timespec="seconds"),
            data.get("species_scientific", ""),
            data.get("species_common", ""),
            data.get("species_code", ""),
            data.get("confidence", 0),
            data.get("image_filename", ""),
            data.get("latitude", ""),
            data.get("longitude", ""),
            data.get("location_name", ""),
            "MX", "Veracruz",
            data.get("notes", ""),
        ])
    return jsonify({"ok": True, "observation_id": obs_id})


@app.route("/export/darwin_core")
def export_darwin_core():
    """Descarga observaciones en formato Darwin Core (compatible iNat/GBIF)."""
    if not OBSERVATIONS_CSV.exists():
        return jsonify({"error": "Sin observaciones"}), 404
    return send_from_directory(OBSERVATIONS_CSV.parent, OBSERVATIONS_CSV.name,
                                as_attachment=True,
                                download_name="raptors-cnn-darwin-core.csv")


# ─── Main ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
