"""Audit the raptors-cnn dataset before training or reporting metrics.

This script is intentionally conservative: it does not modify files. It checks
the processed split for observation leakage, per-species support, unsupported
files and optional image readability. Outputs are written under
codigo/pytorch/outputs/audits/ so they stay local and reproducible.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

from PIL import Image, UnidentifiedImageError

import config


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp"}
EXTRA_MEDIA_EXTS = {".gif"}
SPLITS = ("train", "val", "test")


def observation_id(path: Path) -> str:
    """Extract observationID from <observationID>_<photoID> filenames."""
    first = path.stem.split("_", 1)[0]
    return first if first else path.stem


def iter_files(root: Path):
    if root.exists():
        yield from (p for p in root.rglob("*") if p.is_file())


def is_image(path: Path) -> bool:
    return path.suffix.lower() in IMAGE_EXTS


def audit_processed(processed_dir: Path, check_images: bool = False) -> dict:
    counts = {
        split: {species: 0 for species in config.SPECIES}
        for split in SPLITS
    }
    obs_by_split: dict[str, dict[str, set[str]]] = {
        split: defaultdict(set) for split in SPLITS
    }
    unsupported = []
    corrupt = []
    non_numeric_obs = []

    for split in SPLITS:
        split_dir = processed_dir / split
        for file_path in iter_files(split_dir):
            suffix = file_path.suffix.lower()
            if suffix not in IMAGE_EXTS:
                unsupported.append(str(file_path))
                continue
            species = file_path.parent.name
            if species not in counts[split]:
                counts[split][species] = 0
            counts[split][species] += 1
            obs = observation_id(file_path)
            obs_by_split[split][species].add(obs)
            if not obs.isdigit():
                non_numeric_obs.append(str(file_path))
            if check_images:
                try:
                    with Image.open(file_path) as img:
                        img.verify()
                except (OSError, UnidentifiedImageError):
                    corrupt.append(str(file_path))

    overlaps = {}
    for a, b in (("train", "val"), ("train", "test"), ("val", "test")):
        pair_key = f"{a}_{b}"
        overlaps[pair_key] = {}
        for species in config.SPECIES:
            left = obs_by_split[a].get(species, set())
            right = obs_by_split[b].get(species, set())
            shared = sorted(left & right)
            if shared:
                overlaps[pair_key][species] = {
                    "count": len(shared),
                    "examples": shared[:20],
                }

    rare_species = []
    for species in config.SPECIES:
        row = {
            "species": species,
            "train": counts["train"].get(species, 0),
            "val": counts["val"].get(species, 0),
            "test": counts["test"].get(species, 0),
        }
        if row["train"] < 50 or row["val"] < 10 or row["test"] < 10:
            rare_species.append(row)

    leak_summary = {
        pair: sum(item["count"] for item in species_map.values())
        for pair, species_map in overlaps.items()
    }

    return {
        "processed_dir": str(processed_dir),
        "counts": counts,
        "totals": {
            split: sum(counts[split].values()) for split in SPLITS
        },
        "observation_overlap_by_pair": leak_summary,
        "observation_overlap_detail": overlaps,
        "rare_species_threshold": "train<50 or val<10 or test<10",
        "rare_species": rare_species,
        "unsupported_files": unsupported,
        "non_numeric_observation_ids": non_numeric_obs[:200],
        "corrupt_images": corrupt,
        "check_images": check_images,
    }


def audit_raw(raw_dir: Path) -> dict:
    gifs = []
    unsupported = []
    for file_path in iter_files(raw_dir):
        suffix = file_path.suffix.lower()
        if suffix in EXTRA_MEDIA_EXTS:
            gifs.append(str(file_path))
        elif suffix not in IMAGE_EXTS and suffix not in EXTRA_MEDIA_EXTS:
            unsupported.append(str(file_path))
    return {
        "raw_dir": str(raw_dir),
        "gif_count": len(gifs),
        "gif_examples": gifs[:50],
        "unsupported_files": unsupported[:200],
    }


def write_species_counts_csv(audit: dict, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["species", "train", "val", "test", "total"],
        )
        writer.writeheader()
        counts = audit["counts"]
        for species in config.SPECIES:
            train = counts["train"].get(species, 0)
            val = counts["val"].get(species, 0)
            test = counts["test"].get(species, 0)
            writer.writerow({
                "species": species,
                "train": train,
                "val": val,
                "test": test,
                "total": train + val + test,
            })


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--processed-dir", type=Path, default=config.PROCESSED_DIR)
    parser.add_argument("--raw-dir", type=Path, default=config.RAW_DIR)
    parser.add_argument("--check-images", action="store_true",
                        help="Open every processed image to detect corrupt files")
    parser.add_argument("--fail-on-leak", action="store_true",
                        help="Exit with status 2 when observation leakage exists")
    parser.add_argument("--output-dir", type=Path,
                        default=config.OUTPUT_DIR / "audits")
    args = parser.parse_args()

    processed_audit = audit_processed(args.processed_dir, args.check_images)
    raw_audit = audit_raw(args.raw_dir)
    payload = {
        "processed": processed_audit,
        "raw": raw_audit,
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / "dataset_audit.json"
    csv_path = args.output_dir / "dataset_species_counts.csv"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                         encoding="utf-8")
    write_species_counts_csv(processed_audit, csv_path)

    print("Dataset audit")
    print(f"Processed totals: {processed_audit['totals']}")
    print(f"Observation overlap: {processed_audit['observation_overlap_by_pair']}")
    print(f"Rare/low-support species: {len(processed_audit['rare_species'])}")
    print(f"Unsupported processed files: {len(processed_audit['unsupported_files'])}")
    print(f"Raw GIF files: {raw_audit['gif_count']}")
    print(f"JSON: {json_path}")
    print(f"CSV:  {csv_path}")

    has_leak = any(
        count > 0
        for count in processed_audit["observation_overlap_by_pair"].values()
    )
    if args.fail_on_leak and has_leak:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
