# Scientific Validation Protocol

This document separates preliminary results from thesis-defensible results.
Its purpose is to avoid inflated claims and make the project reproducible.

## 1. Current Metrics

The existing ResNet-50 metrics are **preliminary** because they were produced
with an image-level split. The dataset uses filenames like
`<observationID>_<photoID>`, so multiple photos from the same observation may
appear in train, validation and test at the same time.

Correct interpretation:

- They are an initial technical baseline.
- They should not be presented as final generalisation estimates.
- They must be repeated after regenerating `datos/processed/` with an
  observation-grouped split.

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

Accuracy may decrease compared with the image-level split. That is expected:
the new metric is more honest and scientifically defensible.

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

> Current metrics are preliminary and were generated with an image-level split.
> During auditing, we detected possible observation-level leakage, so the final
> protocol uses `observationID`-grouped splitting, automated dataset auditing
> and retraining before reporting final results.
