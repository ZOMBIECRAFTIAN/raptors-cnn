# YOLO video module / Modulo de video YOLO

## Español

Este modulo agrega deteccion y seguimiento de aves en video con YOLO. La ruta
Flask `/identify_video` usa este flujo:

1. YOLO detecta aves por frame.
2. Un tracker ligero por IoU mantiene un `track_id` por individuo.
3. Cada recorte se clasifica con la CNN de 53 especies cuando existe el
   checkpoint `outputs/checkpoints/best_stage2.pt`.
4. El modulo calcula una etiqueta conservadora de comportamiento:
   `soaring_or_gliding`, `active_flapping_or_maneuvering`,
   `hovering_or_wind_hold`, `stoop_or_descent`,
   `perched_or_stationary` o `insufficient_track`.

Instalacion opcional:

```bash
cd codigo/pytorch
pip install -r requirements-yolo.txt
```

Analizar un video:

```bash
python yolo_predict_video.py --video ../../datos/videos/raw/Buteo_jamaicensis/clip_001.mp4
```

Entrenar un detector YOLO propio, cuando tengas cajas anotadas:

```bash
python yolo_train.py --data yolo/dataset_template.yaml --model yolov8n.pt --epochs 80
python yolo_evaluate.py --data yolo/dataset_template.yaml --weights outputs/yolo/checkpoints/best.pt
```

El detector por defecto usa `RAPTORS_YOLO_WEIGHTS` si existe, despues
`outputs/yolo/checkpoints/best.pt`, y si no hay pesos personalizados usa
`yolov8n.pt` como detector COCO de clase `bird`.

## English

This module adds YOLO-based bird detection and tracking for short videos. The
Flask `/identify_video` route runs:

1. YOLO detects birds per sampled frame.
2. A lightweight IoU tracker assigns a `track_id` per individual.
3. Each crop is classified by the 53-class CNN when
   `outputs/checkpoints/best_stage2.pt` is available.
4. The module exports a conservative behaviour cue:
   `soaring_or_gliding`, `active_flapping_or_maneuvering`,
   `hovering_or_wind_hold`, `stoop_or_descent`,
   `perched_or_stationary` or `insufficient_track`.

Optional installation:

```bash
cd codigo/pytorch
pip install -r requirements-yolo.txt
```

Analyze one video:

```bash
python yolo_predict_video.py --video ../../datos/videos/raw/Buteo_jamaicensis/clip_001.mp4
```

Train a custom YOLO detector once bounding boxes are annotated:

```bash
python yolo_train.py --data yolo/dataset_template.yaml --model yolov8n.pt --epochs 80
python yolo_evaluate.py --data yolo/dataset_template.yaml --weights outputs/yolo/checkpoints/best.pt
```

The detector prefers `RAPTORS_YOLO_WEIGHTS`, then
`outputs/yolo/checkpoints/best.pt`, and finally `yolov8n.pt` as a COCO `bird`
detector.
