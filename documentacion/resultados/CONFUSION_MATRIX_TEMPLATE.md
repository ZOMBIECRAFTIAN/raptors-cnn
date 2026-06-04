# Confusion matrix — 53 × 53

**Status:** template. *To be filled after training.* The matrix is produced by `codigo/pytorch/evaluate.py` as both a CSV (`outputs/confusion_matrix.csv`) and a PNG (`outputs/confusion_matrix.png`).

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

## Headline figure (to be inserted)

`outputs/confusion_matrix.png` will be referenced here once training completes. Suggested caption:

> **Figure 1.** 53 × 53 confusion matrix on the held-out test set for `<ARCH>`. Counts on log scale. Diagonal density reflects per-class accuracy; off-diagonal clusters indicate systematic confusion. The pre-registered hypotheses for confused pairs (see table above) are marked with red boxes.
