"""
Evaluación del modelo sobre el conjunto test — PyTorch.

Genera:
    - reporte de clasificación por especie (precision, recall, F1)
    - matriz de confusión normalizada
    - curvas ROC + macro-AUC

Uso:
    python evaluate.py --arch resnet50 --weights outputs/checkpoints/best_stage2.pt
"""
import argparse
from pathlib import Path

import numpy as np
import torch
import matplotlib.pyplot as plt
from sklearn.metrics import (
    classification_report, confusion_matrix,
    roc_curve, auc, ConfusionMatrixDisplay
)
from sklearn.preprocessing import label_binarize

import config
from data_loader import build_dataloaders
from model import build_model


@torch.no_grad()
def collect_predictions(model, loader, device):
    model.eval()
    all_logits, all_targets = [], []
    for imgs, targets in loader:
        imgs = imgs.to(device)
        outputs = model(imgs)
        all_logits.append(outputs.cpu())
        all_targets.append(targets)
    return torch.cat(all_logits), torch.cat(all_targets)


def plot_confusion_matrix(cm, classes, out_path):
    fig, ax = plt.subplots(figsize=(9, 8))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=classes)
    disp.plot(ax=ax, cmap="Blues", colorbar=True, xticks_rotation=45)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_roc_curves(y_true, y_proba, classes, out_path):
    y_bin = label_binarize(y_true, classes=range(len(classes)))
    fig, ax = plt.subplots(figsize=(8, 7))
    aucs = []
    for i, cls in enumerate(classes):
        fpr, tpr, _ = roc_curve(y_bin[:, i], y_proba[:, i])
        a = auc(fpr, tpr); aucs.append(a)
        ax.plot(fpr, tpr, label=f"{cls} (AUC={a:.3f})")
    ax.plot([0, 1], [0, 1], "k--", lw=1)
    ax.set_xlabel("False Positive Rate"); ax.set_ylabel("True Positive Rate")
    ax.set_title(f"Curvas ROC — macro-AUC={np.mean(aucs):.3f}")
    ax.legend(fontsize=8, loc="lower right")
    plt.tight_layout(); plt.savefig(out_path, dpi=150); plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--arch", default="resnet50")
    parser.add_argument("--weights", required=True)
    args = parser.parse_args()

    device = config.DEVICE
    _, _, test_loader = build_dataloaders()
    model = build_model(args.arch).to(device)
    model.load_state_dict(torch.load(args.weights, map_location=device))

    logits, targets = collect_predictions(model, test_loader, device)
    proba = torch.softmax(logits, dim=1).numpy()
    preds = proba.argmax(axis=1)
    y_true = targets.numpy()

    print(classification_report(y_true, preds, target_names=config.SPECIES, digits=4))
    cm = confusion_matrix(y_true, preds, normalize="true")
    plot_confusion_matrix(cm, config.SPECIES, config.OUTPUT_DIR / "confusion_matrix.png")
    plot_roc_curves(y_true, proba, config.SPECIES, config.OUTPUT_DIR / "roc_curves.png")
    print(f"\nFiguras guardadas en {config.OUTPUT_DIR}")


if __name__ == "__main__":
    main()
