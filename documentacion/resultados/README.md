# Results

This folder contains **reporting templates and current results** for the `raptors-cnn` project. It is the single place reviewers, supervisors and graduate-admission committees should look for empirical evidence.

> **Honesty notice.** Some files are templates marked `to be filled after training`. Where numbers do appear, they come either from (a) a preliminary local ResNet-50 evaluation on the 53-species test split, or (b) the predecessor Australian raptor project used only as external context. The full cross-architecture benchmark will replace the placeholders as soon as all models are evaluated under the same protocol.

## Current preliminary baseline

`ResNet-50`, evaluated locally on 2026-06-06 with `outputs/checkpoints/best_stage2.pt`:

| Metric | Value |
|---|---:|
| Test images | 3,419 |
| Accuracy | 0.5665 |
| F1-macro | 0.5314 |
| Top-3 accuracy | 0.7488 |
| Macro-AUC | 0.9565 |
| Latency | 20.59 ms/image |
| Model size | 90.39 MB |

These values are a baseline for improvement, not final thesis claims.

## Files

| File | Purpose | Status |
|---|---|---|
| [`METRICS_TEMPLATE.md`](METRICS_TEMPLATE.md) | Per-architecture and per-species metrics table | Template — fill after training |
| [`CONFUSION_MATRIX_TEMPLATE.md`](CONFUSION_MATRIX_TEMPLATE.md) | 53 × 53 confusion matrix protocol | Template — fill after evaluation |
| [`GRADCAM_EXAMPLES.md`](GRADCAM_EXAMPLES.md) | Grad-CAM interpretability protocol and example gallery | Template + 1 demo example |
| [`TRAINING_CURVES.md`](TRAINING_CURVES.md) | Loss and accuracy curves per stage | Template — fill after training |
| [`SHORTCUT_LEARNING_FINDING.md`](SHORTCUT_LEARNING_FINDING.md) | Documented failure mode and mitigation | Written |

## How results are produced

1. `python codigo/pytorch/train.py --arch <ARCH>` runs the two-stage protocol and saves checkpoints to `codigo/pytorch/outputs/checkpoints/`.
   - `outputs/training_history.csv` and `outputs/training_history_<ARCH>.csv` — per-epoch loss/accuracy/lr
   - `outputs/learning_curves.png` and `outputs/learning_curves_<ARCH>.png` — training curves
2. `python codigo/pytorch/evaluate.py --arch <ARCH> --weights <CKPT>` produces:
   - `outputs/metrics_<ARCH>.json` — accuracy / F1-macro / top-3 / per-species F1
   - `outputs/classification_report_<ARCH>.txt` — full text report
   - `outputs/confusion_matrix.png` — 53 × 53 normalized confusion-matrix figure
   - `outputs/confusion_matrix_counts_<ARCH>.csv` and `outputs/confusion_matrix_normalized_<ARCH>.csv`
   - `outputs/roc_curves.png` — one-vs-rest ROC curves
3. `python codigo/pytorch/gradcam.py --image <IMG> --weights <CKPT>` produces a Grad-CAM PNG.
4. `python codigo/comparacion/comparar_arquitecturas.py --all` runs all 4 architectures, aggregates the JSONs into `metricas_arquitecturas.csv`, and produces 3 comparison figures in `figures/`.

This `documentacion/resultados/` folder receives **summaries and figures**; raw outputs stay under `codigo/pytorch/outputs/` (gitignored beyond size limits).

## Naming convention

- `<metric>_<arch>_<date>.png|csv|json` for run-specific artefacts.
- `<metric>_summary.md` for the cross-architecture summary tables.
- `gradcam_<species>_<image-id>.png` for explainability images.
