# Implementación PyTorch — Identificación de Aves Rapaces

Implementación del clasificador CNN en PyTorch siguiendo la metodología descrita en el Capítulo 3 de la tesis.

## Estructura

```
pytorch/
├── config.py          # Constantes e hiperparámetros centralizados
├── data_loader.py     # ImageFolder + augmentation + class weights
├── model.py           # ResNet50 / EfficientNet-B3 / MobileNetV3 / ConvNeXt
├── train.py           # Pipeline en dos etapas (feature extraction → fine-tuning)
├── evaluate.py        # Métricas, matriz de confusión y curvas ROC sobre test
├── audit_dataset.py   # Auditoría: fuga por observationID, soporte bajo, archivos raros
├── split_dataset.py   # Split por imagen o por observationID
├── gradcam.py         # Mapas de calor para verificar dónde "mira" el modelo
├── gradcam_batch.py   # Auditoría Grad-CAM por lote: aciertos, errores y CSV
├── yolo/              # Detección/seguimiento en video + heurísticas de comportamiento
├── yolo_train.py      # Entrenamiento de detector YOLO con cajas anotadas
├── yolo_evaluate.py   # Evaluación YOLO (mAP, precision, recall)
├── yolo_predict_video.py # Inferencia YOLO sobre un clip
└── requirements.txt
```

## Instalación

```bash
cd codigo/pytorch
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Opcional: video YOLO
pip install -r requirements-yolo.txt
```

## Estructura de datos esperada

```
datos/processed/
├── train/
│   ├── Cathartes_aura/
│   ├── Coragyps_atratus/
│   ├── Buteo_platypterus/
│   ├── Buteo_swainsoni/
│   ├── Ictinia_mississippiensis/
│   ├── Pandion_haliaetus/
│   └── Falco_sparverius/
├── val/  (misma estructura)
└── test/ (misma estructura)
```

## Uso

```bash
# Entrenamiento completo (etapa 1 + etapa 2)
python split_dataset.py --group-by-observation --clean --link
python audit_dataset.py --fail-on-leak
python train.py --arch resnet50 --split-protocol observation

# Evaluación sobre test
python evaluate.py --arch resnet50 --weights outputs/checkpoints/best_stage2_resnet50.pt --split-protocol observation

# Grad-CAM sobre una imagen
python gradcam.py --image path/a/cathartes.jpg --arch resnet50 --weights outputs/checkpoints/best_stage2.pt

# Grad-CAM por lote sobre aciertos/errores del test
python gradcam_batch.py --arch resnet50 --weights outputs/checkpoints/best_stage2_resnet50.pt --split test --correct 10 --incorrect 10

# Analizar un video con YOLO
python yolo_predict_video.py --video ../../datos/videos/raw/Buteo_jamaicensis/clip_001.mp4

# Entrenar y evaluar un detector YOLO propio cuando tengas cajas anotadas
python yolo_train.py --data yolo/dataset_template.yaml --model yolov8n.pt --epochs 80
python yolo_evaluate.py --data yolo/dataset_template.yaml --weights outputs/yolo/checkpoints/best.pt
```

## Notas

- Los modelos son inicializados con pesos pre-entrenados en ImageNet.
- `config.py` centraliza todos los hiperparámetros — modifícalo antes de tocar el resto.
- La pérdida es cross-entropy ponderada por clase + label smoothing.
- Augmentation incluye RandomResizedCrop, flip, rotation, color jitter, RandomErasing.
- Se recomienda GPU con ≥ 12 GB de VRAM.
- El módulo YOLO es opcional: usa `RAPTORS_YOLO_WEIGHTS`, luego `outputs/yolo/checkpoints/best.pt`, y finalmente `yolov8n.pt` como detector COCO de clase `bird`.
- YOLO detecta/localiza aves; la CNN sigue siendo responsable de la identificación fina de las 53 especies.
- Para resultados de tesis, usa `split_dataset.py --group-by-observation` y valida con `audit_dataset.py --fail-on-leak` antes de entrenar.
- `train.py` y `evaluate.py` guardan manifiestos/metadatos para rastrear arquitectura, seed, commit, split y conteos del dataset.
