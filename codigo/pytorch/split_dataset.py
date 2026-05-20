"""
split_dataset.py — Divide datos/raw/<especie>/*.jpg en train/val/test (70/15/15)
y los copia a datos/processed/{train,val,test}/<especie>/.

Uso:
    conda activate raptors-pt
    cd codigo/pytorch
    python split_dataset.py                          # 70/15/15 por defecto
    python split_dataset.py --train 0.8 --val 0.1   # 80/10/10
    python split_dataset.py --species Harpia_harpyja # solo una especie
    python split_dataset.py --dry-run                # solo lista, no copia
    python split_dataset.py --link                   # usa hardlinks (más rápido)
    python split_dataset.py --clean                  # vacía processed antes

Garantiza:
- Reproducibilidad (seed=42) — el mismo split cada vez.
- Estratificación por especie (cada especie tiene proporciones consistentes).
- No mezcla imágenes V1 ya splitteadas (detecta si una imagen ya está
  en train/val/test y respeta su asignación).

Importante: ImageFolder ordena alfabéticamente, así que el orden de
config.SPECIES debe coincidir con `sorted(os.listdir(processed/train))`.
"""
from __future__ import annotations
import argparse
import random
import shutil
from pathlib import Path

import config

VALID_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp"}

# Subcarpetas que curate.py crea y deben ignorarse al splittear (son artefactos):
SKIP_SUBDIRS = {"_review", "_discard", "_rejected", "_audit"}
# Subcarpetas válidas que curate.py crea para imágenes que se quedan:
KEEP_SUBDIRS = {"_kept", "_keep"}


def list_images(folder: Path, recursive: bool = True) -> list[Path]:
    """Devuelve lista de imágenes.

    Si `recursive=True`, busca también dentro de subcarpetas como `_kept/`
    (usadas por curate.py), excluyendo `_review/` y similares.
    """
    if not folder.exists():
        return []
    if not recursive:
        return sorted(
            p for p in folder.iterdir()
            if p.is_file() and p.suffix.lower() in VALID_EXTS
        )
    # Recursivo: escanea folder + cualquier subcarpeta excepto SKIP_SUBDIRS
    out: list[Path] = []
    for p in folder.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in VALID_EXTS:
            continue
        # Si está dentro de una subcarpeta a ignorar (e.g. _review), salta
        if any(part in SKIP_SUBDIRS for part in p.relative_to(folder).parts):
            continue
        out.append(p)
    return sorted(out)


def existing_assignments(processed_dir: Path, sci: str) -> dict[str, str]:
    """Lee qué archivos YA están en train/val/test para no re-asignarlos."""
    mapping: dict[str, str] = {}
    for split in ("train", "val", "test"):
        d = processed_dir / split / sci
        if d.exists():
            for p in list_images(d):
                mapping[p.name] = split
    return mapping


def transfer(src: Path, dst: Path, *, use_link: bool, dry_run: bool) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dry_run:
        return
    if use_link:
        try:
            if dst.exists():
                dst.unlink()
            dst.hardlink_to(src)  # Python ≥ 3.10
            return
        except (OSError, AttributeError):
            pass
    shutil.copy2(src, dst)


def split_one_species(
    sci: str, raw_dir: Path, processed_dir: Path,
    train_p: float, val_p: float, test_p: float,
    use_link: bool, dry_run: bool, seed: int,
) -> dict[str, int]:
    """Splittea las imágenes de una especie. Devuelve conteos por split."""
    src_folder = raw_dir / sci
    images = list_images(src_folder)
    if not images:
        return {"train": 0, "val": 0, "test": 0, "skipped": 0}

    # Respeta asignaciones existentes para imágenes V1 ya splitteadas
    existing = existing_assignments(processed_dir, sci)

    # Imágenes nuevas (no asignadas previamente)
    new_images = [img for img in images if img.name not in existing]
    rng = random.Random(seed + hash(sci) % 10_000)
    rng.shuffle(new_images)

    n_new = len(new_images)
    n_train = int(n_new * train_p)
    n_val = int(n_new * val_p)
    # el resto al test (para no perder por redondeo)
    train_imgs = new_images[:n_train]
    val_imgs = new_images[n_train:n_train + n_val]
    test_imgs = new_images[n_train + n_val:]

    counts = {"train": 0, "val": 0, "test": 0, "skipped": 0}

    # Existing — solo verifica que sigan en su sitio
    for img in images:
        if img.name in existing:
            counts[existing[img.name]] += 1

    # Nuevas — transferir
    for split_name, lst in (("train", train_imgs), ("val", val_imgs), ("test", test_imgs)):
        for img in lst:
            dst = processed_dir / split_name / sci / img.name
            if dst.exists():
                counts["skipped"] += 1
                continue
            transfer(img, dst, use_link=use_link, dry_run=dry_run)
            counts[split_name] += 1

    return counts


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--train", type=float, default=0.70)
    p.add_argument("--val", type=float, default=0.15)
    p.add_argument("--test", type=float, default=0.15)
    p.add_argument("--species", default=None,
                   help="Solo splittea esta especie (Genus_species)")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--link", action="store_true",
                   help="Usa hardlinks en lugar de copiar (ahorra disco)")
    p.add_argument("--clean", action="store_true",
                   help="Vacía processed/{train,val,test}/<especie> antes")
    p.add_argument("--seed", type=int, default=config.SEED)
    args = p.parse_args()

    assert abs(args.train + args.val + args.test - 1.0) < 1e-6, \
        f"Las proporciones deben sumar 1: {args.train + args.val + args.test}"

    raw_dir = config.RAW_DIR
    processed_dir = config.PROCESSED_DIR
    print(f"Origen:  {raw_dir}")
    print(f"Destino: {processed_dir}")
    print(f"Split:   {args.train:.0%} train · {args.val:.0%} val · {args.test:.0%} test")
    if args.dry_run:
        print("⚡ DRY RUN — no se copia nada\n")
    if args.link:
        print("🔗 Usando hardlinks (más rápido, requiere mismo sistema de archivos)\n")

    species_list = ([args.species] if args.species
                    else sorted(config.SPECIES))

    grand_total = {"train": 0, "val": 0, "test": 0, "skipped": 0}
    sin_imagenes = []
    for sci in species_list:
        if args.clean and not args.dry_run:
            for split in ("train", "val", "test"):
                d = processed_dir / split / sci
                if d.exists():
                    shutil.rmtree(d)
                    d.mkdir(parents=True)

        c = split_one_species(
            sci, raw_dir, processed_dir,
            args.train, args.val, args.test,
            args.link, args.dry_run, args.seed,
        )
        marker = "❌" if c["train"] + c["val"] + c["test"] == 0 else "✓"
        if marker == "❌":
            sin_imagenes.append(sci)
        print(f"  {marker} {sci:34s} → train={c['train']:5d}  val={c['val']:4d}  "
              f"test={c['test']:4d}  (skipped={c['skipped']})")
        for k in grand_total:
            grand_total[k] += c[k]

    print(f"\n📊 TOTAL: train={grand_total['train']}  val={grand_total['val']}  "
          f"test={grand_total['test']}  (omitidas={grand_total['skipped']})")

    if sin_imagenes:
        print(f"\n⚠️  {len(sin_imagenes)} especies sin imágenes en datos/raw/:")
        for s in sin_imagenes:
            print(f"    - {s}")
        print(f"\n    Ejecuta:  python download_inaturalist.py --target 200")
        print(f"    para descargar las que faltan.")


if __name__ == "__main__":
    main()
