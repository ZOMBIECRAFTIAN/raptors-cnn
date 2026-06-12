# Scientific Validation Protocol

This document separates preliminary results from thesis-defensible results.
Its purpose is to avoid inflated claims and make the project reproducible.

## 1. Current Metrics

ResNet-50 has now been retrained and evaluated with the defensible
`observationID` protocol. The dataset audit reports 0 observation leaks across
train, validation and test.

Local result from 2026-06-12:

| Metric | Value |
|---|---:|
| Test images | 2,653 |
| Accuracy | 0.6072 |
| Accuracy 95% CI | 0.5895-0.6246 |
| Balanced accuracy | 0.5808 |
| F1-macro | 0.5837 |
| F1-macro 95% CI | 0.5594-0.6009 |
| Top-3 accuracy | 0.6958 |
| Macro-AUC | 0.9226 |
| Cohen's kappa | 0.5969 |

Correct interpretation:

- These numbers are more defensible than the older image-level baseline.
- Very low-support species remain inconclusive at species level.
- Other architectures still require their own runs; they should not be inferred
  from ResNet-50.

## 2. Thesis-Grade Split

The defensible split is grouped by observation:

```bash
cd codigo/pytorch
python split_dataset.py --group-by-observation --clean --link
python audit_dataset.py --fail-on-leak
```

To keep the previous split for historical comparison:

```bash
python split_dataset.py --group-by-observation --processed-dir ../../datos/processed_grouped --clean --link
python audit_dataset.py --processed-dir ../../datos/processed_grouped --fail-on-leak
```

Then retrain and re-evaluate:

```bash
python train.py --arch resnet50 --split-protocol observation
python evaluate.py --arch resnet50 \
  --weights outputs/checkpoints/best_stage2_resnet50.pt \
  --split-protocol observation
```

Accuracy may differ from the image-level split. That is expected: the
observation-grouped metric is more honest and scientifically defensible.

## 3. Mandatory Dataset Audit

Before training or reporting:

```bash
python audit_dataset.py --check-images
```

The audit checks:

- per-species counts by split;
- `observationID` leakage across train/val/test;
- low-support species;
- unsupported files in `datos/processed`;
- GIF files in `datos/raw`;
- corrupt images when `--check-images` is enabled.

## 4. Rare Species

Species with `train < 50`, `val < 10` or `test < 10` have unstable per-species
metrics. They should be reported as low-support classes, not as definitive
model failures.

Acceptable strategies:

- targeted data collection for rare species;
- reporting metrics by taxonomic family in addition to species;
- hierarchical classification family -> genus -> species;
- top-3 accuracy as an ecologically realistic metric.

## 5. Architectures and Frameworks

PyTorch is the main implementation. TensorFlow is a partial mirror and should
not yet be presented as an equivalent experimental comparison because it does
not share the full advanced training protocol.

The architecture benchmark is complete only when each backbone has:

- architecture-specific checkpoint;
- `metrics_<arch>.json`;
- classification report;
- confusion matrix;
- latency and model size;
- training/evaluation manifest.

## 6. YOLO and Behaviour

YOLO is implemented as a functional prototype for video detection and tracking.
It is not yet a final validated behaviour result.

To defend it as a scientific module, it needs:

- annotated bounding boxes;
- mAP50 and mAP50-95;
- tracking evaluation;
- temporal behaviour labels;
- comparison against a baseline.

## 7. Recommended Defense Statement

> The current ResNet-50 metrics were regenerated with `observationID`-grouped
> splitting and automated auditing with no leakage across train, validation and
> test. Rare species are still reported cautiously because some have fewer than
> 10 test images.
