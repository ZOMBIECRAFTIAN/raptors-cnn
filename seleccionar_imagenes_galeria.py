"""
seleccionar_imagenes_galeria.py

Para cada una de las 53 especies en datos/processed/train/, escoge la
imagen mas representativa (mayor calidad estimada por resolucion +
nitidez + brillo medio) y la copia redimensionada (ancho 600 px, alto
proporcional) a codigo/pytorch/app_flask/static/img/species/{ESPECIE}.jpg

Esto alimenta la pagina "Species Guide" de la GUI Flask, que ya espera
imagenes con esa convencion de nombre.

Uso:
    python seleccionar_imagenes_galeria.py
    python seleccionar_imagenes_galeria.py --width 800
    python seleccionar_imagenes_galeria.py --force        # sobreescribe existentes
    python seleccionar_imagenes_galeria.py --source datos/raw  # otra carpeta fuente
    python seleccionar_imagenes_galeria.py --quick        # solo escoge el archivo mas grande, sin scoring

Dependencias: Pillow (incluido en environment.yml).

Autor: Brian Fernandez Baez - mayo 2026
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable

try:
    from PIL import Image, ImageStat, ImageFilter
except ImportError:
    print("ERROR: falta Pillow. Instala con:  pip install Pillow")
    sys.exit(1)

VALID_EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


# ---------------------------------------------------------------------------
def score_image(path: Path) -> float:
    """Devuelve un score 0-100 estimando calidad de la imagen.

    Combina: resolucion (lado mayor en px), nitidez (varianza del Laplaciano
    aproximada por filtro FIND_EDGES) y brillo medio penalizando muy oscuras
    o quemadas. No es perfecto, pero filtra los miniaturas y los oscuros.
    """
    try:
        with Image.open(path) as im:
            im = im.convert("RGB")
            w, h = im.size
            lado_mayor = max(w, h)

            # Resolucion: max 40 puntos. Premia >= 800px.
            res_score = min(40.0, (lado_mayor / 800.0) * 40.0)

            # Nitidez aproximada: varianza de los bordes (mas alto = mas nitido)
            edges = im.filter(ImageFilter.FIND_EDGES)
            edge_stat = ImageStat.Stat(edges)
            edge_mean = sum(edge_stat.mean) / 3.0
            sharp_score = min(30.0, (edge_mean / 25.0) * 30.0)

            # Brillo: max 30. Premia rango 70-180 (de 0-255). Penaliza extremos.
            stat = ImageStat.Stat(im)
            brillo = sum(stat.mean) / 3.0
            if 70 <= brillo <= 180:
                br_score = 30.0
            elif 50 <= brillo < 70 or 180 < brillo <= 210:
                br_score = 20.0
            else:
                br_score = 5.0

            return res_score + sharp_score + br_score
    except Exception as e:
        print(f"  WARNING: no pude leer {path.name}: {e}")
        return -1.0


# ---------------------------------------------------------------------------
def quick_pick(files: Iterable[Path]) -> Path | None:
    """Devuelve el archivo mas grande por bytes."""
    files = list(files)
    if not files:
        return None
    return max(files, key=lambda p: p.stat().st_size)


# ---------------------------------------------------------------------------
def best_pick(files: Iterable[Path], muestreo: int = 30) -> Path | None:
    """Score un subconjunto de hasta `muestreo` imagenes y devuelve la mejor.

    Muestreamos por bytes (top-N mas pesadas) para evitar evaluar cientos
    de imagenes pequenas/duplicadas. Suele ser un buen proxy de calidad.
    """
    files = sorted(files, key=lambda p: p.stat().st_size, reverse=True)
    if not files:
        return None
    candidatas = files[: max(1, muestreo)]
    if len(candidatas) == 1:
        return candidatas[0]
    scored = [(score_image(p), p) for p in candidatas]
    scored = [(s, p) for s, p in scored if s >= 0]
    if not scored:
        return candidatas[0]
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1]


# ---------------------------------------------------------------------------
def listar_imagenes(carpeta: Path) -> list[Path]:
    return [p for p in carpeta.iterdir()
            if p.is_file() and p.suffix.lower() in VALID_EXT]


# ---------------------------------------------------------------------------
def procesar(
    source_root: Path,
    dest_root: Path,
    width: int = 600,
    force: bool = False,
    quick: bool = False,
) -> tuple[int, int, list[str]]:
    """Procesa todas las especies. Devuelve (ok, skipped, faltantes)."""
    if not source_root.exists():
        print(f"ERROR: la carpeta fuente {source_root} no existe.")
        sys.exit(1)

    dest_root.mkdir(parents=True, exist_ok=True)

    especies = sorted([d for d in source_root.iterdir() if d.is_dir()])
    if not especies:
        print(f"ERROR: no hay subcarpetas de especie en {source_root}.")
        sys.exit(1)

    ok = 0
    skipped = 0
    faltantes: list[str] = []

    for i, sp_dir in enumerate(especies, start=1):
        sp_name = sp_dir.name
        dest = dest_root / f"{sp_name}.jpg"

        if dest.exists() and not force:
            print(f"  [{i:>2}/{len(especies)}] SKIP {sp_name:<32} (ya existe)")
            skipped += 1
            continue

        files = listar_imagenes(sp_dir)
        if not files:
            print(f"  [{i:>2}/{len(especies)}] FALTA {sp_name:<32} (sin imagenes)")
            faltantes.append(sp_name)
            continue

        picker = quick_pick if quick else best_pick
        elegida = picker(files)
        if elegida is None:
            faltantes.append(sp_name)
            continue

        try:
            with Image.open(elegida) as im:
                im = im.convert("RGB")
                w, h = im.size
                if w > width:
                    nuevo_h = int(h * (width / w))
                    im = im.resize((width, nuevo_h), Image.LANCZOS)
                im.save(dest, "JPEG", quality=88, optimize=True)
            n = len(files)
            print(f"  [{i:>2}/{len(especies)}] OK   {sp_name:<32} "
                  f"({n:>4} imgs - elegida: {elegida.name[:30]})")
            ok += 1
        except Exception as e:
            print(f"  [{i:>2}/{len(especies)}] FAIL {sp_name:<32} ({e})")
            faltantes.append(sp_name)

    return ok, skipped, faltantes


# ---------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(
        description="Selecciona y copia una imagen por especie a la galeria de la GUI Flask.")
    ap.add_argument("--source", default="datos/processed/train",
                    help="Carpeta fuente con subcarpetas por especie "
                         "(default: datos/processed/train)")
    ap.add_argument("--dest", default="codigo/pytorch/app_flask/static/img/species",
                    help="Carpeta destino para las galerias (default: app_flask/static/img/species)")
    ap.add_argument("--width", type=int, default=600,
                    help="Ancho objetivo en pixeles (default: 600)")
    ap.add_argument("--force", action="store_true",
                    help="Sobreescribir imagenes existentes en destino")
    ap.add_argument("--quick", action="store_true",
                    help="Modo rapido: escoge la imagen mas grande por bytes sin score")
    args = ap.parse_args()

    source = Path(args.source).resolve()
    dest = Path(args.dest).resolve()

    print(f"\n=== Galeria de especies para la Species Guide ===\n")
    print(f"Fuente:  {source}")
    print(f"Destino: {dest}")
    print(f"Ancho:   {args.width} px   Modo: "
          f"{'QUICK (bytes)' if args.quick else 'BEST (score)'}   "
          f"Force: {args.force}\n")

    ok, skipped, faltantes = procesar(
        source, dest, width=args.width, force=args.force, quick=args.quick)

    print(f"\n=== Resumen ===")
    print(f"  Procesadas OK   : {ok}")
    print(f"  Saltadas        : {skipped}  (ya existian; usa --force para regenerar)")
    print(f"  Sin imagen      : {len(faltantes)}")
    if faltantes:
        print(f"  Faltantes       : {', '.join(faltantes)}")
        print(f"\n  Tip: para esas especies necesitas descargar mas imagenes con")
        print(f"       descargar_v1_1.bat <CODE>  o  descargar_v1_1.bat raras")


if __name__ == "__main__":
    main()
