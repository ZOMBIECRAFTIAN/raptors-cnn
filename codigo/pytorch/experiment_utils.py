"""Small helpers for experiment traceability."""
from __future__ import annotations

import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp"}


def git_commit(project_root: Path) -> str:
    """Return the short git commit, or 'unknown' outside a git checkout."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"


def dataset_counts(processed_dir: Path) -> dict:
    """Count image files by split and species."""
    out = {}
    for split in ("train", "val", "test"):
        split_dir = processed_dir / split
        species_counts = {}
        if split_dir.exists():
            for species_dir in sorted(p for p in split_dir.iterdir() if p.is_dir()):
                count = sum(
                    1 for p in species_dir.iterdir()
                    if p.is_file() and p.suffix.lower() in IMAGE_EXTS
                )
                species_counts[species_dir.name] = count
        out[split] = {
            "total": sum(species_counts.values()),
            "species": species_counts,
        }
    return out


def runtime_metadata(project_root: Path, processed_dir: Path) -> dict:
    """Collect lightweight metadata for reproducible experiment reports."""
    return {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_commit(project_root),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "dataset_counts": dataset_counts(processed_dir),
    }


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                    encoding="utf-8")
