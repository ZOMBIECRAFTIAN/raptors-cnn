"""
Sistema de active learning — recibe correcciones del usuario sobre las
predicciones del modelo y las acumula para retraining incremental.

Cuando el usuario sube una imagen y el modelo predice mal, puede señalar:
  - "Es incorrecta" + seleccionar la especie correcta
  - "Es correcta, confirmo"
  - "No es ninguna rapaz" (out-of-distribution)

Estas decisiones se guardan en:
  - datos/feedback/<scientific_name>/<hash>.jpg            (imagen)
  - datos/feedback/feedback_log.csv                        (registro)

Posteriormente, el script `retrain_with_feedback.py` toma estas correcciones
y hace fine-tuning incremental del modelo.
"""
from __future__ import annotations
import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from PIL import Image

# Imports del proyecto
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config

FEEDBACK_DIR = config.DATA_DIR / "feedback"
FEEDBACK_LOG = FEEDBACK_DIR / "feedback_log.csv"

FIELDNAMES = [
    "timestamp_utc", "filename_hash", "image_path", "decision",
    "predicted_species", "predicted_code", "predicted_prob",
    "true_species", "true_code",
    "user_notes", "latitude", "longitude",
]


def _hash_image_bytes(pil_image: Image.Image) -> str:
    """SHA-1 (12 chars) de los bytes RGB para nombre único reproducible."""
    arr = pil_image.convert("RGB").tobytes()
    return hashlib.sha1(arr).hexdigest()[:12]


def _ensure_csv() -> None:
    """Crea CSV si no existe con header."""
    FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)
    if not FEEDBACK_LOG.exists():
        with open(FEEDBACK_LOG, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=FIELDNAMES)
            w.writeheader()


def record_feedback(
    pil_image: Image.Image,
    decision: str,                            # "confirm" | "correct" | "not_raptor"
    predicted_species: str,
    predicted_code: str,
    predicted_prob: float,
    true_species: Optional[str] = None,
    true_code: Optional[str] = None,
    user_notes: str = "",
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
) -> dict:
    """
    Guarda una corrección. Devuelve dict con info sobre lo guardado.

    decision:
      - "confirm"      → el usuario confirma que la predicción es correcta
      - "correct"      → la predicción es errónea; true_species es la correcta
      - "not_raptor"   → la imagen no es de una rapaz (ruido / negativo)
    """
    _ensure_csv()

    img_hash = _hash_image_bytes(pil_image)
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

    # Guardar la imagen físicamente (organizada por etiqueta real)
    if decision == "confirm":
        target_species = predicted_species
    elif decision == "correct":
        if not true_species:
            return {"ok": False, "error": "Necesitas indicar true_species para corregir."}
        target_species = true_species
    elif decision == "not_raptor":
        target_species = "_not_raptor"
    else:
        return {"ok": False, "error": f"Decisión no reconocida: {decision}"}

    species_folder = FEEDBACK_DIR / target_species
    species_folder.mkdir(parents=True, exist_ok=True)
    image_path = species_folder / f"{img_hash}.jpg"
    pil_image.convert("RGB").save(image_path, quality=92)

    # Registrar en CSV
    with open(FEEDBACK_LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        w.writerow({
            "timestamp_utc": timestamp,
            "filename_hash": img_hash,
            "image_path": str(image_path.relative_to(config.DATA_DIR)),
            "decision": decision,
            "predicted_species": predicted_species,
            "predicted_code": predicted_code,
            "predicted_prob": f"{predicted_prob:.4f}",
            "true_species": true_species or "",
            "true_code": true_code or "",
            "user_notes": user_notes,
            "latitude": f"{latitude:.6f}" if latitude is not None else "",
            "longitude": f"{longitude:.6f}" if longitude is not None else "",
        })

    return {
        "ok": True,
        "image_path": str(image_path),
        "target_species": target_species,
        "decision": decision,
        "hash": img_hash,
    }


def get_feedback_stats() -> dict:
    """Estadísticas del feedback acumulado."""
    if not FEEDBACK_LOG.exists():
        return {"total": 0, "by_decision": {}, "by_species": {}}

    total = 0
    by_decision = {}
    by_species = {}
    with open(FEEDBACK_LOG, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            total += 1
            by_decision[row["decision"]] = by_decision.get(row["decision"], 0) + 1
            label = row["true_species"] or row["predicted_species"]
            by_species[label] = by_species.get(label, 0) + 1

    return {
        "total": total,
        "by_decision": by_decision,
        "by_species": by_species,
        "ready_for_retrain": total >= 50,  # umbral arbitrario
    }


def get_recent_feedback(limit: int = 20) -> list[dict]:
    """Devuelve las últimas N entradas del log."""
    if not FEEDBACK_LOG.exists():
        return []
    with open(FEEDBACK_LOG, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return rows[-limit:][::-1]  # más reciente primero
