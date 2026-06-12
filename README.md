<div align="center">

# raptors-cnn

### A reproducible AI pipeline for raptor identification using silhouette, flight behaviour and deep learning

**Master's research proposal — work in progress — Brian Fernandez Baez — 2026**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![PyTorch 2.3](https://img.shields.io/badge/PyTorch-2.3-EE4C2C.svg?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![CUDA 12.1](https://img.shields.io/badge/CUDA-12.1-76B900.svg?logo=nvidia&logoColor=white)](https://developer.nvidia.com/cuda-toolkit)
[![Status: research preview](https://img.shields.io/badge/status-research%20preview-orange.svg)]()
[![Cite this](https://img.shields.io/badge/cite-CITATION.cff-informational.svg)](CITATION.cff)

[Español](README_ES.md) · [Installation manual](documentacion/guias/MANUAL_INSTALACION.md) · [Complete documentation](documentacion/guias/COMPLETE_PROJECT_DOCUMENTATION_EN.md) · [Scientific validation](documentacion/SCIENTIFIC_VALIDATION.md) · [YOLO video module](documentacion/YOLO_VIDEO_MODULE.md)

</div>

> **About this repository.** This is an **ongoing research project**, not a finished thesis. The code, the dataset specification, the model architectures, the evaluation protocol and the planned experiments are public so the work can be reviewed and reproduced from scratch. Results sections marked *"to be filled after training"* are placeholders that will be replaced as experiments complete. Where numbers do appear, they are explicitly labelled with their source and date.

---

## 1. Project summary

`raptors-cnn` is a research-grade computer-vision prototype for identifying the **53 diurnal raptor species of Mexico** (American Ornithological Society 2024 check-list) from photographs and short videos. The system is designed as a **reproducible AI pipeline**: a curated dataset, four CNN architectures benchmarked head-to-head, two-stage transfer learning, Grad-CAM interpretability validation, a Flask web GUI, and an open International Sign vocabulary that makes the tool accessible to Deaf naturalists.

The project is being developed as the basis of a master's research proposal in artificial intelligence applied to wildlife conservation. It is intentionally **open from day one**: code is MIT-licensed, data and signs are CC-BY, and the development log is public.

## 2. Scientific problem

Raptor identification in the field is dominated by **flight observations**: the bird is far, often backlit, and plumage colour is not visible. Existing AI tools such as **Merlin Bird ID** and **iNaturalist Computer Vision** train predominantly on **perched birds with rich colour photographs**, and their predictions rely heavily on plumage features that are unavailable in typical raptor sightings.

A trained ornithologist relies instead on **silhouette** (wing chord ratio, wingtip shape, tail outline, head proportion) and on **flight behaviour** (soaring, flap-glide, hovering, kettle formation, stoop). No published open-source identifier explicitly targets these cues.

## 3. Research objective

To design, build and evaluate a reproducible computer-vision pipeline that:

- identifies the 53 diurnal raptor species of Mexico from flight-silhouette photographs;
- complements the visual classifier with a temporal flight-behaviour module integrated as a Bayesian prior;
- validates interpretability through Grad-CAM analysis on a held-out test set;
- ships as an installable, multi-platform (CUDA / CPU / Apple Silicon MPS) software package.

**Secondary objective (Section 9 — separated on purpose):** co-design with the Deaf community a 53-sign vocabulary in International Sign that mirrors the species catalogue, so that the same scientific knowledge is accessible without an audio channel. This is an inclusion deliverable; it is *not* a core AI contribution.

## 4. Why raptor identification matters

Raptors are **apex predators** and recognised **bioindicators** of ecosystem health (Sergio et al., *Ecological Letters*, 2008). Their populations are sensitive to habitat loss, pesticide accumulation and climate change. Mexico hosts the largest raptor migration corridor in the Americas — over **five million birds** transit the Veracruz River of Raptors corridor each autumn (Pronatura Veracruz, 2020). Scaling field monitoring beyond what trained ornithologists can do manually requires automated identification tools that work under realistic field conditions, including high-altitude flight against bright sky.

Accurate, scalable raptor ID directly supports:

- post-disturbance monitoring (fire, drought, deforestation);
- citizen-science contributions to **iNaturalist**, **eBird**, **CONABIO**, **GBIF**;
- conservation status assessment for IUCN and NOM-059-SEMARNAT-2010 listings.

## 5. Dataset

| Property | Specification |
|---|---|
| Source platforms | iNaturalist (research-grade), Macaulay Library, eBird, CONABIO |
| Licence filter | CC0 / CC-BY / CC-BY-SA only |
| Target images per species | 200 (rare species: best-effort) |
| Resolution floor | long side ≥ 800 px (post-curation) |
| Curation script | `codigo/pytorch/curate.py` — 0-100 score (resolution + Laplacian sharpness + brightness + perceptual hash) |
| Annotation quality | Double annotation on borderline images; Cohen's κ ≥ 0.85 required |
| Split | 70 / 15 / 15 train / val / test, stratified by species and grouped by `observationID`, seed = 42 |
| Provenance | SHA-256 of every image logged in `datos/annotations/` |

Dataset construction is described in detail in `documentacion/WORKFLOW_DATASET_REAL.md`.

## 6. Target species

**53 diurnal raptors of Mexico** following AOS 2024 (Cathartidae × 4 · Pandionidae × 1 · Accipitridae × 38 · Falconidae × 10). The full list with scientific names, 4-letter codes, IUCN status and NOM-059 status is in `documentacion/LISTA_OFICIAL_RAPACES_MEXICO.md`. Three AOS 2023 reclassifications are applied: *Accipiter cooperii* → *Astur cooperii*, *Accipiter gentilis* → *Astur atricapillus*, *Buteo nitidus* → *Buteo plagiatus*.

## 7. AI methodology

The pipeline applies standard **transfer-learning** on backbones pre-trained on ImageNet, with augmentations specifically tuned to force the model to learn **silhouette and shape** rather than plumage colour:

- colour jitter for brightness, contrast and saturation
- `RandomErasing` on plumage regions
- standard set: `RandomResizedCrop`, `HorizontalFlip`, mild rotation, `ColorJitter`, Normalize, **Mixup** α=0.2, **CutMix** α=1.0

A complementary **video module** (Section 8) adds YOLO-based detection/tracking over short clips. YOLO localises birds per sampled frame, a lightweight IoU tracker keeps individual IDs across frames, and the 53-class CNN classifies each crop. Flight behaviour is reported with conservative interpretable heuristics (`soaring_or_gliding`, `active_flapping_or_maneuvering`, `hovering_or_wind_hold`, `stoop_or_descent`) before a supervised temporal classifier is trained.

## 8. Model architectures

Four backbones are benchmarked head-to-head under the same split, the same augmentations and the same training protocol. Comparative results will be reported in `documentacion/resultados/METRICS_TEMPLATE.md` after training.

| Architecture | Parameters | Input | ImageNet top-1 (ref.) | Intended role |
|---|---|---|---|---|
| MobileNetV3-Large | 5.5 M | 224×224 | 75.2 % | Edge / mobile / Raspberry Pi |
| EfficientNet-B3 | 12.2 M | 300×300 | 81.6 % | Accuracy-per-parameter |
| ResNet-50 | 25.6 M | 224×224 | 80.4 % | **Baseline** |
| ConvNeXt-Tiny | 28.6 M | 232×232 | 82.1 % | SOTA challenger |

ImageNet numbers are reference top-1 accuracy from the corresponding original papers / torchvision model zoo; they are *not* this project's results.

## 9. Training pipeline

Two-stage transfer learning, following Howard & Ruder (2018, ULMFiT):

**Stage 1 — feature extraction** (10 epochs)
Adam, lr = 1e-3. Backbone frozen, only the classifier head trains. Purpose: stabilise the head before risking the pre-trained weights.

**Stage 2 — fine-tuning** (≤ 80 epochs, early-stopping patience 15)
AdamW, lr = 1e-4, weight decay = 5e-4. Cosine annealing with 3 warm-up epochs. Label smoothing 0.1, Mixup α = 0.2, CutMix α = 1.0. Weighted cross-entropy mitigates class imbalance. Training history is exported as CSV plus learning-curve figures.

Hardware-aware defaults in `config.py`: `BATCH_SIZE = 16`, `GRADIENT_ACCUM_STEPS = 2`, `USE_AMP = True`. Multi-platform device detection (NVIDIA CUDA, Apple MPS, CPU fallback).

## 10. Evaluation metrics

- **Accuracy** (global, on 53-class test set)
- **F1-macro** (unweighted average across species — primary metric for imbalanced classes)
- **F1 per species** (53 values)
- **Top-3 accuracy**
- **53 × 53 confusion matrix** (CSV + PNG)
- **Inference latency** (ms per image, batch size 1)
- **Trained-model size** (MB on disk)

All scripts that compute these live in `codigo/pytorch/evaluate.py`. Evaluation exports `outputs/metrics_<arch>.json`, a text classification report, a confusion matrix and ROC curves. Reporting templates are in `documentacion/resultados/`.

## 11. Explainability with Grad-CAM

`codigo/pytorch/gradcam.py` produces gradient-weighted class activation maps for any image given a trained checkpoint. The validation protocol is described in `documentacion/resultados/GRADCAM_EXAMPLES.md`:

- at least 20 maps per class are reviewed by the author;
- any image where the activation peak falls on background (sky / canopy) instead of on the bird is flagged for audit;
- this catches a well-known failure mode called **shortcut learning** (Geirhos et al., *Nature Machine Intelligence*, 2020) — see `documentacion/resultados/SHORTCUT_LEARNING_FINDING.md`.

## 12. Current status

| Component | Status | Notes |
|---|---|---|
| Dataset acquisition (53 species) | **In progress** | Local processed split contains 53 class folders; public media is gitignored |
| Curation pipeline (`curate.py`) | **Working** | Designed for the 53-species dataset and writes curation metadata |
| Four-architecture training | **Partially run locally** | ResNet/EfficientNet/MobileNet checkpoints can be trained; full benchmark still pending |
| Evaluation scripts | **Working** | Export JSON metrics, classification report, confusion matrix and ROC curves |
| ResNet-50 evaluation | **Observation-level local result** | `observationID` split; test n=2,653; accuracy=0.6072; balanced accuracy=0.5808; F1-macro=0.5837; top-3=0.6958; macro-AUC=0.9226 |
| Grad-CAM module | **Working** | Demo on synthetic data validated |
| Flask web GUI | **Working in demo mode** | Loads trained weights when present |
| Behaviour/video module | **YOLO prototype implemented** | `/identify_video` uses YOLO + IoU tracking + CNN crop classification; custom YOLO training is ready for annotated boxes |
| International Sign vocabulary | **Proposal stage** | 53 signs drafted; focus-group validation scheduled |
| Reproducibility infrastructure | **Working** | Seeds, environment files (CUDA / CPU / MPS), Git tags |

## 13. Limitations

- **Class imbalance.** *Cathartes aura* has > 1000 images available, while *Harpia harpyja* and *Morphnus guianensis* have fewer than 100. Weighted cross-entropy, Mixup, CutMix help; partnership with The Peregrine Fund and CONABIO is required for rare-species data.
- **iNaturalist photographic bias.** Most uploads are clear-sky soaring birds. The model is expected to under-perform on canopy backgrounds typical of *Spizaetus* and *Harpagus*.
- **Temporal resolution of the behaviour module.** The current YOLO video path is a prototype: it detects and tracks birds, but behaviour labels are heuristic. Final results require annotated boxes and temporal behaviour labels per clip.
- **Geographic prior risk.** Range-by-coordinates priors can introduce confirmation bias. V2 will weight the prior by visual-classifier uncertainty.
- **Rare-species uncertainty.** The current ResNet-50 numbers are based on the defensible `observationID` split, but rare species with very low test support still have unstable per-species estimates. *Buteogallus solitarius* and *Morphnus guianensis* require targeted data collection before their species-level F1 can be treated as conclusive.
- **No peer-reviewed publication yet.** This is a research project under development.

## 14. Future work

1. Complete the four-architecture benchmark and publish the Pareto curve (accuracy vs latency vs VRAM).
2. Train a custom YOLO detector with Mexican raptor boxes and compare it against the COCO `bird` detector.
3. Replace behaviour heuristics with a supervised temporal classifier for soaring, flap-glide, hovering, kettle formation and stoop.
4. Validate the International Sign catalogue with the Deaf community using a Likert protocol (clarity, naturalness, memorability).
5. Multi-modal Bayesian fusion: vision + behaviour + phenology + geography at the posterior level.
6. Extension to Strigiformes (owls), which introduces audio and night-vision modalities.

## 15. How to install

A complete multi-platform manual is in [`documentacion/guias/MANUAL_INSTALACION.md`](documentacion/guias/MANUAL_INSTALACION.md). Quick start:

```bash
git clone https://github.com/ZOMBIECRAFTIAN/raptors-cnn.git
cd raptors-cnn

# Pick the environment that matches your hardware
conda env create -f codigo/pytorch/environment.yml          # NVIDIA CUDA
# conda env create -f codigo/pytorch/environment-cpu.yml    # CPU only
# conda env create -f codigo/pytorch/environment-mps.yml    # Apple Silicon

conda activate raptors-pt
pip install -r codigo/pytorch/pip-requirements.txt
# Optional: YOLO video module
pip install -r codigo/pytorch/requirements-yolo.txt
python codigo/pytorch/verify_setup.py
```

## 16. How to train

```bash
# 1. Download a small dataset
cd codigo/pytorch
python download_inaturalist.py --target 50 --max-pages 1

# 2. Curate and split
python curate.py --apply
python split_dataset.py --group-by-observation --clean --link
python audit_dataset.py --fail-on-leak

# 3. Smoke test (1 epoch, ~5 min)
python train.py --arch resnet50 --smoke-test

# 4. Full training (4-8 h on RTX 3050; CPU not recommended)
python train.py --arch resnet50 --split-protocol observation

# 5. Evaluate
python evaluate.py --arch resnet50 \
                   --weights outputs/checkpoints/best_stage2_resnet50.pt \
                   --split-protocol observation
```

## 17. How to run inference

```bash
# Flask web GUI
cd codigo/pytorch/app_flask
python app.py
# open http://localhost:5000

# Grad-CAM on a single image
cd codigo/pytorch
python gradcam.py --image path/to/image.jpg \
                  --arch resnet50 \
                  --weights outputs/checkpoints/best_stage2.pt

# YOLO video analysis
python yolo_predict_video.py --video ../../datos/videos/raw/Buteo_jamaicensis/clip_001.mp4

# Train/evaluate a custom YOLO detector once boxes are annotated
python yolo_train.py --data yolo/dataset_template.yaml --model yolov8n.pt --epochs 80
python yolo_evaluate.py --data yolo/dataset_template.yaml \
                        --weights outputs/yolo/checkpoints/best.pt
```

## 18. How to cite

If you reference this work in academic writing, please cite the CITATION file:

```bibtex
@misc{fernandezbaez_raptors_cnn_2026,
  author = {Brian Fernandez Baez},
  title  = {raptors-cnn: a reproducible AI pipeline for raptor identification using silhouette and flight behaviour},
  year   = {2026},
  url    = {https://github.com/ZOMBIECRAFTIAN/raptors-cnn},
  note   = {Master's research proposal, work in progress}
}
```

Full machine-readable metadata is in [`CITATION.cff`](CITATION.cff).

---

## Repository layout

```
raptors-cnn/
├── README.md                       This file
├── README_ES.md                    Spanish version
├── LICENSE  ·  CITATION.cff
│
├── codigo/pytorch/                 Main implementation
│   ├── config.py                   Single source of truth for hyperparameters + device
│   ├── train.py · evaluate.py · gradcam.py
│   ├── curate.py · split_dataset.py · download_inaturalist.py
│   ├── environment.yml · environment-cpu.yml · environment-mps.yml
│   ├── pip-requirements.txt
│   └── app_flask/                  Flask GUI (separate module)
│
├── codigo/comparacion/             Four-architecture benchmark scripts
├── datos/                          Dataset folders; heavy media is gitignored
│
├── documentacion/                  Public methodology docs, guides and results templates
│   ├── guias/                      Installation, setup and command guides
│   ├── diagramas/                  Architecture diagrams
│   └── resultados/                 Result templates — see Section 10
│       ├── METRICS_TEMPLATE.md
│       ├── CONFUSION_MATRIX_TEMPLATE.md
│       ├── GRADCAM_EXAMPLES.md
│       ├── TRAINING_CURVES.md
│       └── SHORTCUT_LEARNING_FINDING.md
│
├── scripts/                        Windows shortcuts and dataset utilities
├── lengua_de_senas/                International Sign extension (Section 9)
└── referencias/                    Bibliography
```

---

## 19. International Sign extension (secondary deliverable)

A complementary inclusion deliverable: a proposed **53-sign vocabulary in International Sign**, co-designed with the Deaf community. This sits in `lengua_de_senas/` and follows the [World Federation of the Deaf](https://wfdeaf.org) manifesto and the CAST framework for Universal Design for Learning. **It is reported as a separate contribution and is not part of the AI evaluation.**

---

## Contact

Brian Fernandez Baez · brianferbaez@gmail.com · [GitHub](https://github.com/ZOMBIECRAFTIAN)

**Licences:** code MIT · data and signs CC-BY 4.0
