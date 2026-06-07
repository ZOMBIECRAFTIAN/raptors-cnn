"""Evaluate a trained YOLO detector and export metrics JSON."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import config


def _ultralytics_device(device: str | None):
    if device is None:
        return None
    value = str(device).lower()
    if value == "cuda":
        return "0"
    if value.startswith("cuda:"):
        return value.split(":", 1)[1]
    return value


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Evaluate YOLO detector")
    p.add_argument("--data", required=True, help="Path to YOLO dataset YAML")
    p.add_argument("--weights", default=str(config.OUTPUT_DIR / "yolo" / "checkpoints" / "best.pt"))
    p.add_argument("--imgsz", type=int, default=640)
    p.add_argument("--device", default=None)
    p.add_argument("--output", default=str(config.OUTPUT_DIR / "yolo" / "metrics_yolo.json"))
    return p.parse_args()


def main() -> None:
    args = parse_args()
    try:
        from ultralytics import YOLO
    except Exception as exc:
        raise SystemExit(
            "Ultralytics is missing. Install with: "
            "pip install -r codigo/pytorch/requirements-yolo.txt"
        ) from exc

    model = YOLO(args.weights)
    metrics = model.val(
        data=str(Path(args.data)),
        imgsz=args.imgsz,
        device=_ultralytics_device(args.device or str(config.DEVICE)),
        project=str(config.OUTPUT_DIR / "yolo" / "val"),
        name="eval",
        exist_ok=True,
    )

    box = getattr(metrics, "box", None)
    payload = {
        "weights": args.weights,
        "data": args.data,
        "imgsz": args.imgsz,
        "map50_95": float(getattr(box, "map", 0.0) or 0.0),
        "map50": float(getattr(box, "map50", 0.0) or 0.0),
        "map75": float(getattr(box, "map75", 0.0) or 0.0),
        "precision": float(getattr(box, "mp", 0.0) or 0.0),
        "recall": float(getattr(box, "mr", 0.0) or 0.0),
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))
    print(f"Saved: {output}")


if __name__ == "__main__":
    main()
