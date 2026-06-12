"""
Batch Grad-CAM audit for correct and incorrect test examples.

The script scans an ImageFolder split, predicts with a trained checkpoint,
selects a fixed number of correct and incorrect examples, and writes Grad-CAM
figures plus a CSV audit sheet. The images stay under outputs/ and are intended
for local review, not for GitHub.
"""
import argparse
import csv
import random
from pathlib import Path

import matplotlib.pyplot as plt
import torch
from PIL import Image
from torchvision import datasets

import config
from data_loader import get_transforms
from gradcam import GradCAM, get_target_layer
from model import build_model


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--arch", default="resnet50")
    parser.add_argument(
        "--weights",
        default=str(config.CHECKPOINT_DIR / "best_stage2_resnet50.pt"),
    )
    parser.add_argument("--processed-dir", type=Path, default=config.PROCESSED_DIR)
    parser.add_argument("--split", default="test", choices=["train", "val", "test"])
    parser.add_argument("--out-dir", type=Path, default=None)
    parser.add_argument("--correct", type=int, default=8)
    parser.add_argument("--incorrect", type=int, default=8)
    parser.add_argument("--seed", type=int, default=config.SEED)
    parser.add_argument("--max-scan", type=int, default=0)
    parser.add_argument("--focus-species", nargs="*", default=None)
    return parser.parse_args()


def safe_name(value: str) -> str:
    return value.replace(" ", "_").replace("/", "_").replace("\\", "_")


def save_gradcam_figure(image, cam, true_name, pred_name, confidence, out_path):
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    ax[0].imshow(image)
    ax[0].set_title(f"True: {true_name}")
    ax[0].axis("off")
    ax[1].imshow(image)
    ax[1].imshow(cam, cmap="jet", alpha=0.5)
    ax[1].set_title(f"Pred: {pred_name} ({confidence:.3f})")
    ax[1].axis("off")
    plt.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def main():
    args = parse_args()
    device = config.DEVICE
    input_size = config.input_size_for_arch(args.arch)
    out_dir = args.out_dir or (config.OUTPUT_DIR / f"gradcam_{args.arch}_{args.split}_audit")
    out_dir.mkdir(parents=True, exist_ok=True)

    _, eval_tf = get_transforms(input_size)
    dataset = datasets.ImageFolder(args.processed_dir / args.split, transform=eval_tf)
    if dataset.classes != config.SPECIES:
        raise RuntimeError("Dataset classes do not match config.SPECIES order.")

    model = build_model(args.arch, pretrained=False).to(device)
    model.load_state_dict(torch.load(args.weights, map_location=device))
    model.eval()
    cam_engine = GradCAM(model, get_target_layer(model, args.arch))

    samples = list(dataset.samples)
    if args.focus_species:
        focus = set(args.focus_species)
        samples = [(p, y) for p, y in samples if config.SPECIES[y] in focus]
    rng = random.Random(args.seed)
    rng.shuffle(samples)
    if args.max_scan and args.max_scan > 0:
        samples = samples[: args.max_scan]

    selected = {"correct": 0, "incorrect": 0}
    rows = []

    for path, true_idx in samples:
        if selected["correct"] >= args.correct and selected["incorrect"] >= args.incorrect:
            break

        original = Image.open(path).convert("RGB")
        x = eval_tf(original).unsqueeze(0).to(device)
        with torch.no_grad():
            probs = torch.softmax(model(x), dim=1)[0]
            confidence, pred_idx_tensor = probs.max(dim=0)
        pred_idx = int(pred_idx_tensor.item())
        is_correct = pred_idx == true_idx
        kind = "correct" if is_correct else "incorrect"
        if selected[kind] >= getattr(args, kind):
            continue

        cam, _ = cam_engine(x)
        true_name = config.SPECIES[true_idx]
        pred_name = config.SPECIES[pred_idx]
        resized = original.resize((input_size, input_size))
        stem = safe_name(Path(path).stem)
        out_path = out_dir / (
            f"{kind}_{selected[kind] + 1:02d}_"
            f"true-{safe_name(true_name)}_pred-{safe_name(pred_name)}_{stem}.png"
        )
        save_gradcam_figure(
            resized,
            cam,
            true_name,
            pred_name,
            float(confidence.item()),
            out_path,
        )
        rows.append(
            {
                "kind": kind,
                "image_path": str(path),
                "true_species": true_name,
                "predicted_species": pred_name,
                "confidence": f"{float(confidence.item()):.6f}",
                "gradcam_path": str(out_path),
                "manual_verdict": "",
                "notes": "",
            }
        )
        selected[kind] += 1

    csv_path = out_dir / "gradcam_audit.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "kind",
                "image_path",
                "true_species",
                "predicted_species",
                "confidence",
                "gradcam_path",
                "manual_verdict",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {len(rows)} Grad-CAM examples to {out_dir}")
    print(f"Audit CSV: {csv_path}")
    print(f"Correct: {selected['correct']} | Incorrect: {selected['incorrect']}")


if __name__ == "__main__":
    main()
