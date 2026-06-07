"""Train a YOLO detector for the raptors-cnn video module.

Expected dataset format: standard Ultralytics YOLO data YAML with train/val
image folders and label TXT files. See codigo/pytorch/yolo/dataset_template.yaml.
"""
from __future__ import annotations

import argparse
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
    p = argparse.ArgumentParser(description="Train YOLO detector for raptor videos")
    p.add_argument("--data", required=True, help="Path to YOLO dataset YAML")
    p.add_argument("--model", default="yolov8n.pt",
                   help="Base YOLO weights, e.g. yolov8n.pt or yolo11n.pt")
    p.add_argument("--epochs", type=int, default=80)
    p.add_argument("--imgsz", type=int, default=640)
    p.add_argument("--batch", type=int, default=8)
    p.add_argument("--device", default=None,
                   help="cuda, 0, cpu, mps; defaults to config.DEVICE")
    p.add_argument("--name", default="raptors_yolo_detector")
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

    project = config.OUTPUT_DIR / "yolo" / "runs"
    model = YOLO(args.model)
    model.train(
        data=str(Path(args.data)),
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=_ultralytics_device(args.device or str(config.DEVICE)),
        project=str(project),
        name=args.name,
        exist_ok=True,
    )
    print(f"YOLO training finished. Runs written to: {project / args.name}")
    print("Copy the best checkpoint to:")
    print(config.OUTPUT_DIR / "yolo" / "checkpoints" / "best.pt")


if __name__ == "__main__":
    main()
