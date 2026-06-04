# Grad-CAM examples and interpretability protocol

**Status:** protocol written. Worked demo on synthetic data validated. *Per-class gallery to be filled after training the 53-species model.*

Grad-CAM (Selvaraju et al., *IJCV* 2020) produces gradient-weighted class activation maps that highlight which image regions a CNN used to make its decision. For raptor identification, the audit question is: **does the model attend to the bird, or to the sky / canopy?**

## Validation protocol

1. Train the model end-to-end (Stage 1 + Stage 2) on the 53-species split.
2. For each species, sample at least 20 test images.
3. For each image, generate the Grad-CAM map on the last convolutional block (`layer4` for ResNet-50, `features.7` for EfficientNet-B3, etc.).
4. Manually inspect the activation peak:
   - **Pass** — peak falls on the bird's silhouette, especially on diagnostic features (wingtip, tail, head).
   - **Audit** — peak falls on background, cloud, water, vegetation, or off-image artefacts. Image is flagged for `outputs/gradcam_audit.csv`.
5. Compute the **attention precision** per species: fraction of images that pass the audit. Target: ≥ 0.90.
6. If a class falls below 0.80 attention precision but still has high F1, this is a strong signal of **shortcut learning** — see [`SHORTCUT_LEARNING_FINDING.md`](SHORTCUT_LEARNING_FINDING.md).

## Why this matters beyond a number

A 95 % accuracy model that attends to *the sky* is worse than an 85 % model that attends to the bird. The first will fail catastrophically when deployed to a new geography where the background distribution shifts. The second will generalise. **Grad-CAM is the only cheap tool that surfaces this distinction.**

## Demo example (current — synthetic data, V1 subset)

A working Grad-CAM image is saved at `codigo/pytorch/outputs/gradcam_BW_test_0000.png` from a smoke-test run on the 23-species V1 subset (Broad-winged Hawk, *Buteo platypterus*). The activation peak falls on the wing silhouette as expected. This is a demo of the *machinery*, not a validation of the V1.1 model.

## Per-class gallery (to be filled after training)

The gallery layout will be: 4 images per row, one row per species, captioned with predicted class and the audit verdict.

```
[ image ]   [ image ]   [ image ]   [ image ]
Buteo platypterus — PASS · PASS · AUDIT · PASS
[ image ]   [ image ]   [ image ]   [ image ]
Accipiter striatus — PASS · PASS · PASS · PASS
...
```

A mosaic figure (`documentacion/resultados/gradcam_mosaic_53.png`) will be the headline interpretability figure of the thesis.

## References

- Selvaraju, R. R., Cogswell, M., Das, A., Vedantam, R., Parikh, D., & Batra, D. (2020). Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization. *IJCV*, 128, 336–359.
- Geirhos, R., Jacobsen, J.-H., Michaelis, C., Zemel, R., Brendel, W., Bethge, M., & Wichmann, F. A. (2020). Shortcut learning in deep neural networks. *Nature Machine Intelligence*, 2(11), 665–673.
