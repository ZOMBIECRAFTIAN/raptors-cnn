# Pre-Registro del Proyecto raptors-cnn

> Documento de **pre-registro de hipótesis y métodos**, exigible en proyectos de Maestría con componente cuantitativo. Sigue las recomendaciones del Center for Open Science (COS) y el formato adaptado de Munafò et al. (2017) sobre ciencia reproducible.

**Fecha de pre-registro:** 2026-05-14
**Autor:** Brian Fernández Báez
**Repositorio público:** https://github.com/ZOMBIECRAFTIAN/raptors-cnn
**Versión del pre-registro:** 1.1

---

## 1. Pregunta de investigación

**P1:** ¿Puede una red neuronal convolucional entrenada mediante transfer learning identificar correctamente las 53 especies de rapaces diurnas de México a partir de imágenes en vuelo, reportando métricas globales y por especie?

**P2:** ¿Cuál de las cuatro arquitecturas (ResNet-50, EfficientNet-B3, MobileNetV3-Large, ConvNeXt-Tiny) ofrece el mejor compromiso entre precisión y eficiencia computacional?

**P3:** ¿Puede un catálogo de 53 señas en International Sign, co-creado con la comunidad sorda, obtener calificación promedio ≥ 4.0 / 5.0 en escala Likert sobre claridad, naturalidad y memorabilidad?

**P4:** ¿Puede un módulo basado en YOLO detectar y seguir aves en video para extraer señales de comportamiento de vuelo que complementen la clasificación visual?

## 2. Hipótesis

**H1 (principal, cuantitativa):**
Una CNN ResNet-50 entrenada en dos etapas (feature extraction de 10 epochs + fine-tuning de hasta 80 epochs con cross-entropy ponderada por clase, Mixup/CutMix y label smoothing) funcionará como baseline principal para el catálogo nacional de 53 especies. La hipótesis se evaluará con:
- Accuracy global
- F1 macro
- F1 por especie
- Top-3 accuracy
- AUC macro

**H0 (hipótesis nula):**
La CNN no superará un baseline trivial (modelo que predice la clase mayoritaria) en F1 macro con significancia estadística p < 0.05.

**H2 (complementaria, cualitativa-cuantitativa):**
Un catálogo de 53 señas en IS, validado con grupo focal de 8-12 miembros de la comunidad sorda, obtendrá promedio Likert ≥ 4.0 en cada una de las tres dimensiones (claridad, naturalidad, memorabilidad).

## 3. Diseño experimental

### 3.1 Variables

**Variables independientes:**
- Arquitectura CNN (factor de 4 niveles): ResNet-50, EfficientNet-B3, MobileNetV3-Large, ConvNeXt-Tiny.
- Framework (factor de 2 niveles): PyTorch, TensorFlow.

**Variables dependientes:**
- Accuracy global, precision/recall por clase, F1 macro, ROC-AUC, top-3 accuracy.
- Tiempo de inferencia por imagen (ms).
- VRAM máxima durante entrenamiento (GB).

**Variables de control:**
- Resolución de entrada: 224×224 (256×256 internamente con center crop).
- Batch size: 32 (16 si OOM).
- Semilla aleatoria: 42 (fijo en todos los experimentos).
- División train/val/test: 70/15/15 estratificada.
- Hardware: GPU NVIDIA RTX 3050 (4.3 GB VRAM) o equivalente.

### 3.2 Tamaño muestral

**Justificación:**
- Mínimo de 200 imágenes por clase basado en heurística de Tan & Le (2019) para fine-tuning de EfficientNet con transfer learning sobre dominios específicos.
- Total objetivo inicial: 10,600 imágenes (53 × 200), aceptando estrategia de "best effort" para especies extremadamente raras como *Morphnus guianensis*, *Harpia harpyja* y *Falco deiroleucus*.
- Baseline aleatorio aproximado: 1/53 ≈ 1.9 %. Debido al desbalance esperado, F1 macro será la métrica primaria de comparación.

### 3.3 Procedimientos de validación

1. **Validación cruzada estratificada** k=5 sobre el conjunto train+val, manteniendo proporciones de clase.
2. **Test reservado** (15 %) inalterable hasta el reporte final.
3. **Doble anotación** de cada imagen por dos observadores; kappa de Cohen mínimo aceptado: κ ≥ 0.80.
4. **Test estadístico para comparativa** PyTorch vs TensorFlow: McNemar pareado sobre el test, complementado con t-test pareado sobre folds.

### 3.4 Criterios de exclusión

- Imágenes con resolución < 640 px en el lado mayor.
- Imágenes donde múltiples especies aparezcan sin posibilidad de recortar.
- Imágenes con marca de agua sobre el individuo.
- Imágenes donde el ave está posada (no en vuelo) → corpus principal.
- Imágenes con desacuerdo inter-anotador no resuelto tras tercera revisión.

## 4. Análisis estadístico planeado

### 4.1 Métricas primarias

| Métrica | Fórmula | Reporte |
|---------|---------|---------|
| Accuracy | (TP+TN)/(TP+TN+FP+FN) | Media ± IC 95 % por bootstrap (1000 reps) |
| F1 macro | Media aritmética de F1 por clase | Media ± IC 95 % por bootstrap |
| AUC macro | Media de AUCs one-vs-rest | Media ± IC 95 % |
| Kappa de Cohen | (Po−Pe)/(1−Pe) | Para acuerdo inter-anotador |

### 4.2 Análisis comparativo

- **Test de McNemar** (no-paramétrico, clasificadores pareados sobre mismo test).
- **t-test pareado** sobre métricas por fold.
- **Corrección Bonferroni** para comparaciones múltiples (4 arquitecturas × 2 frameworks = 8, threshold ajustado p < 0.0125).

### 4.3 Análisis de errores

- Matriz de confusión 53×53 normalizada por filas.
- Análisis cualitativo de pares confundidos con frecuencia (ej. *Buteo* juveniles entre sí, *Spizaetus* spp., *Cathartes aura* vs. *Cathartes burrovianus*).
- Grad-CAM sobre 3 imágenes correctas y 3 incorrectas por clase.

## 5. Resultados que considero como "aceptables"

Esta tesis considera la hipótesis H1 **soportada** si y solo si:
1. Al menos UNA arquitectura supera claramente el baseline mayoritario y aleatorio en test.
2. F1 macro y top-3 accuracy son suficientemente altos para justificar continuidad experimental.
3. No hay ninguna clase con recall < 0.50 (todas las especies son identificables al menos la mitad del tiempo).

Si H1 NO se soporta, la tesis aún tiene valor: documentar el resultado negativo es contribución científica, identificar qué clases son irrecuperables sin más datos es información práctica.

## 6. Resultados que serían sospechosos

Las siguientes señales activarían revisión rigurosa antes de aceptar resultados:

- Accuracy > 99 % (probable shortcut learning o fuga de datos).
- F1 macro idéntico entre clases muy distintas en abundancia (probable sesgo de evaluación).
- Variabilidad inter-fold > 5 puntos (entrenamiento inestable).
- Grad-CAM atendiendo a regiones del fondo en lugar del ave (modelo aprendió cielo, no especie).

Cualquiera de estos resultados activa una segunda iteración del análisis y revisión del pipeline.

## 7. Limitaciones reconocidas pre-experimento

- El dataset puede no representar variación geográfica completa entre norte, centro, sur y trópico mexicano.
- La validación del catálogo de señas se realizará con grupo focal mexicano; generalización a otras comunidades sordas internacionales será trabajo futuro.
- Hardware de entrenamiento (RTX 3050, 4.3 GB VRAM) puede limitar tamaño de batch en arquitecturas grandes (ConvNeXt-Tiny puede requerir batch=16 en lugar de 32).
- El módulo YOLO de video/comportamiento existe como prototipo, pero sus resultados de comportamiento son heurísticos hasta contar con cajas y etiquetas temporales anotadas.

## 8. Compromisos de transparencia

- **Código:** publicación bajo MIT License en GitHub público desde el inicio.
- **Datos:** metadatos en CSV abierto; imágenes con licencia CC-BY individuales documentadas.
- **Pesos del modelo:** CC-BY 4.0 al final del proyecto.
- **Negativos:** se publicarán resultados negativos o no concluyentes con el mismo rigor que los positivos.
- **Cambios al pre-registro:** documentados con fecha y motivo en `documentacion/preregistration_changelog.md`.

---

## Referencias

- Munafò, M. R., et al. (2017). A manifesto for reproducible science. *Nature Human Behaviour*, 1(1), 0021.
- Center for Open Science. (2022). Preregistration Templates. https://osf.io/zab38/
- Tan, M., & Le, Q. V. (2019). EfficientNet: Rethinking model scaling for convolutional neural networks. *ICML 2019*.
- Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and Psychological Measurement*, 20(1), 37–46.

---

*Este pre-registro queda fechado y versionado en el repositorio git. Cualquier modificación posterior se documenta en `preregistration_changelog.md` con fecha, autor y justificación.*
