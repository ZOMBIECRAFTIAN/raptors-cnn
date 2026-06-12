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
import csv
import json
import time
from pathlib import Path

import numpy as np
import torch
import matplotlib.pyplot as plt
from sklearn.metrics import (
    classification_report, confusion_matrix,
    roc_curve, auc, ConfusionMatrixDisplay,
    accuracy_score, balanced_accuracy_score, cohen_kappa_score,
    f1_score, top_k_accuracy_score
)
from sklearn.preprocessing import label_binarize

import config
from data_loader import build_dataloaders
from experiment_utils import runtime_metadata
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


def write_confusion_csv(cm, classes, out_path):
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["true\\pred", *classes])
        for cls, row in zip(classes, cm):
            writer.writerow([cls, *row])


def plot_roc_curves(y_true, y_proba, classes, out_path):
    y_bin = label_binarize(y_true, classes=range(len(classes)))
    fig, ax = plt.subplots(figsize=(8, 7))
    aucs = []
    for i, cls in enumerate(classes):
        if len(np.unique(y_bin[:, i])) < 2:
            continue
        fpr, tpr, _ = roc_curve(y_bin[:, i], y_proba[:, i])
        a = auc(fpr, tpr); aucs.append(a)
        ax.plot(fpr, tpr, label=f"{cls} (AUC={a:.3f})")
    ax.plot([0, 1], [0, 1], "k--", lw=1)
    ax.set_xlabel("False Positive Rate"); ax.set_ylabel("True Positive Rate")
    ax.set_title(f"Curvas ROC — macro-AUC={np.mean(aucs):.3f}")
    ax.legend(fontsize=8, loc="lower right")
    plt.tight_layout(); plt.savefig(out_path, dpi=150); plt.close(fig)
    return float(np.mean(aucs)) if aucs else 0.0


def bootstrap_confidence_intervals(y_true, preds, proba, *, iters: int, seed: int):
    """Bootstrap 95% CI for headline metrics."""
    if iters <= 0:
        return {}
    rng = np.random.default_rng(seed)
    n = len(y_true)
    labels = np.arange(config.NUM_CLASSES)
    rows = {"accuracy": [], "f1_macro": [], "top3_accuracy": []}
    for _ in range(iters):
        idx = rng.integers(0, n, size=n)
        yt = y_true[idx]
        yp = preds[idx]
        pp = proba[idx]
        rows["accuracy"].append(accuracy_score(yt, yp))
        rows["f1_macro"].append(f1_score(
            yt, yp, average="macro", labels=labels, zero_division=0
        ))
        rows["top3_accuracy"].append(top_k_accuracy_score(
            yt, pp, k=min(3, config.NUM_CLASSES), labels=labels
        ))
    return {
        key: {
            "low": float(np.percentile(values, 2.5)),
            "high": float(np.percentile(values, 97.5)),
        }
        for key, values in rows.items()
    }


def compute_family_metrics(y_true, preds):
    """Metrics grouped by taxonomic family for coarse-grained analysis."""
    out = {}
    families = sorted(set(config.SPECIES_FAMILY))
    for family in families:
        indices = [
            i for i, fam in enumerate(config.SPECIES_FAMILY)
            if fam == family
        ]
        mask = np.isin(y_true, indices)
        if not np.any(mask):
            out[family] = {"support": 0, "accuracy": None, "f1_macro": None}
            continue
        out[family] = {
            "support": int(mask.sum()),
            "accuracy": float(accuracy_score(y_true[mask], preds[mask])),
            "f1_macro": float(f1_score(
                y_true[mask], preds[mask],
                average="macro", labels=indices, zero_division=0,
            )),
        }
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--arch", default="resnet50")
    parser.add_argument("--weights", required=True)
    parser.add_argument("--split-protocol", default="unknown",
                        choices=["image", "observation", "unknown"],
                        help="Protocolo usado para crear el test set")
    parser.add_argument("--processed-dir", type=Path, default=config.PROCESSED_DIR,
                        help="Directorio con train/val/test")
    parser.add_argument("--bootstrap-iters", type=int, default=1000,
                        help="Iteraciones bootstrap para IC 95%%; 0 desactiva")
    args = parser.parse_args()

    device = config.DEVICE
    input_size = config.input_size_for_arch(args.arch)
    _, _, test_loader = build_dataloaders(
        processed_dir=args.processed_dir,
        input_size=input_size,
    )
    model = build_model(args.arch).to(device)
    model.load_state_dict(torch.load(args.weights, map_location=device))

    t0 = time.perf_counter()
    logits, targets = collect_predictions(model, test_loader, device)
    elapsed = time.perf_counter() - t0
    proba = torch.softmax(logits, dim=1).numpy()
    preds = proba.argmax(axis=1)
    y_true = targets.numpy()

    report = classification_report(
        y_true, preds,
        target_names=config.SPECIES,
        digits=4,
        zero_division=0,
        output_dict=True,
    )
    report_text = classification_report(
        y_true, preds,
        target_names=config.SPECIES,
        digits=4,
        zero_division=0,
    )
    print(report_text)
    cm_counts = confusion_matrix(y_true, preds)
    cm = confusion_matrix(y_true, preds, normalize="true")
    plot_confusion_matrix(cm, config.SPECIES, config.OUTPUT_DIR / "confusion_matrix.png")
    write_confusion_csv(
        cm_counts,
        config.SPECIES,
        config.OUTPUT_DIR / f"confusion_matrix_counts_{args.arch}.csv",
    )
    write_confusion_csv(
        cm,
        config.SPECIES,
        config.OUTPUT_DIR / f"confusion_matrix_normalized_{args.arch}.csv",
    )
    macro_auc = plot_roc_curves(y_true, proba, config.SPECIES, config.OUTPUT_DIR / "roc_curves.png")

    labels = np.arange(config.NUM_CLASSES)
    top3 = top_k_accuracy_score(
        y_true,
        proba,
        k=min(3, config.NUM_CLASSES),
        labels=labels,
    )
    ci95 = bootstrap_confidence_intervals(
        y_true, preds, proba,
        iters=args.bootstrap_iters,
        seed=config.SEED,
    )
    model_size_mb = None
    weights_path = Path(args.weights)
    if weights_path.exists():
        model_size_mb = weights_path.stat().st_size / (1024 * 1024)

    per_species = {}
    for species in config.SPECIES:
        row = report.get(species, {})
        per_species[species] = {
            "precision": float(row.get("precision", 0.0)),
            "recall": float(row.get("recall", 0.0)),
            "f1": float(row.get("f1-score", 0.0)),
            "support": int(row.get("support", 0)),
        }

    metrics_out = {
        "metadata": runtime_metadata(config.PROJECT_ROOT, args.processed_dir),
        "arch": args.arch,
        "weights": str(weights_path),
        "split_protocol": args.split_protocol,
        "processed_dir": str(args.processed_dir),
        "num_classes": config.NUM_CLASSES,
        "num_test_images": int(len(y_true)),
        "accuracy": float(accuracy_score(y_true, preds)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, preds)),
        "cohen_kappa": float(cohen_kappa_score(y_true, preds)),
        "f1_macro": float(f1_score(y_true, preds, average="macro", zero_division=0)),
        "f1_weighted": float(f1_score(y_true, preds, average="weighted", zero_division=0)),
        "top3_accuracy": float(top3),
        "ci95": ci95,
        "macro_auc": float(macro_auc),
        "latency_ms_per_image": float((elapsed / max(1, len(y_true))) * 1000),
        "model_size_mb": None if model_size_mb is None else float(model_size_mb),
        "family_metrics": compute_family_metrics(y_true, preds),
        "per_species": per_species,
    }

    out_json = config.OUTPUT_DIR / f"metrics_{args.arch}.json"
    out_txt = config.OUTPUT_DIR / f"classification_report_{args.arch}.txt"
    out_json.write_text(json.dumps(metrics_out, indent=2, ensure_ascii=False), encoding="utf-8")
    out_txt.write_text(report_text, encoding="utf-8")

    print(f"\nFiguras guardadas en {config.OUTPUT_DIR}")
    print(f"Métricas JSON guardadas en {out_json}")
    print(f"Reporte de clasificación guardado en {out_txt}")


if __name__ == "__main__":
    main()
