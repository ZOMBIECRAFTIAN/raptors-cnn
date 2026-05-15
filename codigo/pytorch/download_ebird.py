"""
Cliente eBird API 2.0 para obtener metadatos de observaciones.

eBird NO sirve imagenes directamente (las fotos viven en Macaulay Library),
pero su API gratuita ofrece datos extremadamente utiles para la tesis:

    - Codigos de especie estandarizados (ej. "buwhaw" = Broad-winged Hawk)
    - Observaciones recientes en una region (ej. Veracruz, MX-VER)
    - Hotspots de observacion ranked por actividad
    - Estadisticas de abundancia por mes/temporada
    - Verificacion taxonomica oficial

Este script genera un CSV con observaciones recientes de cada una de las
14 especies del proyecto, util para:

    - Validar que el dataset cubra zonas donde la especie realmente esta
    - Mapear hotspots (Cardel, Chichicaxtle, otros sitios)
    - Comparar abundancia entre especies (apoyo al Cap. 4)
    - Cruzar con el dataset descargado de iNaturalist

REQUIERE:
    1. Crear archivo .env en la raiz del proyecto con:
           EBIRD_API_KEY=tu_key_real
    2. pip install python-dotenv requests pandas

USO:
    conda activate raptors-pt
    cd codigo\\pytorch
    python download_ebird.py --region MX-VER --days 30
    python download_ebird.py --region MX-VER --species OS --days 90
"""
import argparse
import csv
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

import config

API_BASE = "https://api.ebird.org/v2"

# Codigos eBird (4-7 letras) por nombre cientifico. eBird usa codigos
# alfanumericos estandarizados que NO coinciden con nuestros codigos
# internos de dos letras (BW, SS, etc.). Esta tabla hace la traduccion.
EBIRD_SPECIES_CODES = {
    "Accipiter_striatus":       "shshaw",   # Sharp-shinned Hawk
    "Astur_cooperii":           "coohaw",   # Cooper's Hawk
    "Buteo_albonotatus":        "zotaw1",   # Zone-tailed Hawk (eBird usa zotaw1, no zothaw1)
    "Buteo_jamaicensis":        "rethaw",   # Red-tailed Hawk
    "Buteo_lineatus":           "reshaw",   # Red-shouldered Hawk
    "Buteo_platypterus":        "brwhaw",   # Broad-winged Hawk
    "Buteo_swainsoni":          "swahaw",   # Swainson's Hawk
    "Cathartes_aura":           "turvul",   # Turkey Vulture
    "Circus_hudsonius":         "norhar2",  # Northern Harrier
    "Falco_columbarius":        "merlin",   # Merlin
    "Falco_peregrinus":         "perfal",   # Peregrine Falcon
    "Falco_sparverius":         "amekes",   # American Kestrel
    "Ictinia_mississippiensis": "miskit",   # Mississippi Kite
    "Pandion_haliaetus":        "osprey",   # Osprey
}


def get_api_key() -> str:
    """Carga la API key desde .env o falla con error claro."""
    load_dotenv(config.PROJECT_ROOT / ".env")
    key = os.getenv("EBIRD_API_KEY", "").strip()
    if not key or key == "tu_api_key_aqui":
        print("[ERROR] No se encontro EBIRD_API_KEY en .env", file=sys.stderr)
        print("       Crea el archivo .env (basado en .env.example) y agrega:", file=sys.stderr)
        print("           EBIRD_API_KEY=tu_key_real", file=sys.stderr)
        print("       Obten una key gratis en https://ebird.org/api/keygen", file=sys.stderr)
        sys.exit(1)
    return key


def ebird_get(endpoint: str, api_key: str, params: dict | None = None) -> list | dict:
    """Hace request a la API de eBird con la key en el header."""
    headers = {"X-eBirdApiToken": api_key}
    r = requests.get(f"{API_BASE}{endpoint}", headers=headers, params=params or {}, timeout=60)
    r.raise_for_status()
    return r.json()


def recent_observations(region: str, species_code: str, days: int, api_key: str) -> list[dict]:
    """Observaciones recientes de una especie en una region (max 30 dias)."""
    return ebird_get(
        f"/data/obs/{region}/recent/{species_code}",
        api_key,
        {"back": min(days, 30), "includeProvisional": "false"},
    )


def hotspots_in_region(region: str, api_key: str) -> list[dict]:
    """Hotspots de eBird en una region."""
    return ebird_get(f"/ref/hotspot/{region}", api_key, {"fmt": "json"})


def write_csv(rows: list[dict], path: Path, fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fieldnames})


def main():
    parser = argparse.ArgumentParser(description="eBird API client para el proyecto raptors-cnn")
    parser.add_argument("--region", default="MX-VER",
                        help="Codigo eBird de region (default MX-VER = Veracruz)")
    parser.add_argument("--days", type=int, default=30,
                        help="Cuantos dias hacia atras (max 30, default 30)")
    parser.add_argument("--species", default=None,
                        help="Solo una especie (codigo interno de 2 letras: BW, TV, etc.). Default: todas")
    parser.add_argument("--hotspots", action="store_true",
                        help="Adicionalmente descarga el listado de hotspots de la region")
    args = parser.parse_args()

    api_key = get_api_key()
    print(f"[ok] API key cargada desde .env (longitud {len(api_key)})")

    # Filtrar especies a consultar
    code_to_sci = dict(zip(config.SPECIES_CODE, config.SPECIES))
    if args.species:
        if args.species not in code_to_sci:
            print(f"[error] codigo desconocido: {args.species}")
            print(f"        opciones: {list(code_to_sci)}")
            sys.exit(1)
        species_to_query = [(args.species, code_to_sci[args.species])]
    else:
        species_to_query = list(code_to_sci.items())

    out_dir = config.ANNOTATIONS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / f"ebird_observations_{args.region}.csv"

    # Cabecera del CSV
    fieldnames = [
        "species_code_internal", "scientific_name", "ebird_code",
        "comName", "obsDt", "howMany", "lat", "lng",
        "locName", "locId", "subnational1Code", "obsValid", "obsReviewed",
    ]

    all_rows = []
    for code, sci in species_to_query:
        ebird_code = EBIRD_SPECIES_CODES.get(sci)
        if not ebird_code:
            print(f"  [warn] sin codigo eBird para {sci}, saltando")
            continue
        print(f"\n  > {code} ({sci}, eBird: {ebird_code}) en {args.region} ultimos {args.days} dias...")
        try:
            obs = recent_observations(args.region, ebird_code, args.days, api_key)
            print(f"    {len(obs)} observaciones encontradas")
            for o in obs:
                o["species_code_internal"] = code
                o["scientific_name"] = sci
                o["ebird_code"] = ebird_code
                all_rows.append(o)
        except requests.HTTPError as e:
            print(f"    [error] {e}")
        time.sleep(0.6)

    write_csv(all_rows, csv_path, fieldnames)
    print(f"\n[ok] Total observaciones guardadas: {len(all_rows)} -> {csv_path}")

    # Hotspots (opcional)
    if args.hotspots:
        print(f"\n  > Descargando hotspots de {args.region}...")
        hotspots = hotspots_in_region(args.region, api_key)
        hotspot_path = out_dir / f"ebird_hotspots_{args.region}.csv"
        hotspot_fields = ["locId", "locName", "lat", "lng", "subnational1Code",
                          "numSpeciesAllTime", "latestObsDt"]
        write_csv(hotspots, hotspot_path, hotspot_fields)
        print(f"    {len(hotspots)} hotspots guardados -> {hotspot_path}")


if __name__ == "__main__":
    main()
