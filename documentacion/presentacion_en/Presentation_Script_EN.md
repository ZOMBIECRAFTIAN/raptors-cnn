# Presentation script - English (word-by-word)

**Project:** Raptor Identification by Silhouette and Flight Behaviour using AI, with International Sign accessibility.
**Speaker:** Brian Fernandez Baez.
**Audience:** US-based professor, evaluating viability for a master's program.
**Date:** Friday June 12, 2026, 7:00 am.
**Estimated duration:** 25-28 minutes + Q&A.

---

## How to use this script

Each slide section has:

1. **(EN)** the exact English to speak, in plain delivery English (140 words / minute).
2. **(ES)** a Spanish translation so you can verify you understand what you are saying.
3. **(Tip)** a short stage direction (when to pause, what to emphasise).

Pronunciation guide for hard scientific names is in `Pronunciation_Guide_EN.md` (sibling file).

---

## SLIDE 1 - Title

**(EN)** Good morning, and thank you for taking the time to meet with me. My name is Brian Fernandez Baez, and I am a master's candidate from Mexico. The project I want to share with you today is called *Raptor Identification by Silhouette and Flight Behaviour using Artificial Intelligence*. It is an integrated computer-vision system for the fifty-three diurnal raptor species of Mexico, and it includes a parallel catalogue of fifty-three signs in International Sign so that the Deaf community can also access this scientific knowledge.

**(ES)** Buenos días y gracias por su tiempo. Soy Brian Fernández Báez, candidato a maestría de México. El proyecto se titula *Identificación de Aves Rapaces por Silueta y Comportamiento de Vuelo con Inteligencia Artificial*. Es un sistema de visión por computadora para las 53 especies de rapaces diurnas de México, con un catálogo paralelo de 53 señas en International Sign para incluir a la comunidad sorda.

**(Tip)** Speak slowly. Smile. Make eye contact. This is your hook.

---

## SLIDE 2 - Agenda

**(EN)** In the next twenty-five minutes I will cover seven things. First, the problem we are solving and the two gaps it closes. Second, the research question, hypotheses and objectives that frame the work. Third, the fifty-three species we cover and how we built the dataset. Fourth, the key design decision that makes this project different - silhouette and flight behaviour, instead of plumage. Fifth, the four CNN architectures and a short code walkthrough. Sixth, the International Sign catalogue and the Flask web app that integrates everything. And seventh, the expected results, the honest limitations, and the doctoral roadmap.

**(ES)** En 25 minutos cubriré siete puntos: el problema y sus dos brechas; la pregunta, hipótesis y objetivos; las 53 especies y la construcción del dataset; la decisión clave de silueta y vuelo; las cuatro arquitecturas y un recorrido por el código; el catálogo de señas y la app Flask; y los resultados esperados, limitaciones y la ruta doctoral.

**(Tip)** Hold up your hand and count "one, two, three..." as you list. Keeps the audience anchored.

---

## SLIDE 3 - The problem

**(EN)** Identifying raptors in the field is genuinely hard, and that difficulty is the starting point of this whole project. Look at the image on the left: this is the most common situation an observer faces. A bird in flight, far away, against bright sky. You cannot see the colours. You cannot see the eye, the beak, or the feathers. All you have is the silhouette and the way it flies. To distinguish *Astur cooperii* from *Accipiter striatus* by the cadence of the wingbeat alone takes a trained ornithologist years of practice. And just in the Veracruz corridor of Mexico, more than five million raptors fly through each autumn. There is no human expert force that can scale to that volume.

**(ES)** Identificar rapaces en campo es realmente difícil. La imagen muestra el escenario típico: ave en vuelo, lejos, a contraluz. No ves color, ni ojo, ni plumaje. Solo silueta y forma de volar. Diferenciar *Astur cooperii* de *Accipiter striatus* por el aleteo lleva años de práctica. En el corredor de Veracruz pasan más de cinco millones de rapaces cada otoño y no hay expertos suficientes para esa escala.

**(Tip)** Pause after "More than five million birds per autumn." That number lands hard.

---

## SLIDE 4 - The two gaps

**(EN)** This complexity creates two gaps. The first is *epistemic*: the practical knowledge of how to identify a raptor in two seconds lives in the head of expert ornithologists. It has never been turned into a shared, computational tool that beginners or citizen-science volunteers can use. The second is *accessibility*: existing field guides assume hearing readers and audio-based learning. Deaf naturalists are essentially excluded from raptor identification because there is no signed vocabulary for these species. No catalogue in the world covers fifty-three raptor species in International Sign. This project closes both gaps simultaneously.

**(ES)** Esa dificultad genera dos brechas. Una epistémica: el conocimiento práctico vive en la cabeza de expertos y nunca se ha sistematizado en una herramienta accesible. Y una de accesibilidad: las guías asumen audición, y la comunidad sorda queda excluida porque no existe vocabulario en lengua de señas para rapaces. Este proyecto cierra ambas brechas al mismo tiempo.

**(Tip)** Use the word "simultaneously" with weight. It signals you are doing two non-trivial things at once.

---

## SLIDE 5 - Research question

**(EN)** This is the research question that drives the work. *Can we build a computational system that identifies the fifty-three diurnal raptor species of Mexico from their silhouette in flight, complemented by short-video behaviour analysis, accompanied by a catalogue of fifty-three signs in International Sign co-created with the Deaf community, reaching expert-level accuracy and meeting Universal Design for Learning principles?* It is intentionally one long sentence. Each clause maps to one objective.

**(ES)** Esta es la pregunta. Es una sola oración larga: ¿podemos construir un sistema que identifique las 53 rapaces de México desde la silueta, con análisis de video, con un catálogo de señas co-creado con la comunidad sorda, alcanzando nivel experto y cumpliendo principios de Diseño Universal para el Aprendizaje? Cada cláusula corresponde a un objetivo.

**(Tip)** Read the quotation slowly. Do not summarise. Let the question land.

---

## SLIDE 6 - Three hypotheses

**(EN)** The question becomes three testable hypotheses. *H1*, the technical one: a CNN with transfer learning over four state-of-the-art architectures will reach an F1-macro of at least zero point eight on silhouette-in-flight classification, given a minimum of one hundred images per class. *H2*, the novel claim: adding a temporal behaviour module that measures flap frequency, soaring, and kettle formation reduces confusion between difficult species pairs by at least fifteen percent compared to the static-image model. And *H3*, the inclusive claim: a catalogue of fifty-three International Sign signs, co-designed with the Deaf community, will score at least four out of five in clarity, naturalness, and memorability on a Likert scale.

**(ES)** Tres hipótesis: H1, una CNN con transfer learning sobre cuatro arquitecturas alcanza F1-macro >= 0.80 con >= 100 imágenes por clase. H2, agregar un módulo temporal reduce errores en pares confusos al menos 15%. H3, el catálogo de 53 señas obtiene >= 4.0/5 en claridad, naturalidad y memorabilidad.

**(Tip)** Point with your finger at H1, H2, H3 on screen. Physical cue helps the audience follow.

---

## SLIDE 7 - Objectives

**(EN)** The general objective is to develop one integrated AI system for the fifty-three species, fully reproducible and accessible. It breaks into five specific objectives. One: curate a balanced dataset using iNaturalist, Macaulay Library, eBird and CONABIO. Two: train and compare four CNN architectures, with Grad-CAM for interpretability. Three: design the short-video flight-behaviour module as a Bayesian prior. Four: co-design and validate the fifty-three International Sign signs with the Deaf community. Five: deploy a Flask web app with active learning and Darwin Core export to iNaturalist and GBIF.

**(ES)** Objetivo general: un sistema integrado para las 53 especies, reproducible y accesible. Cinco específicos: curar el dataset; entrenar y comparar 4 CNNs con Grad-CAM; diseñar el módulo de vuelo como prior bayesiano; co-diseñar 53 señas; desplegar la app Flask con active learning y exportación Darwin Core.

**(Tip)** This slide is dense. Read at slightly higher pace and don't elaborate unless asked.

---

## SLIDE 8 - 53 species

**(EN)** Why fifty-three? Because that is the complete list of diurnal raptors documented in Mexico under the AOS check-list, twenty twenty-four edition. They split across four families: thirty-eight in Accipitridae, ten in Falconidae, four in Cathartidae - the New World vultures - and one Pandionidae, the Osprey. The list includes three recent reclassifications from the American Ornithological Society: *Accipiter cooperii* became *Astur cooperii*; *Accipiter gentilis* in the Americas became *Astur atricapillus*; and *Buteo nitidus* split into *Buteo plagiatus*. Five of the fifty-three are IUCN-listed or considered endangered in Mexico.

**(ES)** Las 53 son todas las rapaces diurnas de México según el AOS 2024. Cuatro familias: 38 Accipitridae, 10 Falconidae, 4 Cathartidae, 1 Pandionidae. Incluye 3 reclasificaciones AOS 2023 y 5 especies en estatus de conservación.

**(Tip)** Pronounce the scientific names slowly. If unsure, see `Pronunciation_Guide_EN.md`.

---

## SLIDE 9 - Why silhouette + flight

**(EN)** This is the most important design decision in the entire project, so I want to spend a moment here. The existing tools - Merlin Bird ID, iNaturalist - are excellent, but they are trained on perched birds with rich colour photographs. Plumage colour drives the prediction. That is fine for songbirds in a backyard, but it fails when a raptor is in flight against bright sky. Our approach is the opposite: we train *on* the silhouette in flight, with reduced colour information. The diagnostic features are wing chord ratio, wingtip shape, tail outline, and head proportion. Our augmentation pipeline actively strips saturation, forces grayscale, and erases plumage regions, so the model is forced to learn shape and contour rather than colour. We add a second module that classifies five flight modes from a thirty-second video at one frame per second. The result is a system that mimics how a human expert decides in two seconds, not in two minutes of zooming into the feathers.

**(ES)** La decisión clave. Las herramientas existentes usan plumaje. Eso falla con rapaces en vuelo. Nosotros entrenamos sobre silueta, quitando saturación, forzando grises y borrando regiones de plumaje. El modelo aprende forma, no color. Más un módulo de video que clasifica 5 modos de vuelo. Imita cómo decide un experto en dos segundos.

**(Tip)** This is your differentiator. Speak with conviction. Pause after "wing chord ratio, wingtip shape, tail outline, and head proportion."

---

## SLIDE 10 - Dataset pipeline

**(EN)** The dataset is built in five stages. *Source*: we pull from iNaturalist, Macaulay Library, eBird, and CONABIO, restricted to Creative Commons licences. *Download*: per-species, paged, including old taxonomic synonyms because some APIs have not yet adopted the AOS twenty twenty-four updates. *Curate*: an automatic Python script called `curate.py` evaluates each image for resolution, sharpness using variance of Laplacian, brightness, and perceptual hash for deduplication. *Annotate*: anything marginal goes through double annotation by two independent reviewers, and we require a Cohen's kappa of at least zero point eight five. *Split*: seventy / fifteen / fifteen percent for train, validation, and test, stratified by species, with a fixed random seed of forty-two. Total: roughly ten thousand six hundred images, three gigabytes, fifty-three classes, targeting two hundred images per species.

**(ES)** Cinco etapas: Source (4 fuentes CC), Download (con sinónimos), Curate (script automático), Annotate (doble anotación + kappa >= 0.85), Split (70/15/15 estratificado, seed 42). Total: ~10 600 imágenes, ~3 GB.

**(Tip)** "Cohen's kappa" sounds like "Co-hen's KAH-pa." Confidence on the technical terms matters.

---

## SLIDE 11 - Curate.py

**(EN)** I want to show you the quality curation in a bit more detail, because it is one of the parts I am most proud of. Every image gets a score from zero to one hundred based on five criteria: resolution, sharpness measured by Laplacian variance, brightness penalising under-exposed and over-exposed images, aspect ratio penalising thin strips, and a perceptual hash for finding duplicates across pages. Based on the score, the image is classified into one of three outcomes: *KEEP* goes straight to the training pool; *REVIEW* is borderline and requires double annotation; and *DISCARD* is moved to a side folder, never deleted, so we can audit every decision. The Cohen's kappa floor of zero point eight five corresponds to "almost perfect agreement" in the Landis and Koch nineteen seventy-seven scale.

**(ES)** La curación califica cada imagen de 0 a 100 por resolución, nitidez (Laplaciano), brillo, aspecto y phash. Tres salidas: KEEP, REVIEW, DISCARD. Nada se borra. Kappa >= 0.85 es "casi perfecto" según Landis & Koch 1977.

**(Tip)** Project pride here - this is a technical contribution.

---

## SLIDE 12 - Augmentations

**(EN)** Standard augmentations we apply: random crops, horizontal flips, mild rotations, colour jitter, ImageNet normalisation, Mixup with alpha zero point two, and CutMix with alpha one. These are textbook. The interesting part is the second row - the silhouette-targeted augmentations. We jitter saturation up to forty percent, randomly convert to grayscale with a probability of zero point two, and apply RandomErasing on plumage regions. The combined effect is that the model literally cannot rely on plumage colour to win. It has to learn shape, proportion, and contour - the same features an expert uses.

**(ES)** Augmentaciones estándar más una capa especial: saturación, grises aleatorio y RandomErasing sobre plumaje. El modelo no puede ganar con color, solo con forma.

**(Tip)** "Cannot rely on plumage colour to win" - say this slowly. It's the punch line.

---

## SLIDE 13 - Four architectures

**(EN)** The four architectures we benchmark are intentionally diverse. MobileNetV3-Large is the lightweight option, five point five million parameters, designed for mobile and edge deployment. EfficientNet-B3 is twelve million parameters with the best accuracy-per-parameter ratio. ResNet-fifty is our baseline at twenty-five point six million parameters - it is the model most reported in the ornithological AI literature since two thousand eighteen. And ConvNeXt-Tiny at twenty-eight point six million parameters represents the twenty twenty-two state-of-the-art that closes the gap with vision transformers. All four train on the same split, with the same augmentations, the same two-stage transfer learning protocol. We report F1-macro per species and the Pareto trade-off between accuracy and latency. The script that runs the whole comparison is `comparar_arquitecturas.py` and it produces the CSV and the Pareto plot automatically.

**(ES)** Cuatro arquitecturas: MobileNetV3 (móvil), EfficientNet-B3 (mejor ratio), ResNet-50 (baseline maduro), ConvNeXt-Tiny (SOTA 2022). Mismo split, mismo entrenamiento. Script automático produce CSV y plot de Pareto.

**(Tip)** Mention `comparar_arquitecturas.py` casually. It signals real engineering, not slides only.

---

## SLIDE 14 - Two-stage training

**(EN)** Training uses a two-stage transfer-learning recipe. Stage one is feature extraction: backbone frozen, only the classifier head trains. Adam optimiser, learning rate of one times ten to the minus three, ten epochs. The goal is just to stabilise the head before we risk touching the pre-trained backbone weights. Stage two is fine-tuning: all layers unfrozen, AdamW optimiser, learning rate one times ten to the minus four, weight decay five times ten to the minus four. We use cosine annealing with three warm-up epochs. Label smoothing of zero point one, Mixup with alpha zero point two, CutMix with alpha one. Eighty epochs maximum with early stopping patience of fifteen on validation accuracy. And weighted cross-entropy to mitigate the class imbalance between common species like *Cathartes aura* with over a thousand images, and rare ones like *Harpia harpyja* with around sixty.

**(ES)** Dos etapas: Stage 1, cabeza solamente, Adam lr 1e-3, 10 epochs. Stage 2, todo descongelado, AdamW lr 1e-4, weight decay 5e-4, cosine annealing con 3 warm-up, label smoothing 0.1, Mixup 0.2, CutMix 1.0, 80 epochs con early stopping 15. Cross-entropy ponderada para desbalance.

**(Tip)** Be ready for "why two stages?" - answer: "to avoid catastrophic forgetting of the pre-trained features."

---

## SLIDE 15 - Code walkthrough

**(EN)** I want to show one piece of real code, because all the hyperparameters and design choices we just discussed live in one file: `config.py`. The constants `SPECIES`, `BATCH_SIZE`, `INPUT_SIZE` are shared by every script - training, evaluation, Grad-CAM. The device detection function on the right is small but important: it auto-detects NVIDIA CUDA, Apple's MPS for M-series Macs, or falls back to CPU. So the same code runs unchanged on my RTX three thousand fifty in Mexico, on a Mac with Apple Silicon, and on a server without a GPU. Mixed precision and gradient accumulation let me train on a four-gigabyte VRAM GPU at an effective batch of thirty-two. And weighted cross-entropy plus Mixup and CutMix mitigate the imbalance between common and rare species. Four lines of design wisdom in one file.

**(ES)** Un archivo `config.py` concentra hiperparámetros y configuración. La detección de dispositivo auto-decide CUDA, MPS o CPU sin tocar código. AMP + grad accumulation me dan batch efectivo 32 en 4 GB. Cross-entropy ponderada y Mixup/CutMix manejan el desbalance.

**(Tip)** Don't read every line. Point at the device function and say "this is the multi-platform trick."

---

## SLIDE 16 - Flight behaviour

**(EN)** Now the temporal module - the novel contribution. The pipeline has six steps. We sample frames at one frame per second from a clip of thirty seconds or less. We detect the bird using Faster R-CNN restricted to the COCO "bird" class. We crop with a five percent margin and classify each crop using the CNN from slide thirteen. We extract quantitative descriptors: flap frequency via Fourier transform on the bounding-box height, altitude gain rate from bounding-box scale change, and kettle count. Then a lightweight CNN-LSTM classifies sixteen frames into one of five flight modes: soaring, flap-glide, hovering, active flapping, or stoop. Finally, we combine the visual prediction and the behaviour prediction using Bayes' rule. The posterior probability of a species given the image and the behaviour is proportional to the visual likelihood times the conditional probability of that behaviour given the species. The measurable effect is that confusing pairs - like *Buteogallus anthracinus* versus *Buteogallus urubitinga* - get untangled when the behaviour prior is added.

**(ES)** El módulo de comportamiento tiene seis pasos: muestrear frames, detectar con Faster R-CNN, recortar, clasificar, extraer descriptores cuantitativos, clasificar el modo de vuelo con CNN-LSTM, y combinar con Bayes. Efecto medible: pares confusos como los Buteogallus se separan al agregar el prior de comportamiento.

**(Tip)** This is hypothesis two in action. If the professor lights up, you have made the sale.

---

## SLIDE 17 - Grad-CAM

**(EN)** A model that gets ninety-five percent test accuracy is not enough by itself. We need to verify *why* it gets that accuracy. Grad-CAM - Gradient-weighted Class Activation Mapping - tells us which pixels the model relied on to make its decision. On the right is a representative output for *Buteo platypterus*. The heat zones - red and yellow - land on the wingtip and tail outline, which are the actual diagnostic features that field guides recommend. We manually inspect at least twenty Grad-CAM maps per class, and any sample where the attention falls on sky or trees instead of the bird fails an audit. This is what interpretability means here: not just a number, but visible evidence that the model learned the right thing.

**(ES)** Grad-CAM muestra los píxeles que el modelo usó. El mapa cae sobre punta de ala y cola, las features diagnósticas correctas. Auditamos >= 20 mapas por clase. Si la atención está en cielo o árboles, el sample falla la auditoría.

**(Tip)** "Visible evidence that the model learned the right thing" - this is your closing line for this slide.

---

## SLIDE 18 - International Sign

**(EN)** The fifty-three signs in International Sign are co-designed in three iterations. First iteration: I propose an initial sign based on diagnostic morphology - the crest, the tail shape, the typical behaviour. Second iteration: a focus group of IS users from the Deaf community refines the sign together with me. Third iteration: each sign is validated with a Likert questionnaire on three dimensions - clarity, naturalness, and memorability - with a minimum threshold of four out of five. We also run a retention test: after a ten-minute break, the participant sees fourteen random sign videos and identifies the species. The whole protocol is grounded in the World Federation of the Deaf manifesto on International Sign and the CAST framework for Universal Design for Learning. To my knowledge there is no other biodiversity catalogue with this scope and rigor in any signed language.

**(ES)** 53 señas co-diseñadas en tres iteraciones: propuesta, refinamiento con grupo focal sordo, validación Likert >= 4.0 más test de retención. Protocolo basado en el manifiesto WFD sobre IS y CAST sobre UDL. No existe otro catálogo de biodiversidad de este alcance en lengua de señas.

**(Tip)** Slow down on this slide. The professor in the US likely cares about accessibility deeply.

---

## SLIDE 19 - Flask GUI

**(EN)** All of this comes together in a Flask web application. The user drops an image or a short video. They get a top-three prediction with confidence bars, a Grad-CAM overlay, a Merlin-style species fact sheet with length, wingspan, diet, IUCN status and Mexico's NOM-zero five nine status, a video of the International Sign for the predicted species, and a citizen-science form to record their observation with optional coordinates. The observation can be exported in Darwin Core format directly to iNaturalist or GBIF. The app is bilingual Spanish and English and works with full keyboard navigation. The mock on the right is a real screenshot.

**(ES)** Flask web app. Drag-and-drop, top-3, Grad-CAM, ficha Merlin, video de seña, formulario citizen science con export Darwin Core a iNaturalist o GBIF. Bilingüe ES/EN, navegable con teclado.

**(Tip)** Offer to demo it live if you have laptop + internet. "I am happy to show you live if you'd like."

---

## SLIDE 20 - Active learning

**(EN)** The system improves over time through a controlled active-learning loop. The user uploads an image; the model predicts top-three; the user confirms or corrects the prediction; an expert annotator audits the correction; and only when fifty confirmed corrections accumulate does the system trigger an incremental retraining. The safeguard is critical: we never retrain on un-audited user corrections, because a single misinformed user could drift the model. Everything is logged for a full audit trail.

**(ES)** Active learning con safeguards: usuario sube imagen, modelo predice, usuario corrige, anotador experto audita, y solo con >= 50 confirmadas se hace retraining. No reentrenamos con correcciones no auditadas. Todo queda en log auditable.

**(Tip)** "Audit trail" is a signal phrase for academic and industrial rigour. Use it.

---

## SLIDE 21 - Reproducibility

**(EN)** Reproducibility is built in. All random seeds are fixed at forty-two. Three environment files are published: one for NVIDIA CUDA, one for CPU-only, one for Apple Silicon MPS. Each image's SHA-two-fifty-six is logged in the annotations folder. Each experiment is tagged in Git. Code is MIT licensed; data and signs are CC-BY. Every trained weight file is published per architecture. The fifty-three International Sign videos and SVG vector files are released under CC-BY with full attribution. Nothing about this project is a black box.

**(ES)** Reproducibilidad total: seeds 42, tres entornos conda, SHA-256 por imagen, Git tags, MIT y CC-BY, todos los pesos publicados. Nada es caja negra.

**(Tip)** "Nothing about this project is a black box" - say it slowly, look at the professor.

---

## SLIDE 22 - Expected results

**(EN)** What do we expect to report? Accuracy on the fifty-three-class test set of at least zero point eight. F1-macro of at least zero point eight. Top-three accuracy of zero point nine five or better. Behaviour-prior gain: a measurable fifteen percent error reduction on confused pairs. For the International Sign catalogue, Likert score of four or higher. And inference time below one second per image on a four-gigabyte RTX three thousand fifty. We also report the fifty-three by fifty-three confusion matrix, per-species F1, and the Pareto plot of accuracy versus latency. These are not promises - they are the contractual targets that defend the hypotheses.

**(ES)** Targets: accuracy >= 0.80, F1-macro >= 0.80, top-3 >= 0.95, ganancia por behaviour >= 15%, Likert IS >= 4.0, inferencia < 1 s. Matriz 53x53, F1 por especie y Pareto. Son los objetivos que defienden las hipótesis.

**(Tip)** "Contractual targets" is a strong phrase. It says "I am held accountable to these numbers."

---

## SLIDE 23 - Limitations

**(EN)** I want to be honest about four limitations. First, class imbalance: *Cathartes aura* has over a thousand images, *Harpia harpyja* has about sixty. Even with weighted loss and Mixup, the rare species under-perform. We plan to address this with synthetic minority oversampling and a formal partnership with The Peregrine Fund's Mesoamerican programme. Second, iNaturalist photo bias: most uploads are clear-sky soaring birds. The model under-performs on canopy backgrounds typical of tropical Spizaetus and Harpagus. Camera-trap imagery is the V two solution. Third, temporal resolution: at one frame per second we cannot capture the *Falco peregrinus* stoop, which can exceed three hundred kilometres per hour in less than three seconds. The V two answer is a 3D-CNN at eight to sixteen frames per second. Fourth, the geographic prior can introduce confirmation bias: the model is more likely to predict a Buteogallus in tropical regions even when a young Spizaetus is present. We will weight the prior by visual classifier uncertainty in V two.

**(ES)** Cuatro limitaciones honestas: desbalance de clases; sesgo de fotos iNaturalist; resolución temporal a 1 fps; riesgo del prior geográfico. Cada una con su plan de mitigación en V2.

**(Tip)** Showing limitations builds trust. Don't apologise - explain calmly.

---

## SLIDE 24 - Roadmap V2

**(EN)** The doctoral roadmap. V two has five components. One: a 3D-CNN end-to-end - ResNet3D-eighteen or SlowFast - trained directly on short clips, no longer dependent on the two-D classifier. Two: DeepSORT for individual tracking across frames, so we can aggregate behaviour per bird. Three: a dedicated flight-mode classifier with flap frequency in Hertz, altitude gain in metres per second, and thermal radius. Four: a full multimodal Bayesian fusion of vision, behaviour, phenology and geography at the posterior level. And five: expansion to Strigiformes - the owls - approximately thirty more species, which would also require night-vision and audio modalities.

**(ES)** V2 doctoral: 3D-CNN end-to-end; DeepSORT tracker; clasificador de vuelo con Hz, m/s, radio térmica; fusión bayesiana multimodal completa; expansión a Strigiformes (~30 búhos) que añadiría modalidades nocturna y audio.

**(Tip)** This is the slide where the professor decides "this is PhD-worthy." Speak with vision.

---

## SLIDE 25 - PhD positioning

**(EN)** Why is this work master's-into-PhD material? Three original contributions. One: a silhouette-first identification approach in a literature that is otherwise dominated by plumage-based models. Two: an end-to-end Bayesian fusion of static visual classification with quantitative flight-behaviour priors, which to my knowledge has not been published for raptors. Three: the first validated International Sign vocabulary of any biodiversity domain. Any one of these would be a publishable contribution. Together, they define a research program.

**(ES)** Tres contribuciones originales: identificación por silueta (no plumaje); fusión bayesiana de visión + comportamiento; primer vocabulario IS validado en biodiversidad. Cualquiera publicable; juntas, un programa de investigación.

**(Tip)** "They define a research program" - this is your closing argument. Say it slowly.

---

## SLIDE 26 - Thank you / Q&A

**(EN)** Thank you very much for your attention. The code, the dataset structure, the manuals and the thesis chapters are all on the public GitHub repository under MIT and CC-BY licences. My email is on the slide. I would be very glad to answer any questions or take feedback on what you think is the strongest or the weakest part of the project, and to discuss whether this fits the program you have in mind.

**(ES)** Gracias por su atención. Todo está en GitHub bajo MIT y CC-BY. Estoy disponible para preguntas, sugerencias y para conversar si este proyecto encaja en el programa.

**(Tip)** Pause. Smile. Look at the professor. Then say "I am ready for your questions."

---

## Closing tips

- **Practice three times out loud.** Time yourself. Aim for 25 minutes.
- **Record yourself once.** Listen for words you mispronounce.
- **Memorise the first slide and the last slide verbatim.** Improvise the middle.
- **Slow down.** Non-native English in technical talk reads as smart when slow, rushed when fast.
- **Always pause after a number.** "Five million birds" - then breathe - then continue.
- **Bring a printout of this script.** If you lose your place, you can recover.
- **Have water at hand.** Cold water if available.
- **For Q&A:** "That is a great question, let me think for a moment" is a perfect phrase. It buys five seconds and shows confidence.

Good luck, Brian. You will do great.
