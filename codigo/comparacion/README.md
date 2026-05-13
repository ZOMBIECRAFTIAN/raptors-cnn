# Comparativa PyTorch vs. TensorFlow

Este directorio centraliza el material de la comparativa entre los dos frameworks que exige el Objetivo Específico 2 de la tesis.

## Qué se compara

Para cada una de las 4 arquitecturas (ResNet50, EfficientNet-B3, MobileNetV3-Large, ConvNeXt-Tiny):

| Dimensión | Métrica |
|-----------|---------|
| Precisión | accuracy global, F1 macro, top-3 accuracy |
| Por especie | precision, recall, F1 por cada una de las 14 clases |
| Robustez | varianza entre folds en validación cruzada (5-fold) |
| Eficiencia | tiempo total de entrenamiento, latencia de inferencia (ms/imagen) |
| Memoria | VRAM máxima durante entrenamiento, tamaño del modelo en disco |
| Reproducibilidad | varianza entre semillas distintas |
| Despliegue | facilidad de exportar a ONNX, TorchScript, TFLite |

## Procedimiento de comparación

1. Entrenar el modelo en PyTorch con seed=42.
2. Entrenar el modelo en TensorFlow con seed=42 sobre el mismo split (mismo hash de archivos).
3. Evaluar ambos sobre el conjunto test compartido.
4. Registrar métricas y latencia en `metrics.csv` (script de agregación a desarrollar).
5. Generar las gráficas comparativas:
   - Bar chart de accuracy por arquitectura × framework.
   - Box plot de F1 por clase entre frameworks.
   - Curvas ROC superpuestas.

## Script previsto (a implementar)

```python
# codigo/comparacion/compare.py
# Lee las dos carpetas outputs/ (pytorch/ y tensorflow/),
# unifica los reportes JSON y produce metrics.csv + figuras comparativas.
```

## Análisis cualitativo

Más allá de las métricas, el Capítulo 4 sección 4.2.6 discutirá:

- Curva de aprendizaje: ¿en qué framework converge antes el modelo?
- Estabilidad: ¿hay diferencia en la dispersión entre folds?
- Ergonomía: tiempo del autor para implementar cada framework, claridad del API.
- Despliegue: facilidad de exportar el mejor modelo a TFLite (móvil) o ONNX (multiplataforma).

## Archivos esperados aquí

```
comparacion/
├── README.md            (este archivo)
├── compare.py           (a implementar)
├── metrics.csv          (a generar tras los entrenamientos)
└── figures/
    ├── accuracy_comparison.png
    ├── f1_per_class.png
    └── roc_overlay.png
```
