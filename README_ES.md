<div align="center">

# raptors-cnn

### Pipeline reproducible de IA para identificación de rapaces mediante silueta, comportamiento de vuelo y aprendizaje profundo

**Propuesta de investigación de maestría — trabajo en curso — Brian Fernandez Baez — 2026**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![PyTorch 2.3](https://img.shields.io/badge/PyTorch-2.3-EE4C2C.svg?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![CUDA 12.1](https://img.shields.io/badge/CUDA-12.1-76B900.svg?logo=nvidia&logoColor=white)](https://developer.nvidia.com/cuda-toolkit)
[![Status: research preview](https://img.shields.io/badge/status-research%20preview-orange.svg)]()
[![Cite this](https://img.shields.io/badge/cite-CITATION.cff-informational.svg)](CITATION.cff)

[English](README.md) · [Notas de entrevista](INTERVIEW_NOTES.md) · [Manual de instalación](MANUAL_INSTALACION.md)

</div>

> **Acerca de este repositorio.** Este es un **proyecto de investigación en curso**, no una tesis terminada. El código, la especificación del dataset, las arquitecturas, el protocolo de evaluación y los experimentos planificados son públicos para que el trabajo pueda revisarse y reproducirse desde cero. Las secciones de resultados marcadas como *"a completar tras el entrenamiento"* son plantillas que se sustituirán cuando los experimentos concluyan. Cuando aparezcan números, se etiqueta explícitamente su origen y fecha.

---

## 1. Resumen del proyecto

`raptors-cnn` es un prototipo de visión por computadora de calidad investigativa para identificar las **53 especies de rapaces diurnas de México** (American Ornithological Society 2024) a partir de fotografías y videos cortos. El sistema está diseñado como un **pipeline reproducible de IA**: un dataset curado, cuatro arquitecturas CNN comparadas en igualdad de condiciones, transfer learning en dos etapas, validación de interpretabilidad con Grad-CAM, una GUI web en Flask y un vocabulario abierto en International Sign que hace la herramienta accesible para naturalistas sordos.

El proyecto se desarrolla como base de una propuesta de maestría en inteligencia artificial aplicada a la conservación de fauna silvestre. Es **abierto desde el primer día**: el código está bajo licencia MIT, los datos y señas bajo CC-BY, y el log de desarrollo es público.

## 2. Problema científico

La identificación de rapaces en campo está dominada por **observaciones en vuelo**: el ave está lejos, frecuentemente a contraluz, y el color del plumaje no es visible. Herramientas existentes como **Merlin Bird ID** e **iNaturalist Computer Vision** se entrenan principalmente sobre **aves perchadas con fotografías ricas en color**, y sus predicciones dependen fuertemente de rasgos de plumaje no disponibles en avistamientos típicos de rapaces.

Un ornitólogo entrenado se apoya en cambio en la **silueta** (relación cuerda-envergadura, forma de la punta del ala, contorno de la cola, proporción cefálica) y en el **comportamiento de vuelo** (planeo, flap-glide, hovering, formación en kettle, stoop). Ningún identificador open-source publicado se enfoca explícitamente en estos rasgos.

## 3. Objetivo de investigación

Diseñar, construir y evaluar un pipeline reproducible de visión por computadora que:

- identifique las 53 especies de rapaces diurnas de México a partir de fotografías de silueta en vuelo;
- complemente el clasificador visual con un módulo temporal de comportamiento de vuelo integrado como prior bayesiano;
- valide su interpretabilidad mediante análisis Grad-CAM sobre un conjunto de prueba retenido;
- se distribuya como paquete de software instalable y multiplataforma (CUDA / CPU / Apple Silicon MPS).

**Objetivo secundario (Sección 9 — separado a propósito):** co-diseñar con la comunidad sorda un vocabulario de 53 señas en International Sign que refleje el catálogo de especies, para que el mismo conocimiento científico sea accesible sin canal auditivo. Es un entregable de inclusión; *no* constituye una contribución central de IA.

## 4. Por qué importa la identificación de rapaces

Las rapaces son **depredadores tope** y **bioindicadores** reconocidos del estado de salud de los ecosistemas (Sergio et al., *Ecological Letters*, 2008). Sus poblaciones son sensibles a pérdida de hábitat, acumulación de pesticidas y cambio climático. México alberga el mayor corredor migratorio de rapaces de las Américas — más de **cinco millones de aves** transitan el corredor del Veracruz River of Raptors cada otoño (Pronatura Veracruz, 2020). Escalar el monitoreo de campo más allá de lo que los ornitólogos pueden hacer manualmente requiere herramientas automáticas de identificación que funcionen en condiciones reales, incluyendo vuelo a gran altura contra cielo brillante.

Una identificación precisa y escalable apoya directamente:

- monitoreo post-disturbio (incendios, sequías, deforestación);
- contribuciones de ciencia ciudadana a **iNaturalist**, **eBird**, **CONABIO**, **GBIF**;
- evaluaciones de estatus de conservación para listados de IUCN y NOM-059-SEMARNAT-2010.

## 5. Dataset

| Propiedad | Especificación |
|---|---|
| Plataformas fuente | iNaturalist (research-grade), Macaulay Library, eBird, CONABIO |
| Filtro de licencia | Sólo CC0 / CC-BY / CC-BY-SA |
| Imágenes objetivo por especie | 200 (especies raras: mejor esfuerzo) |
| Resolución mínima | lado mayor ≥ 800 px (post-curación) |
| Script de curación | `codigo/pytorch/curate.py` — score 0-100 (resolución + nitidez Laplaciano + brillo + hash perceptual) |
| Calidad de anotación | Doble anotación en imágenes dudosas; Cohen κ ≥ 0.85 requerido |
| Partición | 70 / 15 / 15 entrenamiento / validación / prueba, estratificado por especie, seed = 42 |
| Procedencia | SHA-256 de cada imagen registrado en `datos/annotations/` |

La construcción del dataset se detalla en `documentacion/WORKFLOW_DATASET_REAL.md`.

## 6. Especies objetivo

**53 rapaces diurnas de México** según AOS 2024 (Cathartidae × 4 · Pandionidae × 1 · Accipitridae × 38 · Falconidae × 10). La lista completa con nombres científicos, códigos de 4 letras, estatus IUCN y NOM-059 está en `documentacion/LISTA_OFICIAL_RAPACES_MEXICO.md`. Se aplican tres reclasificaciones AOS 2023: *Accipiter cooperii* → *Astur cooperii*, *Accipiter gentilis* → *Astur atricapillus*, *Buteo nitidus* → *Buteo plagiatus*.

## 7. Metodología de IA

El pipeline aplica **transfer learning** estándar sobre backbones preentrenados en ImageNet, con augmentaciones específicamente ajustadas para forzar al modelo a aprender **silueta y forma** en lugar de color de plumaje:

- jitter de saturación hasta 0.4
- conversión aleatoria a escala de grises, p = 0.2
- `RandomErasing` sobre regiones de plumaje
- conjunto estándar: `RandomResizedCrop`, `HorizontalFlip`, rotación moderada, `ColorJitter`, Normalize, **Mixup** α=0.2, **CutMix** α=1.0

Un **módulo de video** complementario (Sección 8) está planificado para añadir un prior bayesiano a partir de clips cortos. El código actual implementa el prior como placeholder; el V2 multimodal completo se reserva para el trabajo doctoral.

## 8. Arquitecturas comparadas

Cuatro backbones se comparan en igualdad de condiciones: misma partición, mismas augmentaciones, mismo protocolo. Los resultados comparativos se reportarán en `results/METRICS_TEMPLATE.md` tras el entrenamiento.

| Arquitectura | Parámetros | Input | ImageNet top-1 (referencia) | Rol previsto |
|---|---|---|---|---|
| MobileNetV3-Large | 5.5 M | 224×224 | 75.2 % | Edge / móvil / Raspberry Pi |
| EfficientNet-B3 | 12.2 M | 300×300 | 81.6 % | Mejor accuracy por parámetro |
| ResNet-50 | 25.6 M | 224×224 | 80.4 % | **Baseline** |
| ConvNeXt-Tiny | 28.6 M | 232×232 | 82.1 % | Challenger SOTA |

Los números de ImageNet son top-1 de referencia de los artículos originales / model zoo de torchvision; *no* son resultados de este proyecto.

## 9. Pipeline de entrenamiento

Transfer learning en dos etapas, siguiendo Howard & Ruder (2018, ULMFiT):

**Etapa 1 — feature extraction** (10 epochs)
Adam, lr = 1e-3. Backbone congelado, sólo entrena la cabeza clasificadora. Propósito: estabilizar la cabeza antes de tocar los pesos preentrenados.

**Etapa 2 — fine-tuning** (≤ 80 epochs, early-stopping patience 15)
AdamW, lr = 1e-4, weight decay = 5e-4. Cosine annealing con 3 epochs de warm-up. Label smoothing 0.1, Mixup α = 0.2, CutMix α = 1.0. Cross-entropy ponderada para mitigar desbalance de clases.

Defaults sensibles al hardware en `config.py`: `BATCH_SIZE = 16`, `GRADIENT_ACCUM_STEPS = 2`, `USE_AMP = True`. Detección multiplataforma de dispositivo (NVIDIA CUDA, Apple MPS, fallback CPU).

## 10. Métricas de evaluación

- **Accuracy** (global, sobre conjunto de prueba de 53 clases)
- **F1-macro** (promedio no ponderado entre especies — métrica primaria para clases desbalanceadas)
- **F1 por especie** (53 valores)
- **Top-3 accuracy**
- **Matriz de confusión 53 × 53** (CSV + PNG)
- **Latencia de inferencia** (ms por imagen, batch size 1)
- **Tamaño del modelo entrenado** (MB en disco)

Todos los scripts que calculan estas métricas viven en `codigo/pytorch/evaluate.py`. Las plantillas de reporte están en `results/`.

## 11. Explicabilidad con Grad-CAM

`codigo/pytorch/gradcam.py` produce mapas de activación ponderados por gradiente para cualquier imagen dado un checkpoint entrenado. El protocolo de validación se describe en `results/GRADCAM_EXAMPLES.md`:

- se revisan al menos 20 mapas por clase manualmente;
- cualquier imagen donde el pico de activación caiga sobre fondo (cielo / dosel) en lugar de sobre el ave se marca para auditoría;
- esto detecta un modo de falla conocido como **shortcut learning** (Geirhos et al., *Nature Machine Intelligence*, 2020) — ver `results/SHORTCUT_LEARNING_FINDING.md`.

## 12. Estado actual

| Componente | Estado | Notas |
|---|---|---|
| Adquisición de dataset (53 especies) | **En curso** | Scripts listos; descarga es incremental |
| Pipeline de curación (`curate.py`) | **Funcional** | Probado en el subset V1 (23 especies) |
| Entrenamiento de las 4 arquitecturas | **Pendiente run completo** | Smoke test pasa; benchmark agendado |
| Scripts de evaluación | **Funcional** | Los mismos scripts del proyecto predecesor en Australia (F1-macro 0.85 sobre 8 especies) |
| Módulo Grad-CAM | **Funcional** | Demo sobre datos sintéticos validado |
| GUI web Flask | **Funcional en modo demo** | Carga pesos entrenados cuando existen |
| Módulo de comportamiento (prior V1) | **Prototipo** | Combinación bayesiana implementada como placeholder; V2 multimodal es trabajo doctoral |
| Vocabulario International Sign | **En propuesta** | 53 señas diseñadas; validación con grupos focales agendada |
| Infraestructura de reproducibilidad | **Funcional** | Seeds, environments (CUDA / CPU / MPS), tags de Git |

## 13. Limitaciones

- **Desbalance de clases.** *Cathartes aura* tiene > 1000 imágenes; *Harpia harpyja* y *Morphnus guianensis* menos de 100. Cross-entropy ponderada, Mixup y CutMix ayudan; se requiere alianza con The Peregrine Fund y CONABIO para datos de especies raras.
- **Sesgo fotográfico de iNaturalist.** La mayoría de subidas son aves en planeo contra cielo limpio. El modelo subrendirá previsiblemente sobre fondos de dosel típicos de *Spizaetus* y *Harpagus*.
- **Resolución temporal del módulo de comportamiento.** El prior V1 actual opera a ~1 fps y no captura eventos rápidos como el stoop de *Falco peregrinus*. V2 está planificado con CNN 3D a 8-16 fps.
- **Riesgo del prior geográfico.** Los priors por coordenadas pueden introducir sesgo de confirmación. V2 ponderará el prior por la incertidumbre del clasificador visual.
- **Sin publicación arbitrada aún.** Este es un proyecto de investigación en desarrollo.

## 14. Trabajo futuro

1. Completar el benchmark de las 4 arquitecturas y publicar la curva de Pareto (accuracy vs latencia vs VRAM).
2. Reemplazar el prior placeholder V1 por un módulo de comportamiento basado en CNN 3D (SlowFast o ResNet3D-18).
3. Añadir DeepSORT para tracking por individuo y agregación temporal entre frames.
4. Validar el catálogo de International Sign con la comunidad sorda usando protocolo Likert (claridad, naturalidad, memorabilidad).
5. Fusión bayesiana multimodal: visión + comportamiento + fenología + geografía a nivel posterior.
6. Extensión a Strigiformes (búhos), lo que introduce modalidades de audio y visión nocturna.

## 15. Cómo instalar

Manual multiplataforma completo en [`MANUAL_INSTALACION.md`](MANUAL_INSTALACION.md). Inicio rápido:

```bash
git clone https://github.com/ZOMBIECRAFTIAN/raptors-cnn.git
cd raptors-cnn

# Elegir el entorno según tu hardware
conda env create -f codigo/pytorch/environment.yml          # NVIDIA CUDA
# conda env create -f codigo/pytorch/environment-cpu.yml    # Sólo CPU
# conda env create -f codigo/pytorch/environment-mps.yml    # Apple Silicon

conda activate raptors-pt
pip install -r codigo/pytorch/pip-requirements.txt
python codigo/pytorch/verify_setup.py
```

## 16. Cómo entrenar

```bash
# 1. Descargar un dataset pequeño
cd codigo/pytorch
python download_inaturalist.py --target 50 --max-pages 1

# 2. Curar y partir
python curate.py --apply
python split_dataset.py

# 3. Smoke test (1 epoch, ~5 min)
python train.py --arch resnet50 --smoke-test

# 4. Entrenamiento completo (4-8 h en RTX 3050; CPU no recomendado)
python train.py --arch resnet50

# 5. Evaluar
python evaluate.py --arch resnet50 \
                   --weights outputs/checkpoints/best_stage2.pt
```

## 17. Cómo ejecutar inferencia

```bash
# GUI web Flask
cd codigo/pytorch/app_flask
python app.py
# abrir http://localhost:5000

# Grad-CAM sobre una imagen
cd codigo/pytorch
python gradcam.py --image ruta/a/imagen.jpg \
                  --arch resnet50 \
                  --weights outputs/checkpoints/best_stage2.pt
```

## 18. Cómo citar

Si referencias este trabajo en escritura académica, por favor cita el archivo CITATION:

```bibtex
@misc{fernandezbaez_raptors_cnn_2026,
  author = {Brian Fernandez Baez},
  title  = {raptors-cnn: a reproducible AI pipeline for raptor identification using silhouette and flight behaviour},
  year   = {2026},
  url    = {https://github.com/ZOMBIECRAFTIAN/raptors-cnn},
  note   = {Master's research proposal, work in progress}
}
```

Metadata completa legible por máquina en [`CITATION.cff`](CITATION.cff).

---

## 19. Extensión en International Sign (entregable secundario)

Entregable complementario de inclusión: un **vocabulario propuesto de 53 señas en International Sign**, co-diseñado con la comunidad sorda. Vive en `lengua_de_senas/` y sigue el manifiesto de la [World Federation of the Deaf](https://wfdeaf.org) y el marco CAST de Diseño Universal para el Aprendizaje. **Se reporta como contribución separada y no forma parte de la evaluación de IA.**

---

## Contacto

Brian Fernandez Baez · brianferbaez@gmail.com · [GitHub](https://github.com/ZOMBIECRAFTIAN)

**Licencias:** código MIT · datos y señas CC-BY 4.0
