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
├── gradcam.py         # Mapas de calor para verificar dónde "mira" el modelo
└── requirements.txt
```

## Instalación

```bash
cd codigo/pytorch
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
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
python train.py --arch resnet50

# Evaluación sobre test
python evaluate.py --arch resnet50 --weights outputs/checkpoints/best_stage2.pt

# Grad-CAM sobre una imagen
python gradcam.py --image path/a/cathartes.jpg --arch resnet50 --weights outputs/checkpoints/best_stage2.pt
```

## Notas

- Los modelos son inicializados con pesos pre-entrenados en ImageNet.
- `config.py` centraliza todos los hiperparámetros — modifícalo antes de tocar el resto.
- La pérdida es cross-entropy ponderada por clase + label smoothing.
- Augmentation incluye RandomResizedCrop, flip, rotation, color jitter, RandomErasing.
- Se recomienda GPU con ≥ 12 GB de VRAM.
