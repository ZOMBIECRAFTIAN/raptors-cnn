"""
Módulo de observaciones — guarda registros completos de cada predicción
realizada por el usuario, opcionalmente con coordenadas GPS y notas.

A diferencia de feedback.py (correcciones para retraining), esto es un
registro histórico tipo "log de avistamientos científicos", compatible con
estándares Darwin Core para potencial exportación a iNaturalist / eBird.
"""
from __future__ import annotations
import csv
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from PIL import Image

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config

OBS_DIR = config.DATA_DIR / "observations"
OBS_LOG = OBS_DIR / "observations.csv"

# Compatible con Darwin Core mínimo
FIELDNAMES = [
    "observation_id", "timestamp_utc", "user_id",
    "species_scientific", "species_common", "species_code",
    "confidence", "image_filename",
    "latitude", "longitude", "elevation",
    "location_name", "country", "stateProvince",
    "notes",
]


def _ensure_csv() -> None:
    OBS_DIR.mkdir(parents=True, exist_ok=True)
    if not OBS_LOG.exists():
        with open(OBS_LOG, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=FIELDNAMES)
            w.writeheader()


def save_observation(
    pil_image: Image.Image,
    species_scientific: str,
    species_common: str,
    species_code: str,
    confidence: float,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    elevation: Optional[float] = None,
    location_name: str = "",
    country: str = "MX",
    state_province: str = "Veracruz",
    notes: str = "",
    user_id: str = "anonymous",
) -> dict:
    """
    Persiste una observación completa.
    """
    _ensure_csv()

    obs_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

    # Guardar imagen
    img_dir = OBS_DIR / "images"
    img_dir.mkdir(parents=True, exist_ok=True)
    img_path = img_dir / f"{obs_id}.jpg"
    pil_image.convert("RGB").save(img_path, quality=92)

    # Registrar
    with open(OBS_LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        w.writerow({
            "observation_id": obs_id,
            "timestamp_utc": timestamp,
            "user_id": user_id,
            "species_scientific": species_scientific,
            "species_common": species_common,
            "species_code": species_code,
            "confidence": f"{confidence:.4f}",
            "image_filename": img_path.name,
            "latitude": f"{latitude:.6f}" if latitude is not None else "",
            "longitude": f"{longitude:.6f}" if longitude is not None else "",
            "elevation": f"{elevation:.1f}" if elevation is not None else "",
            "location_name": location_name,
            "country": country,
            "stateProvince": state_province,
            "notes": notes,
        })

    return {
        "ok": True,
        "observation_id": obs_id,
        "image_path": str(img_path),
        "darwin_core_compatible": True,
    }


def get_observation_stats() -> dict:
    if not OBS_LOG.exists():
        return {"total": 0, "by_species": {}, "with_gps": 0}

    total = 0
    by_species = {}
    with_gps = 0
    with open(OBS_LOG, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            total += 1
            sp = row["species_scientific"]
            by_species[sp] = by_species.get(sp, 0) + 1
            if row["latitude"] and row["longitude"]:
                with_gps += 1
    return {
        "total": total,
        "by_species": by_species,
        "with_gps": with_gps,
        "without_gps": total - with_gps,
    }
