"""Flight-behaviour heuristics built on top of YOLO tracks.

The labels are intentionally conservative. They are not a trained behaviour
classifier yet; they provide interpretable features and a baseline for the
future annotated-video experiment.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import hypot


@dataclass
class TrackPoint:
    """Single position of one tracked bird in a sampled frame."""

    t: float
    cx: float
    cy: float
    area: float
    frame_width: int
    frame_height: int


BEHAVIOR_LABELS = {
    "insufficient_track": {
        "es": "trayectoria insuficiente",
        "en": "insufficient track",
    },
    "perched_or_stationary": {
        "es": "posado o casi estacionario",
        "en": "perched or nearly stationary",
    },
    "soaring_or_gliding": {
        "es": "planeo o deslizamiento",
        "en": "soaring or gliding",
    },
    "active_flapping_or_maneuvering": {
        "es": "aleteo activo o maniobra",
        "en": "active flapping or maneuvering",
    },
    "hovering_or_wind_hold": {
        "es": "cernido o sosteniendose en viento",
        "en": "hovering or wind hold",
    },
    "stoop_or_descent": {
        "es": "picada o descenso rapido",
        "en": "stoop or fast descent",
    },
    "transit_flight": {
        "es": "vuelo de traslado",
        "en": "transit flight",
    },
}


def localized_behavior(label: str, lang: str = "es") -> str:
    """Return a readable behaviour label in Spanish or English."""
    values = BEHAVIOR_LABELS.get(label, BEHAVIOR_LABELS["insufficient_track"])
    return values.get(lang, values["en"])


def classify_track(points: list[TrackPoint]) -> str:
    """Classify a short track using movement, vertical trend and area change."""
    if len(points) < 3:
        return "insufficient_track"

    diag = hypot(points[-1].frame_width, points[-1].frame_height) or 1.0
    duration = max(points[-1].t - points[0].t, 1e-6)

    distances = [
        hypot(b.cx - a.cx, b.cy - a.cy) / diag
        for a, b in zip(points, points[1:])
    ]
    total_motion = sum(distances)
    avg_speed = total_motion / duration

    areas = [max(p.area, 1.0) for p in points]
    area_delta = (areas[-1] - areas[0]) / max(areas[0], 1.0)
    area_range = (max(areas) - min(areas)) / max(sum(areas) / len(areas), 1.0)

    vertical_delta = (points[-1].cy - points[0].cy) / max(points[-1].frame_height, 1)
    vertical_speed = vertical_delta / duration
    horizontal_range = (
        max(p.cx for p in points) - min(p.cx for p in points)
    ) / max(points[-1].frame_width, 1)
    vertical_range = (
        max(p.cy for p in points) - min(p.cy for p in points)
    ) / max(points[-1].frame_height, 1)

    direction_changes = 0
    previous_sign = 0
    for a, b in zip(points, points[1:]):
        dx = b.cx - a.cx
        sign = 1 if dx > 2 else -1 if dx < -2 else 0
        if previous_sign and sign and sign != previous_sign:
            direction_changes += 1
        if sign:
            previous_sign = sign

    if avg_speed < 0.004 and area_range < 0.20:
        return "perched_or_stationary"
    if vertical_speed > 0.030 and area_delta > 0.10:
        return "stoop_or_descent"
    if avg_speed < 0.012 and vertical_range < 0.06 and horizontal_range < 0.08:
        return "hovering_or_wind_hold"
    if avg_speed < 0.030 and area_range < 0.35:
        return "soaring_or_gliding"
    if avg_speed >= 0.030 or direction_changes >= 2:
        return "active_flapping_or_maneuvering"
    return "transit_flight"


def majority_behavior(labels: list[str]) -> str:
    """Return the most frequent non-empty behaviour label."""
    clean = [label for label in labels if label]
    if not clean:
        return "insufficient_track"
    return Counter(clean).most_common(1)[0][0]
