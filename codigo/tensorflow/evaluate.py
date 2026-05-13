"""
Evaluación — TensorFlow / Keras.

Mismas métricas y figuras que la versión PyTorch para una comparación 1-a-1.
"""
import argparse
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.metrics import (
    classification_report, confusion_matrix,
    roc_curve, auc, ConfusionMatrixDisplay
)
from sklearn.preprocessing import label_binarize

import config
from data_loader import build_datasets


def collect_predictions(model, ds):
    y_true, y_proba = [], []
    for x, y in ds:
        y_true.append(y.numpy())
        y_proba.append(model.predict(x, verbose=0))
    return np.concatenate(y_true), np.concatenate(y_proba)


def plot_confusion(cm, classes, out):
    fig, ax = plt.subplots(figsize=(9, 8))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=classes)
    disp.plot(ax=ax, cmap="Blues", colorbar=True, xticks_rotation=45)
    plt.tight_layout(); plt.savefig(out, dpi=150); plt.close(fig)


def plot_roc(y_true, y_proba, classes, out):
    y_bin = label_binarize(y_true, classes=range(len(classes)))
    fig, ax = plt.subplots(figsize=(8, 7)); aucs = []
    for i, cls in enumerate(classes):
        fpr, tpr, _ = roc_curve(y_bin[:, i], y_proba[:, i])
        a = auc(fpr, tpr); aucs.append(a)
        ax.plot(fpr, tpr, label=f"{cls} (AUC={a:.3f})")
    ax.plot([0, 1], [0, 1], "k--", lw=1)
    ax.set_xlabel("FPR"); ax.set_ylabel("TPR")
    ax.set_title(f"Curvas ROC — macro-AUC={np.mean(aucs):.3f}")
    ax.legend(fontsize=8, loc="lower right")
    plt.tight_layout(); plt.savefig(out, dpi=150); plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", required=True)
    args = parser.parse_args()

    _, _, test_ds = build_datasets()
    model = tf.keras.models.load_model(args.weights)

    y_true, y_proba = collect_predictions(model, test_ds)
    y_pred = y_proba.argmax(axis=1)

    print(classification_report(y_true, y_pred, target_names=config.SPECIES, digits=4))
    cm = confusion_matrix(y_true, y_pred, normalize="true")
    plot_confusion(cm, config.SPECIES, config.OUTPUT_DIR / "confusion_matrix.png")
    plot_roc(y_true, y_proba, config.SPECIES, config.OUTPUT_DIR / "roc_curves.png")
    print(f"\nFiguras en {config.OUTPUT_DIR}")


if __name__ == "__main__":
    main()
