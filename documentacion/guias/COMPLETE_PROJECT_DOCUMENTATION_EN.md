# Complete documentation for the raptors-cnn project

**Project:** raptors-cnn  
**Author:** Brian Fernandez Baez  
**Type:** master's-level research proposal/prototype  
**Documented version:** current repository structure after reorganization  

---

## 1. What this document is

`README.md` is the public landing page for GitHub. It explains the goal, scientific problem, general methodology, installation and basic usage.

This file is the detailed technical map. It explains where everything lives, what each major folder does, what each important source file does, how models are trained, how they are evaluated, where the Flask interface is generated and which parts are still future work.

---

## 2. Project objective

`raptors-cnn` aims to build a computer-vision tool for identifying diurnal raptors in Mexico from images and, later, video.

The academic objective is to design, build and evaluate a reproducible AI pipeline that:

- identifies 53 diurnal raptor species in Mexico;
- uses deep learning with CNNs and transfer learning;
- emphasizes silhouette and shape instead of relying only on plumage colour;
- compares several architectures under the same protocol;
- evaluates the model with quantitative metrics and interpretability;
- provides a usable web interface for demonstration and observation capture.

---

## 3. Problem addressed

Raptor identification in the field is difficult because the bird is often:

- far away;
- backlit against the sky;
- visible mostly as a silhouette;
- missing clear plumage colour;
- changing shape depending on posture, flight mode and angle.

A bird counter, naturalist or hobbyist cannot always stop and inspect a full field guide. This project tries to support that decision by proposing likely candidates and showing biological information.

---

## 4. Intended users

The project can be understood as a tool for:

- migration bird counters;
- field naturalists;
- biology, ecology or conservation students;
- citizen-science users;
- people learning raptor identification;
- researchers who need a reproducible visual-classification pipeline.

It should not be presented as a replacement for an expert ornithologist. It is an identification assistant and a research base.

---

## 5. Difference from Merlin Bird ID

Merlin Bird ID is a strong, broad and closed general-purpose tool. This project differs as follows:

| Aspect | Merlin Bird ID | raptors-cnn |
|---|---|---|
| Scope | Many birds and regions | Focused on 53 Mexican diurnal raptors |
| Code | Closed | Open and reviewable |
| Focus | General photo/audio identification | Silhouette, shape and flight behaviour |
| Reproducibility | Full training pipeline is not exposed | Scripts, expected data layout, training and evaluation are documented |
| Research status | Finished product | Academic prototype in progress |
| Video/behaviour | Not the visible user-facing focus | Future module planned with YOLO/behaviour |
| Interpretability | Not exposed to users | Grad-CAM checks where the model looks |

The point is not to beat Merlin at scale, but to demonstrate a specialized, open and academic approach for raptors in flight.

---

## 6. Repository overview

```text
raptors-cnn/
├── README.md / README_ES.md        Public project overview
├── codigo/                         Model and interface source code
├── datos/                          Local dataset, annotations and future videos
├── documentacion/                  Academic docs, guides and result templates
├── lengua_de_senas/                Secondary accessibility deliverable
├── referencias/                    Bibliography and templates
├── scripts/                        Windows and dataset utilities
├── .gitignore                      Rules for excluding secrets and heavy files
├── .env.example                    Safe environment-variable template
├── CITATION.cff                    Citation metadata
├── CONTRIBUTING.md                 Contribution guide
└── LICENSE                         Code license
```

---

## 7. Root files

| File | Purpose |
|---|---|
| `README.md` | Main GitHub overview in English. |
| `README_ES.md` | Main overview in Spanish. Best entry point for explaining the project. |
| `.gitignore` | Prevents datasets, heavy videos, trained weights, caches, `.env` and uploads from being committed. |
| `.gitattributes` | Git configuration for file handling and formats. |
| `.env` | Local variables. Must not be uploaded to GitHub. |
| `.env.example` | Safe template for creating a local `.env`. |
| `CITATION.cff` | Academic citation metadata. |
| `CONTRIBUTING.md` | Rules for contributing code, data, docs and sign-language material. |
| `LICENSE` | Code license. |

---

## 8. `codigo/`

This folder contains the source code.

| Folder | Purpose |
|---|---|
| `codigo/pytorch/` | Main implementation. Training and evaluation happen here. |
| `codigo/tensorflow/` | Secondary TensorFlow mirror/alternative. |
| `codigo/comparacion/` | Architecture comparison scripts and figures. |

---

## 9. `codigo/pytorch/`

This is the core of the project.

| File/folder | Purpose |
|---|---|
| `config.py` | Defines paths, species, codes, common names, classes, batch size, epochs and training stages. |
| `data_loader.py` | Loads `datos/processed/train`, `val` and `test` using `ImageFolder`; applies augmentations and normalization. |
| `model.py` | Builds CNN architectures: ResNet-50, EfficientNet-B3, MobileNetV3-Large and ConvNeXt-Tiny. |
| `train.py` | Trains the model in two stages: feature extraction and fine-tuning. |
| `evaluate.py` | Evaluates a checkpoint on the test set; generates report, confusion matrix and ROC curves. |
| `gradcam.py` | Generates Grad-CAM maps to check whether the model attends to the bird rather than the background. |
| `curate.py` | Scores/filters images by resolution, sharpness, brightness and duplicates. |
| `split_dataset.py` | Splits data into train/val/test using a 70/15/15 ratio. |
| `download_inaturalist.py` | Downloads images from iNaturalist. |
| `download_ebird.py` | Downloads or prepares eBird-related metadata. |
| `annotate.py` | Supports annotation/review and annotator-agreement checks. |
| `exclude_empty_species.py` | Handles species with little data or empty folders. |
| `make_synthetic_dataset.py` | Creates a synthetic dataset for quick tests. |
| `retrain_with_feedback.py` | Fine-tunes the model using accumulated user corrections. |
| `verify_setup.py` | Verifies Python, PyTorch and dependency setup. |
| `train_colab.ipynb` | Notebook for Google Colab training. |
| `environment.yml` | Conda environment for NVIDIA/CUDA. |
| `environment-cpu.yml` | Conda environment for CPU. |
| `environment-mps.yml` | Conda environment for Apple Silicon/MPS. |
| `pip-requirements.txt` / `requirements.txt` | pip-installable dependencies. |
| `outputs/` | Generated outputs: checkpoints, matrices, curves and Grad-CAM images. Not source code. |
| `app/` | Older/alternative app prototype. |
| `app_flask/` | Main Flask web interface. |

---

## 10. Where models are trained

Main training happens in:

```text
codigo/pytorch/train.py
```

Typical command:

```bash
cd codigo/pytorch
python train.py --arch resnet50
```

Quick smoke test:

```bash
cd codigo/pytorch
python train.py --arch resnet50 --smoke-test
```

Supported architectures:

- `resnet50`
- `efficientnet_b3`
- `mobilenet_v3_large`
- `convnext_tiny`

Trained weights are saved in:

```text
codigo/pytorch/outputs/checkpoints/
```

Expected checkpoint files:

```text
best_stage1.pt
best_stage2.pt
```

The Flask interface tries to load:

```text
codigo/pytorch/outputs/checkpoints/best_stage2.pt
```

---

## 11. How training works

Training uses two-stage transfer learning:

1. **Stage 1 / feature extraction**  
   The pretrained backbone is frozen and the classifier head is trained.

2. **Stage 2 / fine-tuning**  
   The full model is unfrozen and trained with a smaller learning rate.

Important parameters:

| Parameter | Location | Purpose |
|---|---|---|
| `SPECIES` | `config.py` | Official list of 53 species. |
| `NUM_CLASSES` | `config.py` | Number of classes. |
| `BATCH_SIZE` | `config.py` | Batch size. |
| `USE_AMP` | `config.py` | Uses mixed precision when compatible GPU is available. |
| `GRADIENT_ACCUM_STEPS` | `config.py` | Simulates a larger effective batch size. |
| `STAGE1` | `config.py` | First-stage configuration. |
| `STAGE2` | `config.py` | Fine-tuning configuration. |

---

## 12. Dataset location

Expected data layout:

```text
datos/
├── raw/                         original downloaded images
├── processed/
│   ├── train/                   training split
│   ├── val/                     validation split
│   └── test/                    final test split
├── annotations/                 CSV metadata and curation reports
├── feedback/                    user corrections and feedback
└── videos/                      future behaviour/video module
```

Heavy data should not be uploaded to GitHub. That is why `datos/raw/`, `datos/processed/` and real video folders are ignored.

---

## 13. How model efficiency is evaluated

Main evaluation script:

```text
codigo/pytorch/evaluate.py
```

Command:

```bash
cd codigo/pytorch
python evaluate.py --arch resnet50 --weights outputs/checkpoints/best_stage2.pt
```

It evaluates:

- accuracy;
- per-class report;
- precision, recall and F1;
- confusion matrix;
- ROC curves;
- behaviour on the held-out `test` split.

Expected outputs:

```text
codigo/pytorch/outputs/confusion_matrix.png
codigo/pytorch/outputs/roc_curves.png
```

Architecture comparison lives in:

```text
codigo/comparacion/comparar_arquitecturas.py
codigo/comparacion/README.md
```

The comparison considers:

- accuracy;
- macro-F1;
- top-3 accuracy;
- total training time;
- inference latency;
- model size;
- trade-off figures.

---

## 14. Where the Flask interface is generated

The main interface lives in:

```text
codigo/pytorch/app_flask/
```

Main files:

| File/folder | Purpose |
|---|---|
| `app.py` | Flask backend: loads model, defines routes, inference, feedback and exports. |
| `templates/base.html` | Shared base template. |
| `templates/index.html` | Main upload/result page. |
| `templates/species.html` | Species guide. |
| `templates/data.html` | Data/export panel. |
| `static/css/style.css` | Visual styles. |
| `static/js/main.js` | Frontend JavaScript: uploads image, calls `/identify`, renders results. |
| `translations/es.json` | Spanish interface strings. |
| `translations/en.json` | English interface strings. |
| `species_info.py` | Short species information. |
| `species_data.py` | Extended biological species profiles in Spanish/base language. |
| `species_data_en.py` | Extended biological species profiles in English. |
| `uploads/` | Temporary user uploads. Must not be committed. |

Run command:

```bash
cd C:\Users\hogwa\raptors-cnn
conda activate raptors-pt
cd codigo\pytorch\app_flask
python app.py
```

URL:

```text
http://localhost:5000
```

---

## 15. Main Flask routes

| Route | Purpose |
|---|---|
| `/` | Main page. |
| `/identify` | Receives an image and returns top-3 prediction. |
| `/identify_video` | Video-analysis prototype. Should be replaced/strengthened with YOLO. |
| `/species` | Species guide. |
| `/data` | Data and observations panel. |
| `/feedback` | Stores user corrections. |
| `/feedback_stats` | Shows accumulated feedback count. |
| `/save_observation` | Stores observations with metadata. |
| `/export/observations.csv` | Exports observations. |
| `/export/feedback.csv` | Exports feedback. |
| `/is_videos/<filename>` | Serves sign-language videos. |
| `/behavior_videos/<filename>` | Serves behaviour videos if available. |

---

## 16. Video and YOLO section

There are currently two video-related areas:

```text
datos/videos/
codigo/pytorch/app_flask/static/behavior_videos/
```

`datos/videos/` is intended for field clips used by the future behaviour module. The correct next step is to implement YOLO-based detection/tracking to locate birds in video, then analyse flight behaviour.

Recommended status wording:

- **current:** folder and prototype are prepared;
- **pending:** real YOLO pipeline for detection/tracking;
- **do not claim:** that the video module is already a final validated classifier.

---

## 17. `codigo/comparacion/`

Used to compare architectures and generate figures.

| File/folder | Purpose |
|---|---|
| `comparar_arquitecturas.py` | Runs training/evaluation per architecture and generates reports. |
| `README.md` | Explains the comparison protocol. |
| `metricas_arquitecturas.csv` | Comparative metrics table. |
| `figures/` | Plots: accuracy, macro-F1 and latency vs accuracy. |

---

## 18. `codigo/tensorflow/`

Secondary TensorFlow/Keras implementation.

| File | Purpose |
|---|---|
| `config.py` | Equivalent TensorFlow configuration. |
| `data_loader.py` | TensorFlow data loading. |
| `model.py` | TensorFlow model architecture. |
| `train.py` | TensorFlow training. |
| `evaluate.py` | TensorFlow evaluation. |
| `make_synthetic_dataset.py` | Synthetic dataset for tests. |
| `verify_setup.py` | Dependency verification. |
| `environment.yml` | Conda environment. |
| `requirements.txt` / `pip-requirements.txt` | pip dependencies. |
| `outputs/` | Generated outputs. |

This is not the main implementation. PyTorch should be presented as the authoritative implementation.

---

## 19. `documentacion/`

Contains the academic and project-management material.

| File/folder | Purpose |
|---|---|
| `guias/` | Installation manuals, command guides and complete documentation. |
| `resultados/` | Templates for metrics, curves, confusion matrix and Grad-CAM. |
| `diagramas/` | Architecture diagrams. |
| `LISTA_OFICIAL_RAPACES_MEXICO.md` | Official taxonomic list of target species. |
| `WORKFLOW_DATASET_REAL.md` | Workflow for building the real dataset. |
| `data_management_plan.md` | Data management plan. |
| `preregistration.md` | Hypothesis/methodology preregistration. |
| `contribucion_novedosa.md` | Academic contribution statement. |
| `glosario.md` | Glossary. |
| `RESUMEN_EJECUTIVO.md` | Executive summary. |

Internal drafts, audits, interview notes, binary presentations and Word thesis chapters are kept locally, but excluded from GitHub through `.gitignore`.

---

## 20. `documentacion/resultados/`

This folder does not necessarily contain final results. It contains templates and protocols.

| File | Purpose |
|---|---|
| `README.md` | Explains what belongs in the results folder. |
| `METRICS_TEMPLATE.md` | Metrics template by architecture/species. |
| `CONFUSION_MATRIX_TEMPLATE.md` | Confusion-matrix template. |
| `GRADCAM_EXAMPLES.md` | Grad-CAM review protocol. |
| `TRAINING_CURVES.md` | Guide for interpreting training curves. |
| `SHORTCUT_LEARNING_FINDING.md` | Notes on shortcut learning. |

---

## 21. `scripts/`

Utilities outside the main source code.

### `scripts/windows/`

| File | Purpose |
|---|---|
| `descargar_v1_1.bat` | Windows dataset download shortcut. |
| `entrenar_v1_1.bat` | Windows smoke-test/training shortcut. |
| `pipeline_completo_v1_1.bat` | Runs curation, split, training and evaluation. |
| `limpiar_v1_1.bat` | Cleans generated/obsolete files. |
| `commit_v1_1.bat` | Local commit/push helper. Use with care. |

### `scripts/dataset/`

| File | Purpose |
|---|---|
| `contar_dataset.py` | Counts images per split and species. |
| `seleccionar_imagenes_galeria.py` | Automatically selects species-guide images. |
| `selector_galeria_gui.py` | Tkinter UI for manually selecting species-guide images. |

---

## 22. `datos/`

| Folder/file | Purpose |
|---|---|
| `README.md` | Explains data organization. |
| `FUENTES_DE_IMAGENES.md` | Image sources and criteria. |
| `annotations/` | CSV metadata, curation reports and `.gitkeep`. |
| `feedback/` | User feedback and out-of-domain cases. |
| `videos/README.md` | Video organization plan for behaviour/YOLO. |
| `raw/` | Original downloaded images. Ignored by Git. |
| `processed/` | Dataset split into train/val/test. Ignored by Git. |

---

## 23. `lengua_de_senas/`

Secondary accessibility deliverable.

| File/folder | Purpose |
|---|---|
| `README.md` | Explains the sign-language module. |
| `glosario_IS_LSM.md` | Glossary between International Sign, LSM and related terms. |
| `catalogo_senas/` | Proposed sign catalogue by species. |
| `instrumentos_validacion/` | Questionnaires and validation material. |
| `videos/` | Sign videos. Heavy or future media, not central to AI. |

This should not be sold as the central AI contribution; it is an inclusion component.

---

## 24. `referencias/`

| File | Purpose |
|---|---|
| `bibliografia.md` | Project bibliography. |
| `plantilla_ficha.md` | Template for species/reference sheets. |

---

## 25. `.vscode/`

Visual Studio Code configuration.

| File | Purpose |
|---|---|
| `settings.json` | Editor/lint/format preferences. |
| `extensions.json` | Recommended extensions. |
| `launch.json` | Run/debug configurations. |

This is not part of the model, but it helps keep development consistent.

---

## 26. Complete project flow

```text
1. Define target species
   documentacion/LISTA_OFICIAL_RAPACES_MEXICO.md
   codigo/pytorch/config.py

2. Download images
   codigo/pytorch/download_inaturalist.py
   codigo/pytorch/download_ebird.py

3. Curate images
   codigo/pytorch/curate.py

4. Split dataset
   codigo/pytorch/split_dataset.py

5. Load data and augmentations
   codigo/pytorch/data_loader.py

6. Build model
   codigo/pytorch/model.py

7. Train
   codigo/pytorch/train.py

8. Evaluate
   codigo/pytorch/evaluate.py

9. Interpret with Grad-CAM
   codigo/pytorch/gradcam.py

10. Show in interface
    codigo/pytorch/app_flask/app.py
    codigo/pytorch/app_flask/templates/
    codigo/pytorch/app_flask/static/
```

---

## 27. Main commands

### Verify environment

```bash
cd codigo/pytorch
python verify_setup.py
```

### Count dataset

```bash
python scripts/dataset/contar_dataset.py --por-especie
```

### Quick training

```bash
cd codigo/pytorch
python train.py --arch resnet50 --smoke-test
```

### Full training

```bash
cd codigo/pytorch
python train.py --arch resnet50
```

### Evaluate

```bash
cd codigo/pytorch
python evaluate.py --arch resnet50 --weights outputs/checkpoints/best_stage2.pt
```

### Run Flask

```bash
cd C:\Users\hogwa\raptors-cnn
conda activate raptors-pt
cd codigo\pytorch\app_flask
python app.py
```

---

## 28. What to say in a presentation

Short version:

> This project develops a reproducible AI pipeline for identifying the 53 diurnal raptors of Mexico. Unlike generalist tools such as Merlin, it focuses on raptors in flight, where silhouette, shape and behaviour are more informative than colour. The system includes CNN training, quantitative evaluation, Grad-CAM and a Flask interface for demonstration.

Honest status version:

> Image classification and the Flask interface are implemented as a prototype. The video/behaviour section is prepared as future work and will be strengthened with YOLO for detection and tracking.

---

## 29. What not to claim yet

Do not claim:

- that the system already outperforms Merlin;
- that the YOLO video module is finished;
- that final 53-species benchmark results are validated if the full benchmark has not been run;
- that it replaces human experts;
- that sign language is the central AI contribution.

You can claim:

- the project is open and reproducible;
- it is focused on Mexican raptors;
- it uses transfer learning;
- it has a training/evaluation pipeline;
- the Flask interface provides a clear demonstration;
- video/YOLO is the next module.
