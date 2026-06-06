# Glosario de Términos Técnicos

> Glosario unificado de términos especializados utilizados en la tesis y el repositorio. Útil para lectores no especialistas en alguna de las tres disciplinas convergentes (ornitología, visión computacional, lingüística de señas).

---

## A — Ornitología

**Accipitridae.** Familia taxonómica que incluye águilas, gavilanes, aguilillas y zopilotes negros del Viejo Mundo (no del Nuevo). Una de las dos familias dominantes del proyecto.

**Aspect ratio (en vuelo).** Relación largo:ancho del ala, utilizada como rasgo diagnóstico en identificación de rapaces. Alta aspect ratio = ala larga y estrecha (planeador eficiente). Baja = ala corta y ancha (vuelo maniobrable en bosques).

**Bottleneck migratorio.** Sitio geográfico donde la migración se concentra debido a obstáculos para volar (montañas, agua). Veracruz es el bottleneck más importante del mundo.

**Cathartidae.** Familia de zopilotes del Nuevo Mundo (Cathartes aura, Coragyps atratus). Pese a su apariencia, NO son rapaces verdaderas — son carroñeras emparentadas con cigüeñas.

**Diédrico.** Posición de las alas en V vista desde el frente. Característico de Cathartes aura, Buteo albonotatus y otras especies que utilizan vuelo en V para estabilidad en térmicas.

**Falconidae.** Familia de halcones y caracaras. NO emparentada filogenéticamente con Accipitridae (convergencia evolutiva).

**Kettle.** Formación de bandada en espiral ascendente que aprovecha una térmica. Visible especialmente con Buteo platypterus en pico migratorio.

**Pandionidae.** Familia monotípica del águila pescadora (Pandion haliaetus). Anatómicamente distinta del resto de Accipitriformes.

**Rapaces diurnas.** Aves de presa activas durante el día (excluye búhos y lechuzas, que son Strigiformes nocturnas).

**Soaring.** Vuelo planeado sin batir alas, aprovechando corrientes ascendentes. Modo dominante de migración para Cathartes aura, Buteo y Pandion.

**Stoop.** Picada vertical a alta velocidad, característica diagnóstica de Falco peregrinus (alcanza > 300 km/h).

---

## B — Visión Computacional y Machine Learning

**AUC (Area Under the Curve).** Métrica que cuantifica el área bajo la curva ROC. Valor 1.0 = clasificador perfecto, 0.5 = aleatorio.

**Backpropagation (retropropagación).** Algoritmo para calcular gradientes de la función de pérdida respecto a cada parámetro de la red, propagando errores desde la salida hacia atrás.

**CNN (Convolutional Neural Network).** Red neuronal con capas convolucionales que detectan patrones espaciales locales. Modelo dominante para clasificación de imágenes desde Krizhevsky et al. (2012).

**Cross-entropy loss.** Función de pérdida estándar para clasificación multiclase. L = − Σᵢ yᵢ · log(ŷᵢ).

**Data augmentation.** Técnica para incrementar virtualmente el tamaño del dataset aplicando transformaciones aleatorias durante el entrenamiento (rotación, flip, color jitter, mixup, CutMix).

**Dropout.** Regularización que apaga aleatoriamente un porcentaje de neuronas durante el entrenamiento para reducir overfitting.

**Fine-tuning.** Proceso de re-entrenar un modelo pre-entrenado (típicamente en ImageNet) con datos del dominio específico, ajustando todos los parámetros con learning rate bajo.

**F1-score.** Media armónica de precision y recall. Apropiada para clases desbalanceadas.

**Grad-CAM (Gradient-weighted Class Activation Mapping).** Técnica de interpretabilidad que produce mapas de calor indicando qué regiones de la imagen contribuyeron más a la decisión del modelo (Selvaraju et al., 2017).

**ImageNet.** Dataset de 1.4M imágenes en 1000 clases, estándar para pre-entrenamiento de modelos de visión.

**Kappa de Cohen.** Coeficiente que cuantifica acuerdo entre dos anotadores corrigiendo el acuerdo esperado por azar. κ ≥ 0.80 considerado "casi perfecto".

**Label smoothing.** Técnica de regularización que reemplaza etiquetas one-hot duras (1.0) por valores suavizados (0.9), reduciendo overconfidence.

**Mixup.** Augmentation que combina linealmente pares de imágenes y sus etiquetas (Zhang et al., 2018), mejora generalización.

**Overfitting (sobreajuste).** Cuando el modelo memoriza el train set y no generaliza al test. Detectable por gap creciente entre train y val accuracy.

**Precision.** TP / (TP + FP). De lo que predije como X, ¿cuánto era realmente X?

**Recall (sensibilidad).** TP / (TP + FN). De lo que era X, ¿cuánto detecté?

**ResNet (Residual Network).** Arquitectura CNN con bloques residuales y_l+1 = x_l + F(x_l), permite entrenar redes muy profundas sin vanishing gradient (He et al., 2016).

**ROC curve.** Receiver Operating Characteristic. Gráfico de TPR vs FPR a distintos umbrales.

**Shortcut learning.** Fenómeno donde un modelo aprende correlaciones espurias en lugar de la señal real (Geirhos et al., 2020). Detectable con Grad-CAM. Documentado en este proyecto durante smoke-test con dataset sintético.

**Softmax.** Función de activación final en clasificación multiclase, transforma logits en distribución de probabilidad. softmax(zᵢ) = e^zᵢ / Σ e^zⱼ.

**Stratified K-Fold.** Validación cruzada que mantiene proporciones de clase en cada fold.

**Top-3 accuracy.** Porcentaje de casos donde la clase correcta está entre las 3 predicciones más probables. Complementa la accuracy estándar.

**Transfer learning.** Estrategia de inicializar un modelo con pesos aprendidos en una tarea (típicamente ImageNet) y adaptarlo a una tarea relacionada con menos datos.

**VRAM (Video RAM).** Memoria de la GPU. Limita el tamaño de batch y de modelo. RTX 3050 Laptop tiene ~4.3 GB.

---

## C — Lingüística de Señas y Accesibilidad

**ASL (American Sign Language).** Lengua de señas dominante en Estados Unidos y partes de Canadá.

**Comunidad Sorda.** Grupo cultural-lingüístico de personas sordas (con S mayúscula como reconocimiento de identidad cultural). Distinto de "personas con sordera" (perspectiva médica).

**DUA / UDL (Diseño Universal para el Aprendizaje).** Marco pedagógico que diseña materiales accesibles desde el inicio, no como adaptación posterior (CAST, 2018).

**Iconicidad.** Grado en que una seña visualmente representa lo que significa. Las señas zoológicas tienden a ser altamente icónicas (forma del animal, movimiento característico).

**International Sign (IS).** Sistema pidgin de comunicación entre personas sordas de distintas lenguas de señas. No es una lengua propiamente dicha pero tiene gramática emergente. Usado en eventos internacionales.

**LSM (Lengua de Señas Mexicana).** Lengua oficial de la comunidad sorda mexicana, reconocida desde 2005. Distinta de ASL y de la lengua de señas española.

**Hablante nativo de señas.** Persona que aprendió una lengua de señas como primera lengua (típicamente persona sorda con padres sordos o expuestos a la comunidad desde la infancia).

**HamNoSys.** Sistema de notación para lenguas de señas, similar a transcripción fonética para idiomas hablados.

**Co-creación.** Metodología de diseño donde miembros de la comunidad afectada participan activamente en la creación, no como sujetos sino como autores. Kusters & De Meulder (2019).

**WFD (World Federation of the Deaf).** Organización internacional que representa a las comunidades sordas. Promueve el uso de IS en contextos transnacionales.

---

## D — Acrónimos del Proyecto

| Acrónimo | Significado |
|----------|-------------|
| AOS | American Ornithological Society |
| API | Application Programming Interface |
| AUC | Area Under the Curve |
| AVE | Aves Verdaderas (Neornithes) |
| SSHA, SWHA, TUVU, etc. | Códigos de cuatro letras alineados con el catálogo de 53 especies |
| CC | Creative Commons |
| CDPD | Convención sobre los Derechos de las Personas con Discapacidad (ONU, 2006) |
| CNN | Convolutional Neural Network |
| DMP | Data Management Plan |
| DOI | Digital Object Identifier |
| DUA / UDL | Diseño Universal para el Aprendizaje |
| F1 | F1-score (métrica) |
| FAIR | Findable, Accessible, Interoperable, Reusable |
| IS | International Sign |
| LSM | Lengua de Señas Mexicana |
| MAX_PATH | Límite de longitud de ruta en Windows (260 caracteres) |
| OE | Objetivo Específico |
| OMS | Organización Mundial de la Salud |
| ONU | Organización de las Naciones Unidas |
| PAT | Personal Access Token (GitHub) |
| ROC | Receiver Operating Characteristic |
| RTX | Línea de GPU NVIDIA con capacidades de Ray Tracing |
| TPR / FPR | True Positive Rate / False Positive Rate |
| UNESCO | Organización de las Naciones Unidas para la Educación, la Ciencia y la Cultura |
| WFD | World Federation of the Deaf |

---

*Glosario en construcción. Se actualiza conforme se introducen nuevos términos en la tesis.*
