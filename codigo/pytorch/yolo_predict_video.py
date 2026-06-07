"""Run YOLO video analysis from the command line."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import config
from yolo.video_pipeline import analyze_video


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Analyze a video with YOLO")
    p.add_argument("--video", required=True, help="Path to MP4/MOV/WEBM video")
    p.add_argument("--weights", default=None,
                   help="YOLO weights. Defaults to RAPTORS_YOLO_WEIGHTS, custom best.pt, or yolov8n.pt")
    p.add_argument("--sample-every", type=float, default=1.0)
    p.add_argument("--max-frames", type=int, default=60)
    p.add_argument("--conf", type=float, default=0.35)
    p.add_argument("--imgsz", type=int, default=640)
    p.add_argument("--output-dir", default=str(config.OUTPUT_DIR / "yolo" / "video_analysis"))
    return p.parse_args()


def main() -> None:
    args = parse_args()
    payload = analyze_video(
        args.video,
        yolo_weights=args.weights,
        output_dir=args.output_dir,
        device=str(config.DEVICE),
        sample_every_s=args.sample_every,
        max_frames=args.max_frames,
        conf=args.conf,
        imgsz=args.imgsz,
    )
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"Saved outputs in: {Path(args.output_dir)}")


if __name__ == "__main__":
    main()
