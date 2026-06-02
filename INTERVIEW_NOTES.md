# Interview notes — `raptors-cnn`

Talking points for graduate-admissions interviews, research-fit conversations and informal pitches. **EN first, then ES** below for the same content.

> **Honesty rule.** Where a number is given, it is either (a) from the predecessor Australian raptor project (clearly labelled), or (b) preliminary on the V1 23-species subset. The 53-species results are *not* in yet and the talking points say so explicitly.

---

## 1-minute pitch (English)

> "I'm Brian Fernandez. I am building a reproducible AI pipeline that identifies the 53 diurnal raptor species of Mexico from photographs. The technical novelty is that I train deliberately on the silhouette in flight, not on plumage colour, because that is how an expert ornithologist identifies a raptor at distance. The pipeline compares four CNN architectures under the same protocol, validates interpretability with Grad-CAM to rule out shortcut learning, and ships as installable software with CUDA, CPU and Apple Silicon environment files. The predecessor Australian project from the same research program reached F1-macro of 0.85 on 8 species; the 53-species Mexican benchmark is the next deliverable. The whole thing is open source and is the basis of my master's research proposal."

## 3-minute pitch (English)

> "I'm Brian Fernandez. My research interest is computer vision applied to wildlife conservation, specifically to apex predators that are notoriously hard to identify in the field.
>
> The problem is concrete: Mexico hosts the largest raptor migration corridor in the Americas — over five million birds each autumn — but current AI tools fail in the typical observation setting. Merlin Bird ID and iNaturalist Computer Vision are trained on perched birds with rich colour photos. In the field, you almost always see a raptor in flight, far away, backlit. Plumage is invisible. An expert relies on silhouette and on flight behaviour. No published AI identifier explicitly targets that.
>
> What I built. A reproducible pipeline in PyTorch. The dataset is curated from iNaturalist, Macaulay Library and CONABIO under Creative-Commons licenses, with an automatic quality script and double annotation with a Cohen's kappa floor of 0.85. I compare four CNN architectures head to head — MobileNetV3-Large, EfficientNet-B3, ResNet-50 as baseline, ConvNeXt-Tiny — under the same split, same augmentations, same two-stage transfer learning protocol. The augmentations are designed to strip colour information — saturation jitter, random grayscale, plumage erasing — so the model must learn shape.
>
> What I validate. Accuracy and F1-macro are not enough on their own. I run a Grad-CAM audit on at least 20 images per class. If the model's attention falls on the sky or canopy instead of the bird, the image is flagged. This catches shortcut learning, which is a well-documented failure mode in deep learning.
>
> Where the project stands today. The predecessor Australian raptor project — 8 species — reached F1-macro 0.85 with EfficientNet-B4. That recipe and codebase transfer directly. The 53-species Mexican benchmark is the next deliverable. The code, the environment files, the curation scripts and the Flask demo GUI all work today. The full training run is scheduled. The results templates are public so the reproducibility expectation is set up front.
>
> Where I want to take it. The doctorate-level extension is a multimodal V2: a 3D-CNN behaviour module, a multimodal Bayesian fusion of vision plus behaviour plus geography, and the integration with a separate bioacoustic project for nocturnal taxa. That is the research direction I would love to discuss with you."

## 30-second elevator (English)

> "I'm building an open-source raptor identifier for the 53 species of Mexico. The novelty is training on silhouette rather than plumage, because that's how experts actually decide in the field. I validate interpretability with Grad-CAM to catch shortcut learning. The same recipe applied to 8 Australian raptors hit F1-macro 0.85. It's my master's research proposal."

---

## Hard questions with recommended answers

### Q1. "How do you know your model isn't memorising the dataset?"

> "Three layers. First, the test split is 15 % held out and stratified by species, never touched during training or hyperparameter selection. Second, I run a Grad-CAM audit — for each class I inspect at least 20 maps and any image where attention falls on background is logged. Third, the pipeline includes an augmentation ablation: removing the silhouette-targeted augmentations should *increase* training accuracy but *decrease* test accuracy. If it doesn't, the model is exploiting plumage as a shortcut. This protocol is documented in `results/SHORTCUT_LEARNING_FINDING.md`."

### Q2. "Why didn't you use a Vision Transformer?"

> "ViT-base needs at least 10–20× more data per class than I have for fine-grained classification. With 100–200 images per species, a ViT either underfits or overfits, depending on the warm-up. ConvNeXt-Tiny is in my benchmark and closes most of the gap to ViT with CNN-friendly compute. ViT is in the doctoral roadmap once I have synthetic-minority augmentation in place."

### Q3. "You don't have your 53-species results yet. What if accuracy lands at 0.65 instead of 0.80?"

> "It would still be a publishable result. The contribution is the framework — silhouette-focused augmentation plus Bayesian behaviour prior plus the interpretability audit — not the specific accuracy number. A 0.65 result with a clean diagnosis of why it lands there is more useful to the field than a 0.85 number reported without an audit. The Australian predecessor at F1 0.85 on 8 species gives me a calibrated expectation; if the 53-class number is much lower, the failure analysis itself is the deliverable."

### Q4. "Why two-stage training instead of just end-to-end fine-tuning?"

> "If you unfreeze the whole backbone from epoch one with a randomly initialised head, the gradient from the random head is large enough to wipe out the pre-trained features in the first few hundred steps. Stage 1 stabilises the head with the backbone frozen; Stage 2 unfreezes everything safely. This is the ULMFiT recipe from Howard and Ruder 2018. It is also the recipe that worked for the Australian project, which gives me empirical confidence beyond the original NLP paper."

### Q5. "How is this different from BirdNET or iNaturalist?"

> "BirdNET is audio. iNaturalist Computer Vision is general — covering all species with rich photographs of perched animals. Neither is designed for the raptor-in-flight case. I am specifically targeting the case where plumage is unavailable, with three concrete differences: silhouette-targeted augmentations, a flight-behaviour prior, and a Grad-CAM audit that surfaces shortcut learning. None of the three is in the published BirdNET or iNaturalist pipelines."

### Q6. "Why open-source everything?"

> "Three reasons. First, reproducibility — anyone can verify the result. Second, biodiversity infrastructure benefits when tools feed Atlas of Living Australia and GBIF through Darwin Core. Third, it is the right way to do science applied to conservation: keeping the model and the data behind a paywall would slow down the people doing the actual fieldwork."

### Q7. "What is the biggest weakness of your project today?"

> "I do not yet have the full 53-species training run. The codebase, the dataset spec, the curation scripts and the smoke tests work; the production run is the next deliverable. Second, the behaviour module is implemented as a placeholder prior, not as the full 3D-CNN. Both are honestly documented in the `Current status` section of the README. I would rather have a calibrated reader expectation than oversell what is done."

### Q8. "Will you keep working on this if you're admitted?"

> "Yes. The master's thesis is the 53-species benchmark with the V1 behaviour prior and the Grad-CAM audit. The doctoral extension is the V2 multimodal — 3D-CNN, DeepSORT, Bayesian fusion across vision, audio and geography, plus extension to Strigiformes. The bioacoustic project I have running in parallel feeds directly into the audio modality. I have already mapped the work packages."

### Q9. "Have you talked to ornithologists?"

> "Yes — Pronatura Veracruz on the migration data, CONABIO on species lists and on access to historical archives, and informally with The Peregrine Fund's Mesoamerican programme regarding rare-species photos. The list of 53 species and the AOS 2023 reclassifications come from those conversations, not from a Wikipedia scrape."

### Q10. "Why should we admit you?"

> "Because the work is real, reproducible and published openly. You can clone the repository, install the environment in any of three OS modes, run the smoke test in five minutes, and read the Grad-CAM finding. Most candidates show one paper and one notebook; I show three live projects with code, tests, documentation and a calibrated honest assessment of what is done and what is not. That is the kind of researcher I would want to supervise, and that is what I bring."

---

## Honest limitations (always disclose first if asked)

- **No peer-reviewed publication yet.** This is a research project under development.
- **53-species results not in.** The README is explicit about which numbers are from the Australian predecessor and which are TBD.
- **Behaviour module is a prior, not a full model.** Full 3D-CNN multimodal is doctoral work.
- **Class imbalance.** Rare species (Harpy Eagle, Crested Eagle, Orange-breasted Falcon) have < 100 images each.
- **iNaturalist photographic bias.** Most photos are clear-sky soaring; canopy backgrounds under-perform.
- **International Sign vocabulary is proposed, not validated.** Likert focus-group studies are scheduled, not executed.

---

## Five recovery phrases if a question is genuinely unknown

1. "That is a great question. I have not measured that directly, but my intuition is X — I'll verify and follow up."
2. "You are right — that is a documented limitation. It is in section X of the README."
3. "Honestly, I don't know yet — that experiment is in the roadmap."
4. "Let me think about that for a moment." *(three seconds of silence reads as confidence, not weakness)*
5. "Could you help me make sure I understood the question correctly?"

Any of these is better than guessing wrong.

---

# Versión en español

## Pitch de 1 minuto

> "Soy Brian Fernández. Estoy construyendo un pipeline reproducible de IA que identifica las 53 especies de rapaces diurnas de México a partir de fotografías. La novedad técnica es que entreno deliberadamente sobre la silueta en vuelo, no sobre el color del plumaje, porque así es como un ornitólogo experto identifica una rapaz a distancia. El pipeline compara cuatro arquitecturas CNN bajo el mismo protocolo, valida interpretabilidad con Grad-CAM para descartar shortcut learning, y se distribuye como software instalable con entornos para CUDA, CPU y Apple Silicon. El proyecto predecesor en Australia, dentro del mismo programa de investigación, alcanzó F1-macro de 0.85 sobre 8 especies; el benchmark mexicano de 53 especies es el siguiente entregable. Todo es open source y es la base de mi propuesta de investigación de maestría."

## Pitch de 3 minutos

> "Soy Brian Fernández. Mi interés de investigación es visión por computadora aplicada a conservación de fauna silvestre, específicamente a depredadores tope que son notoriamente difíciles de identificar en campo.
>
> El problema es concreto: México alberga el mayor corredor migratorio de rapaces de las Américas — más de cinco millones de aves cada otoño — pero las herramientas de IA actuales fallan en el escenario típico de observación. Merlin Bird ID e iNaturalist Computer Vision están entrenados con aves perchadas y fotos ricas en color. En campo casi siempre ves una rapaz en vuelo, lejos y a contraluz. El plumaje no se ve. Un experto se apoya en silueta y en comportamiento de vuelo. Ningún identificador publicado se enfoca explícitamente en eso.
>
> Lo que construí. Un pipeline reproducible en PyTorch. El dataset se cura desde iNaturalist, Macaulay Library y CONABIO bajo licencias Creative Commons, con un script de calidad automático y doble anotación con Cohen's kappa mínimo 0.85. Comparo cuatro arquitecturas — MobileNetV3-Large, EfficientNet-B3, ResNet-50 como baseline, y ConvNeXt-Tiny — bajo la misma partición, las mismas augmentaciones y el mismo protocolo de transfer learning en dos etapas. Las augmentaciones están diseñadas para retirar color — jitter de saturación, grises aleatorios, borrado de plumaje — de modo que el modelo deba aprender forma.
>
> Lo que valido. Accuracy y F1-macro no son suficientes por sí solos. Hago una auditoría Grad-CAM con al menos 20 imágenes por clase. Si la atención del modelo cae sobre el cielo o el dosel en lugar del ave, la imagen queda marcada. Esto detecta shortcut learning, un modo de falla documentado en deep learning.
>
> Dónde está hoy el proyecto. El proyecto predecesor en Australia — 8 especies — alcanzó F1-macro de 0.85 con EfficientNet-B4. Esa receta y código transfieren directamente. El benchmark mexicano de 53 especies es el siguiente entregable. El código, los entornos, los scripts de curación y la GUI Flask funcionan hoy. El entrenamiento completo está agendado. Las plantillas de resultados están públicas para que la expectativa de reproducibilidad esté clara de entrada.
>
> Hacia dónde quiero llevarlo. La extensión de nivel doctoral es un V2 multimodal: módulo de comportamiento basado en CNN 3D, fusión bayesiana multimodal de visión + comportamiento + geografía, e integración con un proyecto bioacústico paralelo para taxa nocturnos. Esa es la dirección que me encantaría discutir con usted."

## Elevator de 30 segundos

> "Estoy construyendo un identificador de rapaces open source para las 53 especies de México. La novedad es entrenar sobre silueta en lugar de plumaje, porque así deciden los expertos en campo. Valido interpretabilidad con Grad-CAM para detectar shortcut learning. La misma receta aplicada a 8 rapaces australianas alcanzó F1-macro 0.85. Es mi propuesta de investigación de maestría."

## Preguntas difíciles con respuestas recomendadas

### P1. "¿Cómo sabe que su modelo no está memorizando el dataset?"

> "Tres capas. Primero, la partición de prueba es 15 % retenido, estratificado por especie, nunca tocado durante entrenamiento o selección de hiperparámetros. Segundo, hago una auditoría Grad-CAM — para cada clase reviso al menos 20 mapas y cualquier imagen donde la atención cae en fondo queda registrada. Tercero, el pipeline incluye una ablación de augmentaciones: quitar las augmentaciones de silueta debería *aumentar* la accuracy de entrenamiento pero *disminuir* la de prueba. Si no lo hace, el modelo está explotando plumaje como atajo. El protocolo está en `results/SHORTCUT_LEARNING_FINDING.md`."

### P2. "¿Por qué no usó un Vision Transformer?"

> "ViT-base necesita 10 a 20 veces más datos por clase de los que tengo para clasificación fine-grained. Con 100 a 200 imágenes por especie, un ViT subentrena o sobreajusta según el warm-up. ConvNeXt-Tiny está en mi benchmark y cubre la mayor parte del gap con cómputo amigable a CNN. ViT está en el roadmap doctoral una vez que tenga sobremuestreo sintético de la minoría."

### P3. "Aún no tiene los resultados de las 53 especies. ¿Y si la accuracy queda en 0.65 en lugar de 0.80?"

> "Sigue siendo un resultado publicable. La contribución es el marco — augmentación enfocada en silueta más prior bayesiano de comportamiento más auditoría de interpretabilidad — no el número de accuracy específico. Un resultado de 0.65 con un diagnóstico limpio de por qué cae ahí es más útil para el campo que un 0.85 reportado sin auditoría. El predecesor australiano con F1 0.85 sobre 8 especies me da una expectativa calibrada; si el número de 53 clases es mucho menor, el análisis de fallo es en sí el entregable."

### P4. "¿Por qué entrenamiento en dos etapas en lugar de fine-tuning end-to-end?"

> "Si descongelas el backbone desde el epoch uno con una cabeza inicializada aleatoriamente, el gradiente de la cabeza aleatoria es lo suficientemente grande para borrar las features preentrenadas en los primeros pasos. La Etapa 1 estabiliza la cabeza con el backbone congelado; la Etapa 2 descongela todo de manera segura. Es la receta ULMFiT de Howard & Ruder 2018. También es la receta que funcionó en el proyecto australiano, lo que me da confianza empírica más allá del paper original de NLP."

### P5. "¿Cómo es diferente esto de BirdNET o iNaturalist?"

> "BirdNET es audio. iNaturalist Computer Vision es general — cubre todas las especies con fotos ricas de animales perchados. Ninguno está diseñado para el caso de rapaz en vuelo. Yo apunto específicamente al caso donde el plumaje no está disponible, con tres diferencias concretas: augmentaciones enfocadas en silueta, un prior de comportamiento de vuelo y una auditoría Grad-CAM que detecta shortcut learning. Ninguna de las tres está en los pipelines publicados de BirdNET o iNaturalist."

### P6. "¿Por qué todo open source?"

> "Tres razones. Reproducibilidad: cualquiera puede verificar el resultado. Infraestructura de biodiversidad: las herramientas se benefician cuando alimentan Atlas of Living Australia y GBIF vía Darwin Core. Tercera, es la manera correcta de hacer ciencia aplicada a conservación: dejar el modelo y los datos detrás de un paywall frenaría a las personas que hacen el trabajo de campo."

### P7. "¿Cuál es la mayor debilidad de su proyecto hoy?"

> "Todavía no tengo el run completo de 53 especies. El código, la especificación del dataset, los scripts de curación y los smoke tests funcionan; el run de producción es el siguiente entregable. Segundo, el módulo de comportamiento está implementado como prior placeholder, no como CNN 3D completo. Ambas cosas están documentadas honestamente en la sección `Current status` del README. Prefiero una expectativa calibrada del lector que vender más de lo que está hecho."

### P8. "¿Va a seguir trabajando en esto si lo admitimos?"

> "Sí. La tesis de maestría es el benchmark de 53 especies con el prior de comportamiento V1 y la auditoría Grad-CAM. La extensión doctoral es el V2 multimodal — CNN 3D, DeepSORT, fusión bayesiana entre visión, audio y geografía, y extensión a Strigiformes. El proyecto bioacústico que tengo en paralelo alimenta directamente la modalidad de audio. Los work packages ya están mapeados."

### P9. "¿Ha hablado con ornitólogos?"

> "Sí — Pronatura Veracruz sobre datos de migración, CONABIO sobre listas de especies y acceso a archivos históricos, e informalmente con el programa mesoamericano de The Peregrine Fund respecto a fotos de especies raras. La lista de 53 especies y las reclasificaciones AOS 2023 vienen de esas conversaciones, no de un scrape de Wikipedia."

### P10. "¿Por qué deberíamos admitirlo?"

> "Porque el trabajo es real, reproducible y publicado abiertamente. Pueden clonar el repositorio, instalar el entorno en cualquiera de los tres modos de SO, correr el smoke test en cinco minutos y leer el hallazgo de Grad-CAM. La mayoría de candidatos muestra un paper y un notebook; yo muestro tres proyectos vivos con código, tests, documentación y una evaluación honesta calibrada de lo hecho y lo no hecho. Eso es el tipo de investigador que yo querría supervisar, y eso es lo que traigo."

## Limitaciones honestas (siempre revelarlas primero si preguntan)

- **Sin publicación arbitrada aún.** Es un proyecto de investigación en desarrollo.
- **Resultados de 53 especies pendientes.** El README es explícito sobre cuáles números son del predecesor australiano y cuáles están TBD.
- **El módulo de comportamiento es un prior, no un modelo completo.** El V2 multimodal completo es trabajo doctoral.
- **Desbalance de clases.** Especies raras (Águila Arpía, Águila Monera, Halcón Pechirrufo) tienen menos de 100 imágenes cada una.
- **Sesgo fotográfico de iNaturalist.** La mayoría son cielos despejados con planeo; fondos de dosel subrendirán.
- **El vocabulario en International Sign está propuesto, no validado.** Estudios Likert con grupos focales están agendados, no ejecutados.

## Cinco frases de recuperación si una pregunta es genuinamente desconocida

1. "Esa es una gran pregunta. No lo he medido directamente, pero mi intuición es X — lo verifico y le doy seguimiento."
2. "Tiene razón — esa es una limitación documentada. Está en la sección X del README."
3. "Honestamente no lo sé aún — ese experimento está en el roadmap."
4. "Permítame pensarlo un momento." *(tres segundos de silencio se leen como seguridad, no como debilidad)*
5. "¿Me ayuda a confirmar que entendí bien la pregunta?"

Cualquiera de las cinco es mejor que adivinar mal.
