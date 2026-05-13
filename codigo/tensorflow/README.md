# Implementación TensorFlow / Keras — Identificación de Aves Rapaces

Implementación espejo de la versión PyTorch para realizar la comparativa exigida por el OE2 de la tesis. Misma división de datos, mismas arquitecturas, mismas métricas.

## Estructura

```
tensorflow/
├── config.py        # 14 especies y mismos hiperparámetros que PyTorch
├── data_loader.py   # tf.keras.utils.image_dataset_from_directory + augmentation
├── model.py         # ResNet50 / EfficientNetB3 / MobileNetV3Large / ConvNeXtTiny
├── train.py         # Pipeline en dos etapas (Keras callbacks, EarlyStopping)
├── evaluate.py      # Métricas, matriz de confusión, ROC
└── requirements.txt
```

## Instalación

```bash
cd codigo/tensorflow
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Uso

```bash
# Entrenamiento (etapa 1 + etapa 2)
python train.py --arch resnet50

# Evaluación
python evaluate.py --weights outputs/checkpoints/best_stage2.keras
```

## Notas de paridad con PyTorch

- `SPECIES`, `INPUT_SIZE`, `BATCH_SIZE` y los diccionarios `STAGE1` / `STAGE2` son idénticos a los de la implementación PyTorch.
- El mismo seed (42) y la misma estructura de carpetas garantizan resultados comparables.
- Las pequeñas divergencias esperadas entre frameworks (precisión numérica, scheduler, BatchNorm) se reportan en el Capítulo 4, sección 4.2.6.
