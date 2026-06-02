# Metrics — per-architecture summary

**Status:** template. *To be filled after training.* Numbers will be inserted by `codigo/comparacion/comparar_arquitecturas.py --report`.

## Table 1. Headline metrics across four architectures (53 species, test set)

| Architecture | Params (M) | Input | Accuracy | F1-macro | Top-3 acc | Inference (ms) | Model size (MB) | Train time (h) |
|---|---|---|---|---|---|---|---|---|
| MobileNetV3-Large | 5.5  | 224 | TBD | TBD | TBD | TBD | TBD | TBD |
| EfficientNet-B3   | 12.2 | 300 | TBD | TBD | TBD | TBD | TBD | TBD |
| ResNet-50 *(baseline)* | 25.6 | 224 | TBD | TBD | TBD | TBD | TBD | TBD |
| ConvNeXt-Tiny     | 28.6 | 232 | TBD | TBD | TBD | TBD | TBD | TBD |

**TBD** = to be reported after the full training run. Latency and model size are reported on a fixed reference machine (RTX 3050, 4 GB VRAM; batch size = 1).

## Table 2. Reference results from the Australian predecessor project (8 species)

These are **not** results from the current 53-species Mexico project. They are reported here to give an order-of-magnitude expectation for the same training recipe and are taken from the public sibling repository `raptor-australia`.

| Metric | Value |
|---|---|
| Architecture | EfficientNet-B4 |
| Species | 8 (southeast Australian raptors) |
| Test images | 206 |
| Accuracy | 0.85 |
| F1-macro | 0.85 |
| Best class F1 (Wedge-tailed Eagle) | 0.94 |
| Worst class F1 (Nankeen Kestrel) | 0.74 |
| Source | `raptor-australia/results/reporte_final.json` |
| Date | 2026 |

## Table 3. Per-species F1 (53 species, Mexico) — *to be filled*

A 53-row table will be inserted here from `outputs/metrics_<arch>.json` once training completes.

| # | Code | Scientific name | Common (EN) | Train n | Val n | Test n | F1 | Precision | Recall |
|---|---|---|---|---|---|---|---|---|---|
| 1 | SSHA | Accipiter striatus | Sharp-shinned Hawk | TBD | TBD | TBD | TBD | TBD | TBD |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 53 | BLHE | Spizaetus tyrannus | Black Hawk-Eagle | TBD | TBD | TBD | TBD | TBD | TBD |

## Notes on metric choice

**Primary metric:** F1-macro. Justification: class imbalance is severe (1000× *Cathartes aura* vs ~60× *Harpia harpyja*). Macro-F1 gives equal weight to all species; weighted accuracy alone would understate the failure on rare species.

**Top-3 accuracy** is reported because in practical field use, presenting three plausible candidates is often more useful than a single (possibly wrong) prediction.

**Inference latency** matters for the planned Flask GUI (target: < 1 s per image on consumer GPU). Latency is measured with batch size = 1, AMP enabled, model in eval mode.
