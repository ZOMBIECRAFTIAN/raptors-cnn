"""YOLO-based video analysis pipeline for raptors-cnn.

Pipeline:
1. Sample video frames with OpenCV.
2. Detect birds with YOLO.
3. Track detections with a lightweight IoU tracker.
4. Optionally classify each crop with the 53-class CNN.
5. Summarise species and conservative flight-behaviour cues.
"""
from __future__ import annotations

import csv
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable

import cv2
import numpy as np
from PIL import Image

import config
from .behavior import TrackPoint, classify_track, localized_behavior, majority_behavior

ClassifierFn = Callable[[Image.Image], dict]


DEFAULT_OUTPUT_DIR = config.OUTPUT_DIR / "yolo"
DEFAULT_CUSTOM_WEIGHTS = DEFAULT_OUTPUT_DIR / "checkpoints" / "best.pt"
DEFAULT_COCO_WEIGHTS = "yolov8n.pt"


def default_yolo_weights() -> str:
    """Return the preferred YOLO weights for this project."""
    env_path = os.getenv("RAPTORS_YOLO_WEIGHTS")
    if env_path:
        return env_path
    if DEFAULT_CUSTOM_WEIGHTS.exists():
        return str(DEFAULT_CUSTOM_WEIGHTS)
    return DEFAULT_COCO_WEIGHTS


@dataclass
class TrackState:
    track_id: int
    bbox: list[float]
    points: list[TrackPoint] = field(default_factory=list)
    missed: int = 0
    behavior: str = "insufficient_track"


class IouTracker:
    """Small dependency-free tracker for sampled-frame summaries."""

    def __init__(self, iou_threshold: float = 0.20, max_missed: int = 2):
        self.iou_threshold = iou_threshold
        self.max_missed = max_missed
        self._next_id = 1
        self.tracks: dict[int, TrackState] = {}

    def update(
        self,
        detections: list[dict],
        timestamp_s: float,
        frame_width: int,
        frame_height: int,
    ) -> list[dict]:
        assigned_tracks: set[int] = set()
        assigned_dets: set[int] = set()

        pairs: list[tuple[float, int, int]] = []
        for det_idx, det in enumerate(detections):
            for track_id, track in self.tracks.items():
                pairs.append((_iou(det["bbox"], track.bbox), det_idx, track_id))
        pairs.sort(reverse=True, key=lambda x: x[0])

        for score, det_idx, track_id in pairs:
            if score < self.iou_threshold:
                break
            if det_idx in assigned_dets or track_id in assigned_tracks:
                continue
            self._assign(track_id, detections[det_idx], timestamp_s,
                         frame_width, frame_height)
            assigned_dets.add(det_idx)
            assigned_tracks.add(track_id)

        for det_idx, det in enumerate(detections):
            if det_idx in assigned_dets:
                continue
            track_id = self._next_id
            self._next_id += 1
            self.tracks[track_id] = TrackState(track_id=track_id, bbox=det["bbox"])
            self._assign(track_id, det, timestamp_s, frame_width, frame_height)
            assigned_tracks.add(track_id)

        stale = []
        for track_id, track in self.tracks.items():
            if track_id not in assigned_tracks:
                track.missed += 1
            if track.missed > self.max_missed:
                stale.append(track_id)
        for track_id in stale:
            del self.tracks[track_id]

        return detections

    def _assign(
        self,
        track_id: int,
        detection: dict,
        timestamp_s: float,
        frame_width: int,
        frame_height: int,
    ) -> None:
        track = self.tracks[track_id]
        x0, y0, x1, y1 = detection["bbox"]
        cx = (x0 + x1) / 2.0
        cy = (y0 + y1) / 2.0
        area = max(0.0, x1 - x0) * max(0.0, y1 - y0)
        track.bbox = detection["bbox"]
        track.missed = 0
        track.points.append(TrackPoint(timestamp_s, cx, cy, area,
                                       frame_width, frame_height))
        track.behavior = classify_track(track.points)
        detection["track_id"] = track_id
        detection["behavior"] = track.behavior
        detection["behavior_es"] = localized_behavior(track.behavior, "es")
        detection["behavior_en"] = localized_behavior(track.behavior, "en")


def analyze_video(
    video_path: str | Path,
    *,
    yolo_weights: str | Path | None = None,
    classifier_fn: ClassifierFn | None = None,
    output_dir: str | Path | None = None,
    device: str | None = None,
    sample_every_s: float = 1.0,
    max_frames: int = 60,
    conf: float = 0.35,
    iou: float = 0.45,
    imgsz: int = 640,
    class_filter: Iterable[str] | None = None,
) -> dict:
    """Analyse one video and return a JSON-serialisable summary."""
    try:
        from ultralytics import YOLO
    except Exception as exc:
        raise RuntimeError(
            "Ultralytics YOLO is not installed. Install the optional video "
            "dependencies with: pip install -r codigo/pytorch/requirements-yolo.txt"
        ) from exc

    video_path = Path(video_path)
    weights = str(yolo_weights or default_yolo_weights())
    model = YOLO(weights)

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")

    fps = float(cap.get(cv2.CAP_PROP_FPS) or 30.0)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    duration_s = total_frames / fps if fps > 0 else 0.0
    frame_step = max(1, int(round(fps * sample_every_s)))

    tracker = IouTracker()
    timeline: list[dict] = []
    flat_rows: list[dict] = []
    per_species: dict[str, dict] = {}
    per_track_behaviors: dict[int, list[str]] = {}

    frame_idx = 0
    sampled = 0
    next_sample = 0

    try:
        while sampled < max_frames:
            ok, bgr = cap.read()
            if not ok:
                break
            if frame_idx < next_sample:
                frame_idx += 1
                continue

            timestamp_s = frame_idx / fps if fps > 0 else float(sampled)
            frame_h, frame_w = bgr.shape[:2]
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            pil_frame = Image.fromarray(rgb)

            result = model.predict(
                source=rgb,
                conf=conf,
                iou=iou,
                imgsz=imgsz,
                device=_ultralytics_device(device),
                verbose=False,
            )[0]

            detections = _detections_from_result(
                result,
                pil_frame,
                classifier_fn=classifier_fn,
                class_filter=class_filter,
            )
            tracker.update(detections, timestamp_s, frame_w, frame_h)

            for det in detections:
                key = det["species_key"]
                per_species.setdefault(key, {
                    "species_key": key,
                    "common_name": det["common_name"],
                    "scientific": det["scientific"],
                    "color": det["color"],
                    "frames_with_species": 0,
                    "detections": 0,
                    "behaviors": [],
                })
                per_species[key]["frames_with_species"] += 1
                per_species[key]["detections"] += 1
                per_species[key]["behaviors"].append(det["behavior"])
                per_track_behaviors.setdefault(det["track_id"], []).append(det["behavior"])
                flat_rows.append({
                    "t_seconds": round(timestamp_s, 3),
                    "frame_idx": frame_idx,
                    "track_id": det["track_id"],
                    "yolo_class": det["yolo_class"],
                    "bbox_score": det["bbox_score"],
                    "species_key": key,
                    "common_name": det["common_name"],
                    "scientific": det["scientific"],
                    "cnn_confidence": det["confidence"],
                    "behavior": det["behavior"],
                    "bbox": det["bbox"],
                })

            timeline.append({
                "t_seconds": round(timestamp_s, 2),
                "frame_idx": frame_idx,
                "n_birds": len(detections),
                "detections": detections,
            })
            sampled += 1
            next_sample += frame_step
            frame_idx += 1
    finally:
        cap.release()

    summary = _summarise_species(per_species)
    tracks = _summarise_tracks(per_track_behaviors)
    payload = {
        "detector": "YOLO",
        "detector_weights": weights,
        "duration_seconds": round(duration_s, 2),
        "video_fps": round(fps, 2),
        "frames_sampled": sampled,
        "sample_every_s": sample_every_s,
        "timeline": timeline,
        "summary": summary,
        "tracks": tracks,
        "n_tracks": len(tracks),
    }

    if output_dir:
        _save_outputs(payload, flat_rows, Path(output_dir))

    return payload


def _detections_from_result(
    result,
    pil_frame: Image.Image,
    *,
    classifier_fn: ClassifierFn | None,
    class_filter: Iterable[str] | None,
) -> list[dict]:
    names = result.names or {}
    boxes = result.boxes
    if boxes is None or len(boxes) == 0:
        return []

    xyxy = boxes.xyxy.cpu().numpy()
    confs = boxes.conf.cpu().numpy()
    cls_ids = boxes.cls.cpu().numpy().astype(int)
    keep_names = set(class_filter) if class_filter else None
    default_coco_filter = keep_names is None and _looks_like_coco(names)

    detections = []
    for bbox, score, cls_id in zip(xyxy, confs, cls_ids):
        class_name = str(names.get(int(cls_id), cls_id))
        if keep_names is not None and class_name not in keep_names:
            continue
        if default_coco_filter and class_name != "bird":
            continue

        x0, y0, x1, y1 = _expand_bbox(bbox, pil_frame.size)
        if min(x1 - x0, y1 - y0) < 16:
            continue
        crop = pil_frame.crop((x0, y0, x1, y1))
        if classifier_fn:
            pred = classifier_fn(crop)
        else:
            pred = {
                "species_key": class_name,
                "common_name": class_name,
                "scientific": class_name,
                "confidence": round(float(score) * 100.0, 1),
                "color": "#1A6E68",
            }

        detections.append({
            "bbox": [int(x0), int(y0), int(x1), int(y1)],
            "bbox_score": round(float(score), 3),
            "yolo_class": class_name,
            "track_id": None,
            "behavior": "insufficient_track",
            "behavior_es": localized_behavior("insufficient_track", "es"),
            "behavior_en": localized_behavior("insufficient_track", "en"),
            "species_key": pred.get("species_key", class_name),
            "common_name": pred.get("common_name", class_name),
            "scientific": pred.get("scientific", pred.get("scientific_name", class_name)),
            "confidence": pred.get("confidence", round(float(score) * 100.0, 1)),
            "color": pred.get("color", "#1A6E68"),
        })
    return detections


def _looks_like_coco(names: dict) -> bool:
    values = {str(v) for v in names.values()}
    return "bird" in values and "person" in values and len(values) >= 20


def _ultralytics_device(device: str | None):
    if device is None:
        return None
    value = str(device).lower()
    if value == "cuda":
        return "0"
    if value.startswith("cuda:"):
        return value.split(":", 1)[1]
    return value


def _expand_bbox(bbox: np.ndarray, size: tuple[int, int], margin_ratio: float = 0.05):
    width, height = size
    x0, y0, x1, y1 = [float(v) for v in bbox]
    margin = margin_ratio * min(width, height)
    return (
        max(0, int(x0 - margin)),
        max(0, int(y0 - margin)),
        min(width, int(x1 + margin)),
        min(height, int(y1 + margin)),
    )


def _iou(a: list[float], b: list[float]) -> float:
    ax0, ay0, ax1, ay1 = a
    bx0, by0, bx1, by1 = b
    ix0, iy0 = max(ax0, bx0), max(ay0, by0)
    ix1, iy1 = min(ax1, bx1), min(ay1, by1)
    iw, ih = max(0.0, ix1 - ix0), max(0.0, iy1 - iy0)
    inter = iw * ih
    area_a = max(0.0, ax1 - ax0) * max(0.0, ay1 - ay0)
    area_b = max(0.0, bx1 - bx0) * max(0.0, by1 - by0)
    union = area_a + area_b - inter
    return inter / union if union > 0 else 0.0


def _summarise_species(per_species: dict[str, dict]) -> list[dict]:
    rows = []
    for row in per_species.values():
        primary = majority_behavior(row.pop("behaviors"))
        row["primary_behavior"] = primary
        row["primary_behavior_es"] = localized_behavior(primary, "es")
        row["primary_behavior_en"] = localized_behavior(primary, "en")
        rows.append(row)
    return sorted(rows, key=lambda x: (-x["detections"], x["common_name"]))


def _summarise_tracks(per_track_behaviors: dict[int, list[str]]) -> list[dict]:
    rows = []
    for track_id, labels in per_track_behaviors.items():
        primary = majority_behavior(labels)
        rows.append({
            "track_id": track_id,
            "primary_behavior": primary,
            "primary_behavior_es": localized_behavior(primary, "es"),
            "primary_behavior_en": localized_behavior(primary, "en"),
            "detections": len(labels),
        })
    return sorted(rows, key=lambda x: x["track_id"])


def _save_outputs(payload: dict, flat_rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "yolo_video_analysis.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    if flat_rows:
        fieldnames = [
            "t_seconds", "frame_idx", "track_id", "yolo_class", "bbox_score",
            "species_key", "common_name", "scientific", "cnn_confidence",
            "behavior", "bbox",
        ]
        with open(output_dir / "yolo_video_detections.csv", "w",
                  newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(flat_rows)
