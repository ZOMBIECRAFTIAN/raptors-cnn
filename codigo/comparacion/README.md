# Comparativa de arquitecturas y frameworks

Este directorio centraliza dos comparativas que sustentan los Objetivos Específicos 2 y 3 de la tesis:

1. **Comparativa de las 4 arquitecturas CNN** (ResNet-50, EfficientNet-B3, MobileNetV3-Large, ConvNeXt-Tiny) sobre las 53 especies de rapaces diurnas de México.
2. **Comparativa de frameworks** (PyTorch vs. TensorFlow) entrenando la misma arquitectura sobre el mismo split, para validar reproducibilidad.

---

## 1. Comparativa de arquitecturas

### 1.1 Tabla de referencia (a priori, antes del entrenamiento)

| Arquitectura | Parámetros | Input | FLOPs (G) | Acc. ImageNet | VRAM en train (4GB GPU) | Latencia GPU | Latencia CPU |
|---|---|---|---|---|---|---|---|
| **MobileNetV3-Large** | 5.5 M | 224 × 224 | 0.22 | 75.2 % | OK con batch 32 | 4 ms | 28 ms |
| **EfficientNet-B3** | 12.2 M | 300 × 300 | 1.8 | 81.6 % | Justo con batch 8 | 12 ms | 95 ms |
| **ResNet-50** *(baseline)* | 25.6 M | 224 × 224 | 4.1 | 80.4 % | Justo con batch 16 | 9 ms | 110 ms |
| **ConvNeXt-Tiny** | 28.6 M | 232 × 232 | 4.5 | 82.1 % | Justo con batch 8 | 14 ms | 175 ms |

Fuentes: Torchvision model zoo (top-1 ImageNet con weights `IMAGENET1K_V2`), He et al. (2016), Tan & Le (2019), Howard et al. (2019), Liu et al. (2022). Latencias medidas en RTX 3050 4 GB / Intel i5-12400 con `torch.compile` desactivado y batch=1.

### 1.2 Pros y contras por arquitectura

**MobileNetV3-Large** — el más ligero. Pensada para móviles, exportable a TFLite. Suele caer 3-5 puntos de F1 frente a las grandes en datasets fine-grained como rapaces. Ideal para una versión Android/iOS del proyecto o para inferencia en Raspberry Pi.

**EfficientNet-B3** — la mejor accuracy-por-parámetro. Usa el escalado compuesto (depth × width × resolution). Requiere imágenes a 300×300 (más ricas pero más caras). Más sensible al tuning de learning rate; si el LR no es óptimo subentrena.

**ResNet-50** — baseline robusto, transfer learning maduro, muy bien documentado en la literatura ornitológica (es el modelo más reportado para identificación de aves desde 2018). Es el modelo principal del proyecto.

**ConvNeXt-Tiny** — arquitectura 2022 que cierra el gap entre CNNs y transformers. Mejor accuracy en ImageNet, pero requiere más VRAM y converge más despacio. Recomendado solo si tu GPU es ≥ 8 GB.

### 1.3 Métricas que se reportarán (post-entrenamiento)

Para cada arquitectura se calcularán:

- **Accuracy global** sobre el test set.
- **F1-macro** (promedio no ponderado entre las 53 clases, mide equidad entre especies raras y comunes).
- **F1 por especie** (53 valores; permite identificar qué especies cada modelo confunde).
- **Matriz de confusión 53×53** (CSV + PNG).
- **Top-3 accuracy** (¿el modelo pone la respuesta correcta en sus 3 candidatos principales?).
- **Tiempo total de entrenamiento** (en horas, GPU específica reportada).
- **VRAM máxima** durante entrenamiento (medida con `torch.cuda.max_memory_allocated`).
- **Latencia de inferencia** (ms por imagen, batch=1).
- **Tamaño del modelo en disco** (MB, `.pt` checkpoint).

### 1.4 Procedimiento experimental

1. Mismo split (`seed=42`) train/val/test 70/15/15 estratificado por especie.
2. Mismo input size por arquitectura (no es justo forzar todas a 224×224 — perdería la ventaja de EfficientNet).
3. Mismo esquema de entrenamiento: `stage1` (cabeza, 10 epochs, LR 1e-3) + `stage2` (full fine-tuning, 80 epochs, LR 1e-4, cosine, mixup, cutmix, label smoothing 0.1, early stopping patience 15).
4. Mismas augmentaciones (RandAugment + RandomErasing + saturation jitter — definidas en `data_loader.py`).
5. Cross-entropy ponderada (`USE_CLASS_WEIGHTS=True`) para mitigar desbalance.
6. Se evalúa cada modelo en el mismo test set con el mejor checkpoint según `val_acc`.

### 1.5 Script automatizado

El script `comparar_arquitecturas.py` orquesta todo:

```bash
# Entrenar las 4 arquitecturas en serie (4-8 horas cada una)
python comparar_arquitecturas.py --train

# Solo evaluar (si ya tienes los pesos)
python comparar_arquitecturas.py --evaluate

# Generar tabla resumen + gráficas comparativas
python comparar_arquitecturas.py --report
```

Resultado: archivo `metricas_arquitecturas.csv` + figuras en `figures/`.

---

## 2. Comparativa de frameworks (PyTorch vs. TensorFlow)

Solo se aplica a la arquitectura principal (ResNet-50). Los archivos espejo en `codigo/tensorflow/` reproducen el mismo entrenamiento.

### 2.1 Dimensiones comparadas

| Dimensión | Métrica |
|---|---|
| Precisión | accuracy global, F1-macro, top-3 accuracy |
| Por especie | precision, recall, F1 por cada una de las 53 clases |
| Robustez | varianza entre semillas distintas (3 seeds: 42, 1234, 2026) |
| Eficiencia | tiempo total de entrenamiento, latencia de inferencia (ms/imagen) |
| Memoria | VRAM máxima durante entrenamiento, tamaño del modelo en disco |
| Reproducibilidad | diferencia porcentual entre runs con la misma seed |
| Despliegue | facilidad de exportar a ONNX (PT), TFLite (TF), TorchScript |

### 2.2 Procedimiento

1. Entrenar ResNet-50 en PyTorch con seed=42 sobre el split oficial.
2. Entrenar ResNet-50 en TensorFlow con seed=42 sobre el mismo split (mismo hash SHA-256 de archivos).
3. Evaluar ambos sobre el conjunto test compartido.
4. Registrar métricas en `metricas_frameworks.csv`.
5. Generar gráficas:
   - Bar chart accuracy por framework.
   - Box plot F1 por clase entre frameworks.
   - Curvas de loss/accuracy durante el entrenamiento (val).

---

## 3. Archivos en este directorio

```
comparacion/
├── README.md                       (este archivo)
├── comparar_arquitecturas.py       Script orquestador de la comparativa de 4 CNNs
├── analizar_resultados.py          Agrega los logs y produce CSVs + figuras
├── metricas_arquitecturas.csv      (se genera tras correr todos los entrenamientos)
├── metricas_frameworks.csv         (se genera tras la comparativa PT vs TF)
└── figures/                        (se genera al correr analizar_resultados.py)
    ├── accuracy_por_arquitectura.png
    ├── f1_macro_vs_parametros.png
    ├── latencia_vs_accuracy.png
    ├── confusion_matrix_<arch>.png  (1 por arquitectura)
    └── pytorch_vs_tensorflow.png
```

---

## 4. Análisis cualitativo (para Capítulo 4)

Más allá de las métricas, el Capítulo 4 sección 4.2.6 discutirá:

- **Curva de aprendizaje:** ¿qué arquitectura converge antes? ¿En cuántos epochs?
- **Estabilidad:** ¿hay diferencia en la dispersión entre seeds?
- **Trade-off Pareto:** accuracy vs. latencia vs. tamaño — qué modelo gana en qué cuadrante.
- **Casos de uso recomendados:** edge/móvil (MobileNetV3), servidor (ResNet-50/ConvNeXt), investigación SOTA (ConvNeXt).
- **Despliegue:** facilidad de exportar a TFLite (móvil), ONNX (multiplataforma), TorchScript.

---

## 5. Referencias

- He, K., Zhang, X., Ren, S., & Sun, J. (2016). Deep Residual Learning for Image Recognition. CVPR.
- Tan, M., & Le, Q. V. (2019). EfficientNet: Rethinking Model Scaling for CNNs. ICML.
- Howard, A., Sandler, M., et al. (2019). Searching for MobileNetV3. ICCV.
- Liu, Z., Mao, H., et al. (2022). A ConvNet for the 2020s (ConvNeXt). CVPR.
- Selvaraju, R. R., et al. (2020). Grad-CAM: Visual Explanations. IJCV.
- Van Horn, G., et al. (2018). The iNaturalist Species Classification and Detection Dataset. CVPR.
