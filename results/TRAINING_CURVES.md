# Training curves

**Status:** template. *To be filled after training.* Curves are saved to `outputs/training_history.csv` by `train.py` and plotted automatically into `outputs/learning_curves.png`.

## Expected curve shape (a priori)

For each architecture we expect two visible regimes:

- **Stage 1 (epochs 1–10).** Sharp initial drop in training loss and a fast climb in validation accuracy as the freshly initialised classifier head learns. Validation accuracy should plateau between 0.40 and 0.55 (Stage 1 only).
- **Stage 2 (epochs 11–onward).** A second, slower decline in loss as the backbone fine-tunes. Validation accuracy climbs to its plateau (target ≥ 0.80) over 30–60 epochs. Early stopping fires when validation accuracy has not improved for 15 consecutive epochs.

A divergence between training and validation loss is the first signal of overfitting. With the current augmentation pipeline (Mixup, CutMix, RandomErasing) we expect the gap to remain small (< 0.10 in loss units, < 0.05 in accuracy).

## Per-architecture curves to be inserted

| Architecture | File | Status |
|---|---|---|
| ResNet-50 *(baseline)* | `learning_curves_resnet50.png` | TBD |
| EfficientNet-B3 | `learning_curves_efficientnet_b3.png` | TBD |
| MobileNetV3-Large | `learning_curves_mobilenet_v3.png` | TBD |
| ConvNeXt-Tiny | `learning_curves_convnext_tiny.png` | TBD |

## Diagnostic checklist

When the curves are produced, the author will check:

- [ ] Training loss is monotonically non-increasing within each stage.
- [ ] Validation loss decreases for the first 30 epochs of Stage 2.
- [ ] Train–val gap stays below 0.10 in loss.
- [ ] Early stopping fires before epoch 80 (otherwise the protocol must extend).
- [ ] Learning-rate schedule (cosine) is visible as a smooth decay overlaid on the loss plot.

If any check fails, the failure is documented and the hyperparameters re-tuned (typically `weight_decay`, `mixup_alpha`, or `early_stopping_patience`).
