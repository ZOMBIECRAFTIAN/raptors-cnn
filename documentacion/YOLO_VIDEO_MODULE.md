# YOLO video module: scope, validation and defense notes

## Espanol

### Que hace hoy

El modulo YOLO es complementario al clasificador CNN. Su objetivo no es
reemplazar la identificacion de especie, sino convertir un video en evidencia
usable:

1. Detecta aves por frame con YOLO.
2. Asigna `track_id` por individuo usando tracking ligero por IoU.
3. Recorta cada ave detectada.
4. Envia el recorte al clasificador CNN de 53 especies cuando existe un
   checkpoint entrenado.
5. Resume movimiento con heuristicas conservadoras:
   `soaring_or_gliding`, `active_flapping_or_maneuvering`,
   `hovering_or_wind_hold`, `stoop_or_descent`,
   `perched_or_stationary` o `insufficient_track`.

### Como defenderlo

La forma correcta de presentarlo es:

> El sistema principal de identificacion de especie es la CNN entrenada sobre
> imagenes. YOLO es un modulo complementario de video que localiza aves,
> genera recortes y permite empezar a modelar comportamiento de vuelo. En esta
> etapa funciona como prototipo tecnico y baseline interpretable; todavia no se
> reporta como resultado final de comportamiento.

### Que NO se debe afirmar todavia

- No afirmar que el sistema "reconoce comportamiento" con precision validada.
- No afirmar que YOLO ya esta entrenado especificamente para rapaces mexicanas
  si se esta usando `yolov8n.pt` de COCO.
- No mezclar metricas de la CNN con metricas de deteccion YOLO.
- No usar comportamiento como prueba principal hasta tener etiquetas temporales
  revisadas.

### Validacion necesaria para tesis

| Componente | Metrica necesaria | Evidencia |
|---|---|---|
| Deteccion de aves | mAP50, mAP50-95, precision, recall | Dataset con cajas anotadas |
| Tracking | ID switches, track continuity, fragmentacion | Clips con individuos revisados |
| Comportamiento | F1-macro por conducta, matriz de confusion | Etiquetas temporales por clip |
| Fusion CNN+YOLO | Accuracy/F1 contra CNN sola | Ablation study |

### Comandos

```bash
cd codigo/pytorch
pip install -r requirements-yolo.txt

# Inferencia de video
python yolo_predict_video.py --video ../../datos/videos/raw/Buteo_jamaicensis/clip_001.mp4

# Entrenamiento YOLO propio cuando existan cajas anotadas
python yolo_train.py --data yolo/dataset_template.yaml --model yolov8n.pt --epochs 80

# Evaluacion del detector
python yolo_evaluate.py --data yolo/dataset_template.yaml --weights outputs/yolo/checkpoints/best.pt
```

## English

### What it currently does

The YOLO module complements the CNN classifier. It does not replace
species-level identification; it turns a short video into usable visual
evidence:

1. YOLO detects birds per frame.
2. A lightweight IoU tracker assigns a `track_id` per individual.
3. Each detected bird is cropped.
4. The crop is sent to the 53-class CNN when a trained checkpoint exists.
5. Motion is summarized with conservative heuristic labels:
   `soaring_or_gliding`, `active_flapping_or_maneuvering`,
   `hovering_or_wind_hold`, `stoop_or_descent`,
   `perched_or_stationary` or `insufficient_track`.

### Correct defense framing

> The main species-identification system is the CNN trained on images. YOLO is
> a complementary video module that localizes birds, produces crops, and starts
> modeling flight behaviour. At this stage it is a technical prototype and
> interpretable baseline; it is not yet a final validated behaviour result.

### Claims to avoid for now

- Do not claim validated behaviour-recognition accuracy yet.
- Do not claim YOLO is already custom-trained for Mexican raptors if the
  current fallback is COCO `yolov8n.pt`.
- Do not mix CNN classification metrics with YOLO detection metrics.
- Do not use behaviour as primary evidence until temporal labels are reviewed.

### Thesis validation requirements

| Component | Required metric | Evidence |
|---|---|---|
| Bird detection | mAP50, mAP50-95, precision, recall | Dataset with bounding boxes |
| Tracking | ID switches, track continuity, fragmentation | Reviewed multi-bird clips |
| Behaviour | Macro-F1 per behaviour, confusion matrix | Temporal clip labels |
| CNN+YOLO fusion | Accuracy/F1 against CNN-only baseline | Ablation study |

### Commands

```bash
cd codigo/pytorch
pip install -r requirements-yolo.txt

# Video inference
python yolo_predict_video.py --video ../../datos/videos/raw/Buteo_jamaicensis/clip_001.mp4

# Custom YOLO training once boxes exist
python yolo_train.py --data yolo/dataset_template.yaml --model yolov8n.pt --epochs 80

# Detector evaluation
python yolo_evaluate.py --data yolo/dataset_template.yaml --weights outputs/yolo/checkpoints/best.pt
```
