"""
Descargador de imágenes de iNaturalist para las 14 especies del proyecto.

Usa la API pública de iNaturalist (no requiere autenticación) para descargar
imágenes etiquetadas con grado de investigación (`research-grade`) y bajo
licencias compatibles con uso académico abierto.

Uso típico:
    conda activate raptors-pt
    cd codigo\pytorch
    python download_inaturalist.py --target 250 --max-pages 5

Argumentos:
    --target N       Cuántas imágenes objetivo por especie (default 250).
    --max-pages N    Hasta cuántas páginas de la API consultar por especie (default 5).
    --species CODE   Solo descargar una especie (ej. BW, TV). Default: todas las 14.
    --licenses ...   Lista de licencias permitidas. Default: cc0 cc-by cc-by-sa.
    --dry-run        Solo lista qué descargaría, no descarga nada.

Output:
    datos/raw/<scientific_name>/<inat_id>_<photo_id>.jpg
    datos/annotations/inaturalist_metadata.csv
"""
import argparse
import csv
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import requests

import config

API = "https://api.inaturalist.org/v1"
HEADERS = {"User-Agent": "raptors-cnn-thesis (academic use; brianferbaez@gmail.com)"}

# Licencias compatibles con uso académico abierto. iNat usa códigos en minúsculas.
DEFAULT_LICENSES = ["cc0", "cc-by", "cc-by-sa"]

# Mapeo código → nombre científico (importado desde config para mantener una sola
# fuente de verdad)
CODE_TO_SCI = dict(zip(config.SPECIES_CODE, config.SPECIES))


def lookup_taxon_id(scientific_name: str) -> int:
    """Resuelve un nombre científico a su taxon_id en iNaturalist."""
    name_query = scientific_name.replace("_", " ")
    r = requests.get(
        f"{API}/taxa",
        params={"q": name_query, "rank": "species", "per_page": 5},
        headers=HEADERS,
        timeout=30,
    )
    r.raise_for_status()
    for taxon in r.json().get("results", []):
        if taxon.get("name", "").lower() == name_query.lower():
            return int(taxon["id"])
    raise ValueError(f"No se encontró taxon_id para {scientific_name}")


def search_observations(taxon_id: int, page: int, per_page: int, licenses: list[str]) -> dict:
    """Busca observaciones research-grade con foto y licencia compatible."""
    r = requests.get(
        f"{API}/observations",
        params={
            "taxon_id": taxon_id,
            "quality_grade": "research",
            "photos": "true",
            "page": page,
            "per_page": per_page,
            "order": "votes",
            "order_by": "votes",
            "photo_license": ",".join(licenses),
        },
        headers=HEADERS,
        timeout=60,
    )
    r.raise_for_status()
    return r.json()


def download_image(url: str, dest: Path) -> bool:
    """Descarga la URL al destino. Devuelve True si tuvo éxito."""
    try:
        with requests.get(url, headers=HEADERS, stream=True, timeout=60) as r:
            r.raise_for_status()
            dest.parent.mkdir(parents=True, exist_ok=True)
            with open(dest, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return True
    except Exception as e:
        print(f"    [warn] error descargando {url}: {e}", file=sys.stderr)
        return False


def upgrade_url(url: str) -> str:
    """iNaturalist sirve thumbnails por defecto. Subimos a 'large' para mejor calidad."""
    return url.replace("/square.", "/large.").replace("/medium.", "/large.").replace("/thumb.", "/large.")


def download_for_species(
    species_code: str, scientific_name: str, target: int, max_pages: int,
    licenses: list[str], raw_dir: Path, csv_writer, dry_run: bool,
) -> int:
    """Descarga hasta `target` imágenes para una especie."""
    print(f"\n  ▸ {species_code}  {scientific_name}  → objetivo: {target} imágenes")
    try:
        taxon_id = lookup_taxon_id(scientific_name)
    except ValueError as e:
        print(f"    [error] {e}")
        return 0
    print(f"    taxon_id = {taxon_id}")

    species_dir = raw_dir / scientific_name
    downloaded = 0
    skipped = 0

    for page in range(1, max_pages + 1):
        if downloaded >= target:
            break
        data = search_observations(taxon_id, page=page, per_page=100, licenses=licenses)
        results = data.get("results", [])
        if not results:
            print(f"    página {page}: sin resultados, fin")
            break

        for obs in results:
            if downloaded >= target:
                break
            obs_id = obs["id"]
            obs_url = f"https://www.inaturalist.org/observations/{obs_id}"
            user = obs.get("user", {})
            user_login = user.get("login", "unknown")

            for photo in obs.get("photos", []):
                if downloaded >= target:
                    break
                photo_id = photo.get("id")
                photo_license = photo.get("license_code", "unknown")
                if photo_license not in licenses:
                    skipped += 1
                    continue

                url = upgrade_url(photo.get("url", ""))
                if not url:
                    continue

                ext = Path(urlparse(url).path).suffix or ".jpg"
                filename = f"{obs_id}_{photo_id}{ext}"
                dest = species_dir / filename

                if dest.exists():
                    skipped += 1
                    continue

                if dry_run:
                    print(f"    [dry] {filename}  ({photo_license})  by {user_login}")
                    downloaded += 1
                    continue

                ok = download_image(url, dest)
                if ok:
                    csv_writer.writerow({
                        "filename": str(dest.relative_to(raw_dir.parent)),
                        "species_code": species_code,
                        "scientific_name": scientific_name,
                        "source": "inaturalist",
                        "license": photo_license,
                        "photographer": user_login,
                        "observation_id": obs_id,
                        "observation_url": obs_url,
                        "photo_id": photo_id,
                        "url": url,
                    })
                    downloaded += 1
                    if downloaded % 25 == 0:
                        print(f"    progreso: {downloaded}/{target}")
                # respeta los límites de la API de iNat (60 req/min recomendado)
                time.sleep(0.6)

    print(f"    ✓ {species_code}: descargadas {downloaded}, omitidas {skipped}")
    return downloaded


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=250,
                        help="imágenes objetivo por especie (default 250)")
    parser.add_argument("--max-pages", type=int, default=5,
                        help="máximo de páginas API por especie (default 5)")
    parser.add_argument("--species", type=str, default=None,
                        help="solo una especie por código (BW, TV, etc.). Default: todas")
    parser.add_argument("--licenses", nargs="+", default=DEFAULT_LICENSES,
                        help=f"licencias permitidas (default {' '.join(DEFAULT_LICENSES)})")
    parser.add_argument("--dry-run", action="store_true",
                        help="solo lista qué descargaría, no descarga nada")
    args = parser.parse_args()

    raw_dir = config.RAW_DIR
    raw_dir.mkdir(parents=True, exist_ok=True)
    annotations_dir = config.ANNOTATIONS_DIR
    annotations_dir.mkdir(parents=True, exist_ok=True)
    csv_path = annotations_dir / "inaturalist_metadata.csv"

    # Si el CSV ya existe, abrimos en modo append; si no, escribimos cabecera.
    write_header = not csv_path.exists()
    fieldnames = [
        "filename", "species_code", "scientific_name", "source", "license",
        "photographer", "observation_id", "observation_url", "photo_id", "url",
    ]

    print(f"Descargando imágenes a: {raw_dir}")
    print(f"Metadatos: {csv_path}")
    print(f"Licencias permitidas: {args.licenses}")
    print(f"Objetivo por especie: {args.target}")
    if args.dry_run:
        print("⚡ DRY RUN — no se descarga nada, solo se listan candidatos.")

    species_to_do = []
    if args.species:
        if args.species not in CODE_TO_SCI:
            print(f"[error] código de especie desconocido: {args.species}")
            print(f"        opciones: {' '.join(CODE_TO_SCI)}")
            return
        species_to_do = [(args.species, CODE_TO_SCI[args.species])]
    else:
        species_to_do = list(CODE_TO_SCI.items())

    total = 0
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        for code, sci in species_to_do:
            n = download_for_species(
                species_code=code, scientific_name=sci,
                target=args.target, max_pages=args.max_pages,
                licenses=args.licenses, raw_dir=raw_dir,
                csv_writer=writer, dry_run=args.dry_run,
            )
            total += n

    print(f"\n✅ Total descargado: {total} imágenes a {raw_dir}")


if __name__ == "__main__":
    main()
