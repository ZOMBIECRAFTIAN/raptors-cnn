"""
Generador de dataset sintético — útil para probar el pipeline end-to-end
antes de tener las imágenes reales de las rapaces.

Crea un mini-dataset en datos/processed/{train,val,test}/<especie>/ con
imágenes sintéticas (gradientes + texto + ruido) que imitan la estructura
del dataset real. NO sirve para entrenar un modelo realista — solo verifica
que la cadena de carga, augmentation, modelo, train, evaluate y Grad-CAM
funcione correctamente.

Uso:
    conda activate raptors-pt
    cd codigo/pytorch
    python make_synthetic_dataset.py            # genera 50/10/10 por especie
    python make_synthetic_dataset.py --n 200    # más imágenes por especie
"""
import argparse
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import config


def make_one_image(species_idx: int, code: str, common: str, scientific: str,
                   size: int = 256, seed: int = 0) -> Image.Image:
    """Imagen sintética con un patrón visualmente distinto por clase."""
    rng = np.random.default_rng(seed)

    # Color de fondo: cada especie tiene un tono base distinto
    hue_base = (species_idx * 25) % 360
    bg = _hsl_to_rgb(hue_base, 30, 80)
    fg = _hsl_to_rgb(hue_base, 80, 25)

    # Gradiente diagonal
    arr = np.zeros((size, size, 3), dtype=np.uint8)
    for y in range(size):
        t = y / size
        row = (1 - t) * np.array(bg) + t * np.array(fg)
        arr[y, :, :] = row.astype(np.uint8)

    # Forma geométrica que codifica la especie (figuras distintas por clase)
    img = Image.fromarray(arr)
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2
    r = size // 3
    if species_idx % 4 == 0:                                       # círculo
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=fg, width=4)
    elif species_idx % 4 == 1:                                     # cuadrado
        draw.rectangle((cx - r, cy - r, cx + r, cy + r), outline=fg, width=4)
    elif species_idx % 4 == 2:                                     # triángulo
        draw.polygon([(cx, cy - r), (cx - r, cy + r), (cx + r, cy + r)],
                     outline=fg, width=4)
    else:                                                          # cruz
        draw.line((cx - r, cy, cx + r, cy), fill=fg, width=4)
        draw.line((cx, cy - r, cx, cy + r), fill=fg, width=4)

    # Etiqueta con el código de especie
    try:
        font = ImageFont.truetype("arial.ttf", size // 6)
    except Exception:
        font = ImageFont.load_default()
    draw.text((10, 10), code, fill=fg, font=font)
    draw.text((10, size - 30), scientific, fill=fg, font=font)

    # Ruido para que la red tenga algo que aprender
    noise = (rng.normal(0, 8, (size, size, 3))).clip(-30, 30).astype(np.int16)
    arr = np.clip(np.array(img).astype(np.int16) + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)


def _hsl_to_rgb(h: float, s: float, l: float):
    """HSL (h en grados, s y l en %) → tupla (r, g, b) 0-255."""
    import colorsys
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return int(r * 255), int(g * 255), int(b * 255)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=70,
                        help="imágenes por especie (default 70 = 50 train + 10 val + 10 test)")
    parser.add_argument("--size", type=int, default=256, help="tamaño de la imagen")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed); np.random.seed(args.seed)

    n_total = args.n
    n_train = int(0.7 * n_total)
    n_val   = int(0.15 * n_total)
    n_test  = n_total - n_train - n_val

    print(f"Generando dataset sintético en {config.PROCESSED_DIR}")
    print(f"  {n_total} imágenes × {config.NUM_CLASSES} especies = {n_total * config.NUM_CLASSES} imágenes")
    print(f"  Split: train={n_train}, val={n_val}, test={n_test}")

    splits = {"train": n_train, "val": n_val, "test": n_test}

    for idx, (sp, code, common) in enumerate(zip(
            config.SPECIES, config.SPECIES_CODE, config.SPECIES_COMMON)):
        for split, n in splits.items():
            out_dir = config.PROCESSED_DIR / split / sp
            out_dir.mkdir(parents=True, exist_ok=True)
            for j in range(n):
                seed = idx * 10_000 + (0 if split == "train" else 1 if split == "val" else 2) * 1000 + j
                img = make_one_image(idx, code, common, sp.replace("_", " "),
                                     size=args.size, seed=seed)
                img.save(out_dir / f"{code}_{split}_{j:04d}.jpg", quality=85)
        print(f"  ✓ {code}  {sp}")

    print("\n✅ Dataset sintético listo.\n"
          "   Ahora puedes correr:\n"
          "     python train.py --arch resnet50 --smoke-test\n")


if __name__ == "__main__":
    main()
