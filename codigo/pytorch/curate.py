"""
curate.py — Filtros automáticos sobre imágenes descargadas de iNaturalist.

Analiza cada imagen y calcula:
  - Resolución (lado mayor en px)
  - Brillo promedio (0-255)
  - Contraste (desviación estándar)
  - Sharpness (Laplacian variance — detecta blur)
  - Aspect ratio
  - Color dominante (RGB del centro)
  - Hash perceptual (para detectar duplicados)

Asigna un score 0-100 y propone una decisión (KEEP / REVIEW / DISCARD).
NO borra nada — solo escribe un CSV en datos/annotations/curation_report.csv
y mueve archivos a subcarpetas según la decisión propuesta.

Uso:
    conda activate raptors-pt
    cd codigo/pytorch
    python curate.py                    # analiza datos/raw/ y genera reporte
    python curate.py --apply            # mueve archivos según propuesta
    python curate.py --species TV       # solo una especie
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import shutil
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm

import config


# Umbrales (ajustables)
MIN_RESOLUTION = 640        # lado mayor mínimo en px
MIN_BRIGHTNESS = 30         # 0-255
MAX_BRIGHTNESS = 240
MIN_CONTRAST = 15           # desviación estándar
MIN_SHARPNESS = 60          # Laplacian variance — bajo este valor = blur
MIN_ASPECT_RATIO = 0.4      # 1:2.5 mínimo
MAX_ASPECT_RATIO = 2.5      # 2.5:1 máximo


def perceptual_hash(img: np.ndarray) -> str:
    """Hash perceptual simple para detectar duplicados (32x32, mean threshold)."""
    small = cv2.resize(img, (32, 32), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(small, cv2.COLOR_RGB2GRAY)
    avg = gray.mean()
    bits = (gray > avg).flatten().astype(np.uint8)
    # 1024 bits → 256 hex chars; usamos los primeros 32 hex (128 bits)
    by = np.packbits(bits[:1024])
    return hashlib.md5(by.tobytes()).hexdigest()[:16]


def analyze_image(path: Path) -> dict:
    """Devuelve dict con métricas de calidad de una imagen."""
    try:
        # Cargar con PIL para EXIF, luego a numpy
        pil = Image.open(path).convert("RGB")
        w, h = pil.size
        arr = np.array(pil)
        gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)

        long_side = max(w, h)
        short_side = min(w, h)
        aspect = w / h
        brightness = gray.mean()
        contrast = gray.std()
        laplacian = cv2.Laplacian(gray, cv2.CV_64F).var()
        phash = perceptual_hash(arr)

        return {
            "ok": True,
            "filename": path.name,
            "filesize_kb": path.stat().st_size // 1024,
            "width": w, "height": h,
            "long_side": long_side, "short_side": short_side,
            "aspect_ratio": round(aspect, 3),
            "brightness": round(brightness, 1),
            "contrast": round(contrast, 1),
            "sharpness": round(laplacian, 1),
            "phash": phash,
        }
    except Exception as e:
        return {"ok": False, "filename": path.name, "error": str(e)}


def score_image(m: dict) -> tuple[int, list[str], str]:
    """Score 0-100 + lista de issues + decisión (KEEP/REVIEW/DISCARD)."""
    if not m.get("ok"):
        return 0, ["unreadable"], "DISCARD"

    issues = []
    score = 100

    if m["long_side"] < MIN_RESOLUTION:
        issues.append(f"low_res ({m['long_side']}<{MIN_RESOLUTION})")
        score -= 40

    if m["brightness"] < MIN_BRIGHTNESS:
        issues.append(f"too_dark ({m['brightness']:.0f})")
        score -= 25
    elif m["brightness"] > MAX_BRIGHTNESS:
        issues.append(f"too_bright ({m['brightness']:.0f})")
        score -= 15

    if m["contrast"] < MIN_CONTRAST:
        issues.append(f"low_contrast ({m['contrast']:.0f})")
        score -= 20

    if m["sharpness"] < MIN_SHARPNESS:
        issues.append(f"blurry (sharpness={m['sharpness']:.0f})")
        score -= 30

    if m["aspect_ratio"] < MIN_ASPECT_RATIO or m["aspect_ratio"] > MAX_ASPECT_RATIO:
        issues.append(f"extreme_aspect ({m['aspect_ratio']:.2f})")
        score -= 15

    score = max(0, score)

    if score >= 75:
        decision = "KEEP"
    elif score >= 45:
        decision = "REVIEW"
    else:
        decision = "DISCARD"

    return score, issues, decision


def process_species(raw_dir: Path, species_name: str,
                    apply: bool, report_writer) -> tuple[int, int, int]:
    """Procesa todas las imágenes de una especie. Devuelve (keep, review, discard)."""
    sp_dir = raw_dir / species_name
    if not sp_dir.exists():
        print(f"  [skip] {species_name}: carpeta no existe")
        return (0, 0, 0)

    images = sorted(sp_dir.glob("*.jpg")) + sorted(sp_dir.glob("*.jpeg")) + \
             sorted(sp_dir.glob("*.png"))
    if not images:
        return (0, 0, 0)

    counts = {"KEEP": 0, "REVIEW": 0, "DISCARD": 0}
    seen_hashes = {}

    for img_path in tqdm(images, desc=f"  {species_name}", leave=False):
        metrics = analyze_image(img_path)
        score, issues, decision = score_image(metrics)

        # Detección de duplicados (entre archivos en MISMA especie)
        if metrics.get("ok") and metrics["phash"] in seen_hashes:
            issues.append(f"duplicate_of_{seen_hashes[metrics['phash']]}")
            decision = "DISCARD"
        elif metrics.get("ok"):
            seen_hashes[metrics["phash"]] = img_path.name

        counts[decision] += 1

        # Escribir al CSV
        report_writer.writerow({
            "species": species_name,
            "filename": metrics.get("filename", img_path.name),
            "decision": decision,
            "score": score,
            "issues": "; ".join(issues) or "—",
            **{k: metrics.get(k, "") for k in
                ["filesize_kb", "width", "height", "long_side",
                 "aspect_ratio", "brightness", "contrast", "sharpness", "phash"]},
        })

        # Aplicar (mover archivo a subcarpeta de decisión)
        if apply:
            target_subdir = sp_dir / f"_{decision.lower()}"
            target_subdir.mkdir(exist_ok=True)
            shutil.move(str(img_path), str(target_subdir / img_path.name))

    return (counts["KEEP"], counts["REVIEW"], counts["DISCARD"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--species", default=None,
                        help="Solo procesar una especie (nombre científico con _)")
    parser.add_argument("--apply", action="store_true",
                        help="Mover archivos a subcarpetas _keep / _review / _discard")
    args = parser.parse_args()

    raw_dir = config.RAW_DIR
    annot_dir = config.ANNOTATIONS_DIR
    annot_dir.mkdir(parents=True, exist_ok=True)

    species_to_do = [args.species] if args.species else config.SPECIES

    report_path = annot_dir / "curation_report.csv"
    fieldnames = [
        "species", "filename", "decision", "score", "issues",
        "filesize_kb", "width", "height", "long_side",
        "aspect_ratio", "brightness", "contrast", "sharpness", "phash",
    ]

    print(f"Curando imágenes en {raw_dir}")
    print(f"Reporte → {report_path}")
    if args.apply:
        print("⚡ Modo APPLY: los archivos se MOVERÁN a subcarpetas _keep/_review/_discard.")
    else:
        print("Modo dry-run: solo escribe el reporte, no toca archivos.")

    total = {"KEEP": 0, "REVIEW": 0, "DISCARD": 0}
    with open(report_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for sp in species_to_do:
            k, r, d = process_species(raw_dir, sp, args.apply, w)
            total["KEEP"] += k; total["REVIEW"] += r; total["DISCARD"] += d
            if k + r + d > 0:
                print(f"  ✓ {sp}: KEEP={k}  REVIEW={r}  DISCARD={d}")

    print(f"\n=== Totales ===")
    print(f"  KEEP    : {total['KEEP']}")
    print(f"  REVIEW  : {total['REVIEW']}  (revisar manualmente)")
    print(f"  DISCARD : {total['DISCARD']}")
    print(f"  Reporte : {report_path}")


if __name__ == "__main__":
    main()
