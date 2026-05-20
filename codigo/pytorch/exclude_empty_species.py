"""
fill_empty_species.py (antes exclude_empty_species.py)

Genera una imagen placeholder gris (224×224, "no data") para cada especie
que no tiene imágenes en datos/processed/{train,val,test}/. Esto permite
que ImageFolder no falle y el pipeline corra end-to-end. El modelo no
aprenderá nada útil para esas especies, pero podrás reemplazar el
placeholder con imágenes reales después.

Es la solución más simple y reversible — al descargar imágenes reales,
borra el placeholder y vuelve a correr split_dataset.py.

Uso:
    python exclude_empty_species.py                       # rellena todas las vacías
    python exclude_empty_species.py --species Daptrius_americanus  # solo una
    python exclude_empty_species.py --clean               # borra los placeholders
"""
from __future__ import annotations
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import config

PLACEHOLDER_NAME = "_placeholder_no_data.jpg"
VALID_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp"}


def has_real_images(folder: Path) -> bool:
    if not folder.exists():
        return False
    for p in folder.iterdir():
        if p.is_file() and p.suffix.lower() in VALID_EXTS and p.name != PLACEHOLDER_NAME:
            return True
    return False


def make_placeholder(text: str, dest: Path) -> None:
    """Crea una imagen gris 224×224 con el nombre de la especie escrito."""
    img = Image.new("RGB", (224, 224), color=(128, 128, 128))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except Exception:
        font = ImageFont.load_default()
    # Texto en varias líneas si es largo
    lines = []
    words = text.replace("_", " ").split()
    line = ""
    for w in words:
        if len(line) + len(w) + 1 > 18:
            lines.append(line.strip())
            line = w + " "
        else:
            line += w + " "
    if line.strip():
        lines.append(line.strip())
    lines.append("(no data)")
    y = 100 - 10 * len(lines)
    for ln in lines:
        bbox = draw.textbbox((0, 0), ln, font=font)
        w = bbox[2] - bbox[0]
        draw.text(((224 - w) // 2, y), ln, fill=(255, 255, 255), font=font)
        y += 20
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, quality=85)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--species", nargs="+", default=None,
                   help="Solo rellena estas especies (nombres científicos)")
    p.add_argument("--clean", action="store_true",
                   help="Borra los placeholders generados")
    args = p.parse_args()

    splits = ("train", "val", "test")
    if args.clean:
        n_removed = 0
        for split in splits:
            for sci in config.SPECIES:
                p = config.PROCESSED_DIR / split / sci / PLACEHOLDER_NAME
                if p.exists():
                    p.unlink()
                    n_removed += 1
        print(f"✅ Eliminados {n_removed} placeholders")
        return

    target_species = args.species if args.species else list(config.SPECIES)

    created = 0
    for sci in target_species:
        for split in splits:
            folder = config.PROCESSED_DIR / split / sci
            if has_real_images(folder):
                continue
            dest = folder / PLACEHOLDER_NAME
            make_placeholder(sci, dest)
            created += 1
            print(f"  ✓ {split}/{sci}/{PLACEHOLDER_NAME}")

    print(f"\n✅ Creados {created} placeholders")
    print("   El modelo no aprenderá nada útil de las especies con placeholder.")
    print("   Cuando descargues imágenes reales, ejecuta:")
    print("       python exclude_empty_species.py --clean")
    print("       python split_dataset.py")


if __name__ == "__main__":
    main()
