"""
Generador de dataset sintético — versión TensorFlow.

Es idéntico al de PyTorch (mismo código, mismas imágenes), pero importa
config desde el directorio tensorflow/ para que las rutas y SPECIES sean las
mismas que usa la implementación TF. Puedes correr UNO de los dos
(no los dos) ya que ambos producen el mismo dataset en datos/processed/.
"""
import argparse
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import config


def _hsl_to_rgb(h, s, l):
    import colorsys
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return int(r * 255), int(g * 255), int(b * 255)


def make_one_image(species_idx, code, scientific, size=256, seed=0):
    rng = np.random.default_rng(seed)
    hue_base = (species_idx * 25) % 360
    bg = _hsl_to_rgb(hue_base, 30, 80)
    fg = _hsl_to_rgb(hue_base, 80, 25)

    arr = np.zeros((size, size, 3), dtype=np.uint8)
    for y in range(size):
        t = y / size
        row = (1 - t) * np.array(bg) + t * np.array(fg)
        arr[y, :, :] = row.astype(np.uint8)

    img = Image.fromarray(arr); draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2; r = size // 3
    if species_idx % 4 == 0: draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=fg, width=4)
    elif species_idx % 4 == 1: draw.rectangle((cx - r, cy - r, cx + r, cy + r), outline=fg, width=4)
    elif species_idx % 4 == 2: draw.polygon([(cx, cy - r), (cx - r, cy + r), (cx + r, cy + r)], outline=fg, width=4)
    else:
        draw.line((cx - r, cy, cx + r, cy), fill=fg, width=4)
        draw.line((cx, cy - r, cx, cy + r), fill=fg, width=4)

    try: font = ImageFont.truetype("arial.ttf", size // 6)
    except Exception: font = ImageFont.load_default()
    draw.text((10, 10), code, fill=fg, font=font)
    draw.text((10, size - 30), scientific, fill=fg, font=font)

    noise = (rng.normal(0, 8, (size, size, 3))).clip(-30, 30).astype(np.int16)
    arr = np.clip(np.array(img).astype(np.int16) + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=70)
    parser.add_argument("--size", type=int, default=256)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed); np.random.seed(args.seed)

    n_train = int(0.7 * args.n); n_val = int(0.15 * args.n); n_test = args.n - n_train - n_val
    splits = {"train": n_train, "val": n_val, "test": n_test}

    print(f"Generando dataset sintético en {config.PROCESSED_DIR}")
    for idx, (sp, code) in enumerate(zip(config.SPECIES, config.SPECIES_CODE)):
        for split, n in splits.items():
            out_dir = config.PROCESSED_DIR / split / sp
            out_dir.mkdir(parents=True, exist_ok=True)
            for j in range(n):
                seed = idx * 10_000 + (0 if split == "train" else 1 if split == "val" else 2) * 1000 + j
                img = make_one_image(idx, code, sp.replace("_", " "), size=args.size, seed=seed)
                img.save(out_dir / f"{code}_{split}_{j:04d}.jpg", quality=85)
        print(f"  ✓ {code}  {sp}")

    print("\n✅ Dataset sintético listo. Ahora puedes correr:\n   python train.py --arch resnet50 --smoke-test\n")


if __name__ == "__main__":
    main()
