"""
Procesamiento de video frame-by-frame.

Toma un archivo de video, extrae un frame cada N segundos, y devuelve:
  - una lista de detecciones [(timestamp_s, especie, prob, frame_PIL), ...]
  - una imagen "timeline" mostrando las detecciones en orden temporal
"""
from __future__ import annotations
import io
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

from .config_app import (
    VIDEO_SAMPLE_EVERY_SECS, VIDEO_MAX_DURATION_SECS, VIDEO_MIN_CONFIDENCE,
    SPECIES_DATA, SPECIES_ORDER, THEME_PRIMARY, THEME_ACCENT,
)
from .inference import get_classifier


def process_video(video_path: str | Path,
                  sample_every: float = VIDEO_SAMPLE_EVERY_SECS,
                  max_duration: float = VIDEO_MAX_DURATION_SECS,
                  min_confidence: float = VIDEO_MIN_CONFIDENCE) -> dict:
    """
    Procesa un video y devuelve detecciones por frame muestreado.
    """
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return {"error": f"No se pudo abrir el video: {video_path}"}

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0

    if duration > max_duration:
        cap.release()
        return {
            "error": f"El video dura {duration:.1f}s. Máximo permitido: {max_duration}s. "
                     f"Recorta el video antes de subirlo."
        }

    clf = get_classifier()
    if not clf.loaded:
        cap.release()
        return {"error": "Modelo no disponible. Entrena con `python train.py --smoke-test`."}

    detections = []  # list of dicts {t, species, code, common, prob, frame_pil}
    skip_n_frames = max(1, int(fps * sample_every))
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % skip_n_frames == 0:
            # BGR (OpenCV) -> RGB (PIL)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil = Image.fromarray(rgb)
            pred = clf.predict(pil, top_k=3)
            if "error" not in pred and pred["top1_prob"] >= min_confidence:
                detections.append({
                    "t": frame_idx / fps,
                    "species": pred["top1_species"],
                    "code": pred["top1_code"],
                    "common": pred["top1_common"],
                    "prob": pred["top1_prob"],
                    "frame_pil": pil,
                    "topk": pred["topk"],
                })
        frame_idx += 1

    cap.release()

    if not detections:
        return {"error": "No se detectaron rapaces con confianza suficiente en este video."}

    # Generar timeline plot
    timeline_img = _make_timeline_plot(detections, duration)

    # Generar tabla de detecciones (lista de dicts simples para Gradio)
    rows = [
        [f"{d['t']:.1f} s", d["code"], d["common"], d["species"], f"{d['prob']*100:.1f}%"]
        for d in detections
    ]
    return {
        "duration": duration,
        "n_samples": len(detections),
        "detections": detections,
        "timeline_image": timeline_img,
        "table_rows": rows,
        "best_detection": max(detections, key=lambda d: d["prob"]),
    }


def _make_timeline_plot(detections: list[dict], duration: float) -> Image.Image:
    """Genera una imagen tipo timeline con las detecciones."""
    fig, ax = plt.subplots(figsize=(12, 4))

    # Eje X: tiempo
    ax.set_xlim(0, duration)
    ax.set_ylim(0, 1.1)
    ax.set_xlabel("Tiempo (segundos)")
    ax.set_ylabel("Probabilidad")
    ax.set_title("Timeline de detecciones", fontsize=14, weight="bold", color=THEME_PRIMARY)
    ax.grid(True, alpha=0.3)

    # Color por especie (sólido)
    species_to_color = {}
    cmap = plt.cm.tab20
    for i, sp in enumerate(SPECIES_ORDER):
        species_to_color[sp] = cmap(i / len(SPECIES_ORDER))

    # Barras verticales por detección
    for d in detections:
        ax.bar(d["t"], d["prob"], width=0.5,
               color=species_to_color.get(d["species"], "gray"),
               edgecolor="white", linewidth=0.5)
        ax.text(d["t"], d["prob"] + 0.03, d["code"],
                ha="center", fontsize=8, weight="bold")

    # Leyenda de especies detectadas
    detected_species = list({d["species"]: d for d in detections}.values())
    handles = [plt.Rectangle((0, 0), 1, 1, color=species_to_color[d["species"]],
                              label=f"{d['code']} · {d['common']}")
               for d in detected_species]
    ax.legend(handles=handles, loc="upper right", fontsize=8, framealpha=0.95)

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)
