# Confusion matrix — 53 × 53

**Status:** ResNet-50 observation-level matrix available locally. The matrix is
produced by `codigo/pytorch/evaluate.py` as both CSV
(`outputs/confusion_matrix_counts_resnet50.csv`) and PNG
(`outputs/confusion_matrix.png`).

## Protocol

1. Run `python codigo/pytorch/evaluate.py --arch <ARCH> --weights <CKPT>`.
2. The script generates a 53 × 53 numpy array; rows are true labels in alphabetical scientific-name order, columns are predicted labels.
3. The PNG is plotted with `matplotlib` using `imshow` + a log-scale colour map so rare-class errors remain visible.
4. The CSV is human-readable and used for the per-species F1 table in `METRICS_TEMPLATE.md`.

## Expected confusion clusters (a priori hypotheses)

Based on field-guide knowledge and expert-confusion literature, the following pairs are expected to be the hardest. The behaviour module (`gradcam` + temporal prior) targets exactly these pairs.

| Pair | Why it is hard | Mitigation |
|---|---|---|
| *Accipiter striatus* vs *Astur cooperii* | Same genus historically; size difference is the only field mark | Behaviour: wingbeat cadence |
| *Buteo platypterus* vs *Buteo swainsoni* | Both migrate through Veracruz in soaring kettles | Behaviour: kettle formation count |
| *Buteogallus anthracinus* vs *Buteogallus urubitinga* | Same genus; juveniles especially similar | Geographic prior + size |
| *Spizaetus ornatus* vs *Spizaetus tyrannus* | Both tropical canopy raptors; juveniles confusing | Plumage detail when available |
| *Cathartes aura* vs *Cathartes burrovianus* | Same genus; difference is head colour | Often a known limitation; flag low confidence |

The matrix produced from training will be compared against these hypotheses. **Confirming or refuting the predicted confusion clusters is itself a contribution.**

## Observed confusion clusters: ResNet-50 observation split

Top off-diagonal pairs from the 2026-06-12 run:

| True species | Predicted species | Count | Interpretation |
|---|---|---:|---|
| *Ictinia plumbea* | *Ictinia mississippiensis* | 27 | Same genus; likely silhouette and flight-style similarity. |
| *Accipiter striatus* | *Astur cooperii* | 20 | Known field-identification pair; size and wingbeat cues matter. |
| *Astur cooperii* | *Accipiter striatus* | 17 | Reciprocal confusion in the same accipiter/goshawk complex. |
| *Buteo jamaicensis* | *Buteo platypterus* | 15 | Buteo silhouette overlap in distant flight photographs. |
| *Buteo jamaicensis* | *Buteo lineatus* | 15 | Broad Buteo confusion; requires better wing/tail diagnostic focus. |
| *Buteo platypterus* | *Buteo lineatus* | 12 | Similar perched/soaring image bias likely contributes. |
| *Buteogallus urubitinga* | *Buteogallus anthracinus* | 12 | Same genus; expected by the pre-registered hypothesis. |

These errors are biologically plausible rather than random noise. They support
the decision to include Grad-CAM, YOLO-based flight behaviour and top-3 output
instead of treating single-label top-1 accuracy as the only evidence.

## Headline figure (to be inserted)

`outputs/confusion_matrix.png` will be referenced here once training completes. Suggested caption:

> **Figure 1.** 53 × 53 confusion matrix on the held-out test set for `<ARCH>`. Counts on log scale. Diagonal density reflects per-class accuracy; off-diagonal clusters indicate systematic confusion. The pre-registered hypotheses for confused pairs (see table above) are marked with red boxes.
