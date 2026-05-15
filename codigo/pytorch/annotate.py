"""
annotate.py — Herramienta CLI para anotación doble + cálculo Cohen kappa.

Flujo recomendado:
  1) Anotador 1 corre:  python annotate.py --annotator alice
  2) Anotador 2 corre:  python annotate.py --annotator bob
  3) Comparar:          python annotate.py --compare alice bob

La herramienta abre cada imagen (subprocess que llama al visor del sistema) y
pide en consola:
  Enter / k = keep (especie correcta)
  d = discard (no apta — posada, baja calidad, otra ave)
  c = cambiar etiqueta a otra especie del proyecto
  s = skip por ahora
  q = quit y guardar progreso

Las decisiones se guardan en datos/annotations/<annotator>.csv y se pueden
reanudar — solo se muestran imágenes no anotadas.

Cuando comparas dos anotadores, calcula κ de Cohen y muestra las discrepancias.
"""
from __future__ import annotations
import argparse
import csv
import subprocess
import sys
from pathlib import Path
from typing import Optional

import config


# Imágenes a anotar: prioridad a las "KEEP" del curation_report.csv;
# si no existe ese reporte, anotar todas las de datos/raw/<especie>/.
def candidate_images(species: Optional[str] = None) -> list[tuple[str, Path]]:
    """Devuelve [(scientific_name, image_path), ...]."""
    raw = config.RAW_DIR
    curation = config.ANNOTATIONS_DIR / "curation_report.csv"
    species_list = [species] if species else config.SPECIES

    items = []
    if curation.exists():
        with open(curation, "r", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                sp = row["species"]
                if species and sp != species:
                    continue
                if row["decision"] in ("KEEP", "REVIEW"):
                    img = raw / sp / row["filename"]
                    if img.exists():
                        items.append((sp, img))
    else:
        # Fallback: todas las imágenes
        for sp in species_list:
            for img in (raw / sp).glob("*.jpg"):
                items.append((sp, img))

    return items


def open_image(path: Path) -> None:
    """Abre la imagen con el visor del sistema."""
    if sys.platform == "win32":
        subprocess.Popen(["start", "", str(path)], shell=True)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", str(path)])
    else:
        subprocess.Popen(["xdg-open", str(path)])


def load_existing(annot_file: Path) -> dict:
    """Carga decisiones previas (clave: filename)."""
    if not annot_file.exists():
        return {}
    out = {}
    with open(annot_file, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[row["filename"]] = row
    return out


def append_row(annot_file: Path, row: dict, fieldnames: list[str]) -> None:
    new = not annot_file.exists()
    annot_file.parent.mkdir(parents=True, exist_ok=True)
    with open(annot_file, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        if new: w.writeheader()
        w.writerow(row)


def annotate(annotator: str, species: Optional[str]) -> None:
    """Loop interactivo de anotación."""
    annot_file = config.ANNOTATIONS_DIR / f"{annotator}.csv"
    fieldnames = ["filename", "species_original", "decision", "species_final", "notes"]

    existing = load_existing(annot_file)
    items = candidate_images(species)
    pending = [(sp, p) for sp, p in items if p.name not in existing]

    print(f"\n  Anotador: {annotator}")
    print(f"  Ya anotaste: {len(existing)} imágenes")
    print(f"  Pendientes : {len(pending)}\n")
    if not pending:
        print("  ¡No hay nada pendiente!")
        return

    species_codes = config.SPECIES_CODE
    species_full = config.SPECIES

    for i, (sp, img_path) in enumerate(pending, start=1):
        print(f"\n────────────────────────────────────────")
        print(f"  [{i}/{len(pending)}] {img_path.name}")
        print(f"  Especie sugerida: {sp}")
        print(f"  Abriendo imagen...")
        open_image(img_path)

        while True:
            opt = input("\n  Opciones: [Enter]=keep · d=discard · c=cambiar · s=skip · q=quit : ").strip().lower()

            if opt in ("", "k", "keep"):
                row = dict(filename=img_path.name, species_original=sp,
                           decision="KEEP", species_final=sp, notes="")
                break
            if opt in ("d", "discard"):
                note = input("  Motivo (posada/borrosa/otra_especie/etc): ").strip()
                row = dict(filename=img_path.name, species_original=sp,
                           decision="DISCARD", species_final="", notes=note)
                break
            if opt in ("c", "change"):
                print("  Códigos disponibles: " + " ".join(species_codes))
                code = input("  Nuevo código (2 letras): ").strip().upper()
                if code in species_codes:
                    new_sp = species_full[species_codes.index(code)]
                    row = dict(filename=img_path.name, species_original=sp,
                               decision="RELABEL", species_final=new_sp,
                               notes=f"era {sp}, ahora {new_sp}")
                    break
                print(f"  ⚠ código '{code}' no reconocido. Intenta de nuevo.")
                continue
            if opt in ("s", "skip"):
                row = None
                break
            if opt in ("q", "quit"):
                print("\n  Adiós — tu progreso queda guardado.")
                return
            print("  Opción inválida.")

        if row is not None:
            append_row(annot_file, row, fieldnames)

    print("\n  ✅ Anotación completa.")


def compare(annotator_a: str, annotator_b: str) -> None:
    """Compara dos archivos de anotación y calcula κ de Cohen."""
    from sklearn.metrics import cohen_kappa_score, confusion_matrix

    file_a = config.ANNOTATIONS_DIR / f"{annotator_a}.csv"
    file_b = config.ANNOTATIONS_DIR / f"{annotator_b}.csv"
    if not file_a.exists() or not file_b.exists():
        print(f"  Falta {file_a.name} o {file_b.name}.")
        return

    rows_a = load_existing(file_a)
    rows_b = load_existing(file_b)
    common = sorted(set(rows_a) & set(rows_b))
    print(f"\n  Anotaciones comunes: {len(common)}")

    if not common:
        print("  Sin archivos en común — no se puede comparar.")
        return

    labels_a = [rows_a[f]["species_final"] or rows_a[f]["decision"] for f in common]
    labels_b = [rows_b[f]["species_final"] or rows_b[f]["decision"] for f in common]

    k = cohen_kappa_score(labels_a, labels_b)
    print(f"  κ de Cohen: {k:.4f}")
    if k >= 0.80:
        print("  ✅ acuerdo casi perfecto (≥ 0.80, criterio Cap 3)")
    elif k >= 0.60:
        print("  ⚠️ acuerdo sustancial (0.60-0.80) — revisa discrepancias")
    else:
        print("  ❌ acuerdo bajo (< 0.60) — discusión obligatoria entre anotadores")

    # Reporte de discrepancias
    diffs = [(f, rows_a[f]["species_final"] or rows_a[f]["decision"],
                 rows_b[f]["species_final"] or rows_b[f]["decision"])
             for f in common
             if (rows_a[f]["species_final"] or rows_a[f]["decision"]) !=
                (rows_b[f]["species_final"] or rows_b[f]["decision"])]
    print(f"\n  Discrepancias: {len(diffs)}")
    for fn, a, b in diffs[:20]:
        print(f"    {fn:50s} | {annotator_a}: {a:30s} | {annotator_b}: {b}")
    if len(diffs) > 20:
        print(f"    ... y {len(diffs) - 20} más")

    # Guardar para análisis posterior
    diffs_csv = config.ANNOTATIONS_DIR / f"discrepancies_{annotator_a}_vs_{annotator_b}.csv"
    with open(diffs_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["filename", annotator_a, annotator_b])
        for fn, a, b in diffs: w.writerow([fn, a, b])
    print(f"\n  Discrepancias guardadas en: {diffs_csv}")


def main():
    parser = argparse.ArgumentParser(description="Anotador interactivo + Kappa")
    parser.add_argument("--annotator", help="Nombre del anotador (ej. alice)")
    parser.add_argument("--species", help="Solo una especie (nombre científico con _)")
    parser.add_argument("--compare", nargs=2, metavar=("ANNOTATOR_A", "ANNOTATOR_B"),
                        help="Comparar 2 anotadores y calcular κ")
    args = parser.parse_args()

    if args.compare:
        compare(args.compare[0], args.compare[1])
    elif args.annotator:
        annotate(args.annotator, args.species)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
