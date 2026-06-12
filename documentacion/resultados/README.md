# Results

This folder contains **reporting templates and current results** for the `raptors-cnn` project. It is the single place reviewers, supervisors and graduate-admission committees should look for empirical evidence.

> **Honesty notice.** Some files are templates marked `to be filled after training`. Where current Mexico-project numbers appear, they come from a local ResNet-50 run using the observation-level split audited on 2026-06-12. Older image-level numbers are kept only as historical baselines and should not be used as final thesis claims.

## Current thesis-grade baseline

`ResNet-50`, evaluated locally on 2026-06-12 with
`outputs/checkpoints/best_stage2_resnet50.pt`.
This baseline uses an **observation-level split** generated with
`split_dataset.py --group-by-observation` and audited with
`audit_dataset.py --fail-on-leak`.

| Metric | Value |
|---|---:|
| Test images | 2,653 |
| Accuracy | 0.6072 |
| Accuracy 95% CI | 0.5895-0.6246 |
| Balanced accuracy | 0.5808 |
| F1-macro | 0.5837 |
| F1-macro 95% CI | 0.5594-0.6009 |
| F1-weighted | 0.6133 |
| Top-3 accuracy | 0.6958 |
| Macro-AUC | 0.9226 |
| Cohen's kappa | 0.5969 |
| Latency | 19.08 ms/image |
| Model size | 90.40 MB |

Dataset audit summary: train=12,261, val=2,609, test=2,653, with 0
overlapping `observationID`s across train/val/test.

## Files

| File | Purpose | Status |
|---|---|---|
| [`METRICS_TEMPLATE.md`](METRICS_TEMPLATE.md) | Per-architecture and per-species metrics table | Template — fill after training |
| [`CONFUSION_MATRIX_TEMPLATE.md`](CONFUSION_MATRIX_TEMPLATE.md) | 53 × 53 confusion matrix protocol | Template — fill after evaluation |
| [`GRADCAM_EXAMPLES.md`](GRADCAM_EXAMPLES.md) | Grad-CAM interpretability protocol and example gallery | Template + 1 demo example |
| [`ERROR_ANALYSIS_RESNET50_OBSERVATION.md`](ERROR_ANALYSIS_RESNET50_OBSERVATION.md) | Error analysis for the current ResNet-50 observation-level run | Written |
| [`GRADCAM_AUDIT_RESNET50_OBSERVATION.md`](GRADCAM_AUDIT_RESNET50_OBSERVATION.md) | Grad-CAM audit notes for correct/error examples | Written |
| [`TRAINING_CURVES.md`](TRAINING_CURVES.md) | Loss and accuracy curves per stage | Template — fill after training |
| [`SHORTCUT_LEARNING_FINDING.md`](SHORTCUT_LEARNING_FINDING.md) | Documented failure mode and mitigation | Written |

## How results are produced

1. `python codigo/pytorch/audit_dataset.py --fail-on-leak` verifies that no observationID crosses train/val/test.
2. `python codigo/pytorch/train.py --arch <ARCH> --split-protocol observation` runs the two-stage protocol and saves checkpoints to `codigo/pytorch/outputs/checkpoints/`.
   - `outputs/training_history.csv` and `outputs/training_history_<ARCH>.csv` — per-epoch loss/accuracy/lr
   - `outputs/learning_curves.png` and `outputs/learning_curves_<ARCH>.png` — training curves
3. `python codigo/pytorch/evaluate.py --arch <ARCH> --weights <CKPT> --split-protocol observation` produces:
   - `outputs/metrics_<ARCH>.json` — accuracy / F1-macro / top-3 / per-species F1
   - `outputs/classification_report_<ARCH>.txt` — full text report
   - `outputs/confusion_matrix.png` — 53 × 53 normalized confusion-matrix figure
   - `outputs/confusion_matrix_counts_<ARCH>.csv` and `outputs/confusion_matrix_normalized_<ARCH>.csv`
   - `outputs/roc_curves.png` — one-vs-rest ROC curves
4. `python codigo/pytorch/gradcam.py --image <IMG> --weights <CKPT>` produces a Grad-CAM PNG.
5. `python codigo/comparacion/comparar_arquitecturas.py --all` runs all 4 architectures, aggregates the JSONs into `metricas_arquitecturas.csv`, and produces 3 comparison figures in `figures/`.

This `documentacion/resultados/` folder receives **summaries and figures**; raw outputs stay under `codigo/pytorch/outputs/` (gitignored beyond size limits).

## Naming convention

- `<metric>_<arch>_<date>.png|csv|json` for run-specific artefacts.
- `<metric>_summary.md` for the cross-architecture summary tables.
- `gradcam_<species>_<image-id>.png` for explainability images.
