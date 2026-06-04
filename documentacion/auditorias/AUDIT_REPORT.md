# Repository audit and improvement report

**Date:** June 2026
**Author:** internal review for graduate-admissions readiness
**Repository:** [github.com/ZOMBIECRAFTIAN/raptors-cnn](https://github.com/ZOMBIECRAFTIAN/raptors-cnn)

This document summarises the audit performed on the repository for use as evidence in master's-program applications.

---

## 1. Files added or rewritten

| File | What changed | Why |
|---|---|---|
| `README.md` | Full rewrite. 19 sections, academic tone, *"research project / proposal / work in progress"* framing throughout. Removed "Tesis de Maestría" language and the TensorFlow badge from the headline. Sign-language extension is now Section 19, clearly separated as **secondary deliverable**. | Avoid overstating finished work to admissions committees. |
| `README_ES.md` | New. Mirror of the English README in academic Spanish. | Bilingual reach for Mexican advisors and committees. |
| `documentacion/presentacion_en/INTERVIEW_NOTES.md` | New. 1-minute, 3-minute and 30-second pitches in EN + ES. 10 hard questions with recommended answers. 5 recovery phrases. Honest limitations list. | Concrete preparation for admissions interviews. |
| `documentacion/resultados/README.md` | New. Inventory of result templates with status flags. | Single entry point for reviewers. |
| `documentacion/resultados/METRICS_TEMPLATE.md` | New. Per-architecture and per-species metric tables, all marked TBD. Includes a reference table from the predecessor Australian project (F1-macro 0.85) labelled as such. | No fabricated numbers; calibrated reader expectation. |
| `documentacion/resultados/CONFUSION_MATRIX_TEMPLATE.md` | New. Protocol + a-priori confusion-cluster hypotheses. | Frames the matrix as a hypothesis test, not a black-box dump. |
| `documentacion/resultados/GRADCAM_EXAMPLES.md` | New. Interpretability protocol; per-class audit threshold; gallery layout. | Validates the model attends to the bird, not the background. |
| `documentacion/resultados/TRAINING_CURVES.md` | New. Expected curve shape + diagnostic checklist. | Sets reviewer expectations before training completes. |
| `documentacion/resultados/SHORTCUT_LEARNING_FINDING.md` | New. Documented failure mode (sky-colour shortcut) + three-layer mitigation. | Addresses "how do you know the model learned the right thing?" directly. |
| `documentacion/auditorias/AUDIT_REPORT.md` | This file. | Provides the committee with a transparent change log. |

## 2. Errors fixed and improvements applied

1. **Removed "Tesis de Maestría" framing** from the README. The tool is reframed as a `master's research proposal, work in progress`. This avoids the implicit overclaim of a finished thesis.
2. **Dropped the TensorFlow 2.16 badge** from the headline. The primary implementation is PyTorch; the TF mirror is now mentioned only in the repository layout.
3. **Separated the sign-language extension** into its own Section 19 at the end of the README, explicitly labelled as a secondary inclusion deliverable that is not part of the AI evaluation.
4. **Added explicit `Current status` table** with WORKING / IN PROGRESS / PENDING flags per component, so reviewers can see at a glance what is real today vs. planned.
5. **Added honest `Limitations` section** with five concrete items, including "no peer-reviewed publication yet" at the top.
6. **All result numbers in the README are sourced.** Reference numbers from the Australian predecessor project are labelled `from raptor-australia/results/reporte_final.json (2026)`. 53-species placeholders are marked TBD.
7. **`documentacion/resultados/` folder** created with five reporting templates instead of dumping outputs into `codigo/pytorch/outputs/` where committee reviewers may not look.
8. **`documentacion/presentacion_en/INTERVIEW_NOTES.md`** provides ready answers in EN+ES to the ten most likely hard questions for an admissions interview.

## 3. Errors NOT yet fixed (out of scope of this pass)

- The Windows helper scripts now live in `scripts/windows/` and are intended as convenience wrappers, not required infrastructure.
- The TensorFlow mirror in `codigo/tensorflow/` is partially in sync with the PyTorch implementation. For admissions purposes the PyTorch implementation is authoritative. A later pass can either align or remove the TF tree.
- Capítulos 2 and 4 of the thesis drafts in `documentacion/tesis/` predate the V1.1 expansion. They still reference 23 species in places. Not user-facing but should be regenerated before the formal defence.

## 4. Reproducibility verification commands

These are the exact commands a reviewer can run to verify the repository works from a clean checkout.

### 4.1 Install

```bash
# Clone fresh
git clone https://github.com/ZOMBIECRAFTIAN/raptors-cnn.git
cd raptors-cnn

# Choose ONE environment (NVIDIA / CPU / Apple Silicon)
conda env create -f codigo/pytorch/environment.yml          # CUDA
# conda env create -f codigo/pytorch/environment-cpu.yml    # CPU
# conda env create -f codigo/pytorch/environment-mps.yml    # MPS

conda activate raptors-pt                                   # or raptors-pt-cpu / raptors-pt-mps
pip install -r codigo/pytorch/pip-requirements.txt

# Verify the environment
python codigo/pytorch/verify_setup.py
# Expected output: ticks for Python, PyTorch, torchvision; device detected.
```

### 4.2 Smoke test (5 minutes, no real dataset needed)

```bash
cd codigo/pytorch
python make_synthetic_dataset.py        # creates ~980 synthetic images
python train.py --arch resnet50 --smoke-test
# Expected: 1 epoch completes, prints stage1 loss and accuracy, exits 0.
```

### 4.3 Fast end-to-end training (real data, ~30 minutes on RTX 3050)

```bash
cd codigo/pytorch
python download_inaturalist.py --target 50 --max-pages 1   # ~10 min download
python curate.py --apply
python split_dataset.py
python train.py --arch resnet50 --smoke-test               # 5 min
python evaluate.py --arch resnet50 \
                   --weights outputs/checkpoints/best_stage2.pt
# Expected: metrics_resnet50.json with non-zero F1-macro on the small dataset.
```

### 4.4 Inference demo

```bash
cd codigo/pytorch/app_flask
python app.py
# Open http://localhost:5000 and drag-drop any raptor image.
```

### 4.5 Grad-CAM on a single image

```bash
cd codigo/pytorch
python gradcam.py --image ../../datos/processed/test/Buteo_platypterus/<any>.jpg \
                  --arch resnet50 \
                  --weights outputs/checkpoints/best_stage2.pt
# Produces outputs/gradcam_<image>.png with the activation overlay.
```

## 5. Short presentation speech (English)

> "I've built `raptors-cnn`, an open-source AI pipeline that identifies the 53 diurnal raptor species of Mexico from photographs. The technical novelty is that I train deliberately on the silhouette in flight, not on plumage colour, because that is how an expert ornithologist identifies a raptor at distance. I compare four CNN architectures under the same protocol, validate interpretability with Grad-CAM to rule out shortcut learning, and ship the whole thing as multi-platform installable software. The predecessor Australian project reached F1-macro 0.85 on 8 species under the same recipe; the 53-species Mexican benchmark is the next deliverable. The repository documents both what is working today and what is honestly still in progress, and is the basis of my master's research proposal."

## 6. Short presentation speech (Spanish)

> "He construido `raptors-cnn`, un pipeline de IA open source que identifica las 53 especies de rapaces diurnas de México a partir de fotografías. La novedad técnica es que entreno deliberadamente sobre la silueta en vuelo, no sobre el color del plumaje, porque así es como un ornitólogo experto identifica una rapaz a distancia. Comparo cuatro arquitecturas CNN bajo el mismo protocolo, valido interpretabilidad con Grad-CAM para descartar shortcut learning, y distribuyo todo como software instalable multiplataforma. El proyecto predecesor en Australia alcanzó F1-macro de 0.85 sobre 8 especies con la misma receta; el benchmark mexicano de 53 especies es el siguiente entregable. El repositorio documenta tanto lo que funciona hoy como lo que honestamente sigue en desarrollo, y es la base de mi propuesta de investigación de maestría."
