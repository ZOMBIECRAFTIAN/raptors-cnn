"""
contar_dataset.py - cuenta imagenes por split y por especie

Uso:
    python contar_dataset.py
    python contar_dataset.py --por-especie       # detalle por especie
    python contar_dataset.py --base datos/processed
"""
import argparse
import os
from pathlib import Path

EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif"}


def contar(split_dir: Path) -> tuple[int, dict[str, int]]:
    """Devuelve (total, {especie: n}) para un split."""
    por_especie: dict[str, int] = {}
    if not split_dir.exists():
        return 0, por_especie
    for sp in sorted(split_dir.iterdir()):
        if not sp.is_dir():
            continue
        n = sum(1 for f in sp.iterdir() if f.suffix.lower() in EXT)
        por_especie[sp.name] = n
    total = sum(por_especie.values())
    return total, por_especie


def main() -> None:
    ap = argparse.ArgumentParser(description="Cuenta imagenes del dataset")
    ap.add_argument("--base", default="datos/processed",
                    help="Carpeta base con subdirs train/val/test")
    ap.add_argument("--por-especie", action="store_true",
                    help="Lista conteo por especie (ordenado por menor)")
    args = ap.parse_args()

    base = Path(args.base)
    if not base.exists():
        print(f"ERROR: la carpeta {base.resolve()} no existe.")
        return

    print(f"\nDataset en: {base.resolve()}\n")
    print(f"{'SPLIT':<6} {'TOTAL':>8} {'ESPECIES':>10}")
    print("-" * 28)

    todos: dict[str, dict[str, int]] = {}
    for split in ("train", "val", "test"):
        total, por_sp = contar(base / split)
        todos[split] = por_sp
        print(f"{split:<6} {total:>8} {len(por_sp):>10}")

    if args.por_especie and todos.get("train"):
        print("\nConteo por especie en TRAIN (ordenado por menor):")
        print("-" * 50)
        ordenado = sorted(todos["train"].items(), key=lambda kv: kv[1])
        for sp, n in ordenado:
            print(f"  {n:>5}  {sp}")

    # Resumen sanity-check
    train_sp = set(todos.get("train", {}))
    val_sp = set(todos.get("val", {}))
    test_sp = set(todos.get("test", {}))
    faltan_val = train_sp - val_sp
    faltan_test = train_sp - test_sp
    if faltan_val:
        print(f"\nADVERTENCIA: {len(faltan_val)} especies en train sin val: "
              f"{sorted(faltan_val)[:5]}")
    if faltan_test:
        print(f"ADVERTENCIA: {len(faltan_test)} especies en train sin test: "
              f"{sorted(faltan_test)[:5]}")


if __name__ == "__main__":
    main()
