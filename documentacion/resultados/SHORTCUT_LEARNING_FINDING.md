# Shortcut learning — documented failure mode and mitigation

**Status:** finding written based on the literature, on the predecessor Australian project, and on smoke-test inspection. To be re-confirmed on the 53-species model.

## What "shortcut learning" means here

A model is said to exhibit **shortcut learning** (Geirhos et al., *Nature Machine Intelligence* 2020) when it achieves high accuracy by exploiting features that correlate with the label in the training distribution but do not reflect the actual task. For raptor identification, the most common shortcuts are:

| Shortcut | Concretely |
|---|---|
| **Sky colour** | *Cathartes aura* is photographed on hot summer afternoons → blue sky is a "spurious" cue. |
| **Habitat backdrop** | *Spizaetus tyrannus* is always in tropical canopy → green pixels predict the species. |
| **Watermark** | Some Macaulay-derived JPEGs have a small bottom-right © watermark from a particular contributor who specialises in one species. |
| **Photo orientation** | Portrait vs landscape correlates with photographer style, not species. |
| **Bounding-frame artefacts** | An iNaturalist crop signature can leak. |

## Why this matters

A model that wins by shortcut will fail catastrophically when deployed on:

- a different photographer / dataset,
- a different geography (e.g. a Mexican raptor photographed in Texas),
- a low-light or atypical-background field condition.

Validation accuracy alone cannot detect this. **Interpretability tools can.**

## How this project diagnoses shortcut learning

Three diagnostic layers stack on top of one another:

1. **Augmentation ablation.** The pipeline removes the "silhouette-targeted" augmentations (saturation jitter, grayscale, RandomErasing) and re-runs training. If accuracy *increases* without those augmentations, the model is exploiting plumage colour. The expected outcome with the augmentations is *lower* training accuracy but *higher* test generalisation.
2. **Grad-CAM audit.** See [`GRADCAM_EXAMPLES.md`](GRADCAM_EXAMPLES.md). For each test image, the activation peak must land on the bird; otherwise the image is logged for review.
3. **Cross-source held-out test.** A test sub-set drawn from a different source (e.g. eBird checklists, not iNaturalist research-grade) is reserved. A drop > 10 percentage points between iNaturalist test accuracy and eBird test accuracy is the diagnostic threshold.

## Expected finding (a priori, to be confirmed)

Based on the Australian predecessor project and the smoke tests run on the V1 (23-species) subset, the most likely shortcut to surface is **sky colour for soaring species** (*Cathartes*, *Buteo platypterus*, *Buteo swainsoni*). The augmentation pipeline already weakens this shortcut, but the Grad-CAM audit may still surface 5–10 % of test images where the peak falls on sky.

The mitigation if this is observed:

- Increase saturation jitter from 0.4 to 0.5.
- Add a `RandomFog` or `RandomCloud` augmentation to decorrelate sky pattern from species.
- Re-train and re-audit.

## Why this is a contribution

Most published raptor identifiers report only accuracy and F1, without auditing for shortcut learning. **Documenting the finding, the mitigation and the residual risk is one of the contributions of this thesis.** It is also one of the most powerful answers to the interview question *"how do you know your model actually learned what you say it learned?"*

## References

- Geirhos, R., Jacobsen, J.-H., Michaelis, C., Zemel, R., Brendel, W., Bethge, M., & Wichmann, F. A. (2020). Shortcut learning in deep neural networks. *Nature Machine Intelligence*, 2(11), 665–673.
- Lapuschkin, S., Wäldchen, S., Binder, A., Montavon, G., Samek, W., & Müller, K.-R. (2019). Unmasking Clever Hans predictors. *Nature Communications*, 10, 1096.
- Beery, S., Van Horn, G., & Perona, P. (2018). Recognition in Terra Incognita. *ECCV*.
