# Grad-CAM audit: ResNet-50 observation-level run

Run date: 2026-06-12  
Checkpoint: `codigo/pytorch/outputs/checkpoints/best_stage2_resnet50.pt`  
Script: `codigo/pytorch/gradcam_batch.py`  
Output folder: `codigo/pytorch/outputs/gradcam_resnet50_test_audit/`

## What was generated

The batch audit generated 20 Grad-CAM figures from the held-out observation
test split:

- 10 correctly classified examples.
- 10 incorrectly classified examples.
- Focus species included strong classes and weak/error-prone classes:
  `Busarellus_nigricollis`, `Falco_rufigularis`, `Falco_sparverius`,
  `Herpetotheres_cachinnans`, `Elanus_leucurus`,
  `Buteogallus_solitarius`, `Morphnus_guianensis`, `Ictinia_plumbea`,
  `Astur_atricapillus`, `Buteo_platypterus`.

The CSV audit sheet is:

```text
codigo/pytorch/outputs/gradcam_resnet50_test_audit/gradcam_audit.csv
```

That CSV contains the image path, true species, predicted species, confidence,
Grad-CAM image path, and empty `manual_verdict` / `notes` fields for expert
review.

## Reproducibility command

```bash
cd codigo/pytorch
python gradcam_batch.py \
  --arch resnet50 \
  --weights outputs/checkpoints/best_stage2_resnet50.pt \
  --split test \
  --correct 10 \
  --incorrect 10 \
  --focus-species Buteogallus_solitarius Morphnus_guianensis Ictinia_plumbea \
                  Astur_atricapillus Buteo_platypterus Falco_rufigularis \
                  Busarellus_nigricollis Falco_sparverius \
                  Herpetotheres_cachinnans Elanus_leucurus
```

## Spot-check result

Two generated figures were visually inspected:

- `correct_01_true-Busarellus_nigricollis_pred-Busarellus_nigricollis_260581719_467993978.png`
- `incorrect_01_true-Ictinia_plumbea_pred-Ictinia_mississippiensis_101482916_169489295.png`

Both rendered correctly and showed non-blank activation maps. In the inspected
examples, the activation concentrated on the bird body/head region rather than
random empty background. This is a positive sign, but not yet a full
interpretability validation.

## Manual scoring rubric

Use the `manual_verdict` column in `gradcam_audit.csv`:

| Verdict | Meaning |
|---|---|
| `PASS` | Activation peak falls on the bird, especially head, body, wing, or tail. |
| `AUDIT` | Activation peak falls mainly on sky, branches, text, border, watermark, or other background artifact. |
| `UNCLEAR` | Bird is too small, blurry, or occluded to judge activation reliably. |

## Defense note in Spanish

El proyecto no depende solo de accuracy. Tambien se revisa interpretabilidad
con Grad-CAM para verificar que la CNN mire al ave y no al fondo. En esta
auditoria inicial se generaron 20 ejemplos reales del conjunto de prueba:
10 aciertos y 10 errores. La revision manual completa queda registrada en el
CSV local para que el analisis sea trazable.

## Why images are not committed

The generated Grad-CAM PNGs are derived from local dataset images. They stay
under `codigo/pytorch/outputs/`, which is gitignored, to avoid publishing large
artifacts or media whose redistribution must be checked image by image.
