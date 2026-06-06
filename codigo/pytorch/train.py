"""
Pipeline de entrenamiento — PyTorch.

Implementa la estrategia en dos etapas:
    Etapa 1 — feature extraction (backbone congelado).
    Etapa 2 — fine-tuning (backbone descongelado, lr más bajo, augmentation rica).

Uso:
    python train.py --arch resnet50
    python train.py --arch efficientnet_b3 --skip-stage1
"""
import argparse
import csv
import math
import random
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torch.optim import Adam, AdamW

import config
from data_loader import build_dataloaders, class_weights
from model import build_model, freeze_backbone, unfreeze_all, count_parameters


def set_seed(seed: int = config.SEED) -> None:
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def mixup_data(x, y, alpha: float):
    """Aplica Mixup y devuelve targets pareados."""
    lam = np.random.beta(alpha, alpha) if alpha and alpha > 0 else 1.0
    index = torch.randperm(x.size(0), device=x.device)
    mixed_x = lam * x + (1.0 - lam) * x[index]
    return mixed_x, y, y[index], float(lam)


def _rand_bbox(size, lam: float):
    """Bounding box aleatorio para CutMix sobre tensores NCHW."""
    height, width = size[2], size[3]
    cut_ratio = math.sqrt(1.0 - lam)
    cut_w = int(width * cut_ratio)
    cut_h = int(height * cut_ratio)

    cx = np.random.randint(width)
    cy = np.random.randint(height)

    x1 = np.clip(cx - cut_w // 2, 0, width)
    y1 = np.clip(cy - cut_h // 2, 0, height)
    x2 = np.clip(cx + cut_w // 2, 0, width)
    y2 = np.clip(cy + cut_h // 2, 0, height)
    return int(x1), int(y1), int(x2), int(y2)


def cutmix_data(x, y, alpha: float):
    """Aplica CutMix y ajusta lambda según el área realmente reemplazada."""
    lam = np.random.beta(alpha, alpha) if alpha and alpha > 0 else 1.0
    index = torch.randperm(x.size(0), device=x.device)
    x1, y1, x2, y2 = _rand_bbox(x.size(), lam)

    mixed_x = x.clone()
    mixed_x[:, :, y1:y2, x1:x2] = x[index, :, y1:y2, x1:x2]
    area = (x2 - x1) * (y2 - y1)
    lam = 1.0 - area / float(x.size(2) * x.size(3))
    return mixed_x, y, y[index], float(lam)


def mixed_criterion(criterion, outputs, y_a, y_b, lam: float):
    """Calcula la pérdida para Mixup/CutMix usando el criterio base."""
    return lam * criterion(outputs, y_a) + (1.0 - lam) * criterion(outputs, y_b)


def apply_batch_mixing(imgs, targets, mixup_alpha: float, cutmix_alpha: float):
    """Elige Mixup o CutMix cuando están habilitados para el stage."""
    if imgs.size(0) < 2:
        return imgs, targets, None, 1.0, "none"
    candidates = []
    if mixup_alpha and mixup_alpha > 0:
        candidates.append("mixup")
    if cutmix_alpha and cutmix_alpha > 0:
        candidates.append("cutmix")
    if not candidates:
        return imgs, targets, None, 1.0, "none"

    choice = random.choice(candidates)
    if choice == "mixup":
        mixed, y_a, y_b, lam = mixup_data(imgs, targets, mixup_alpha)
    else:
        mixed, y_a, y_b, lam = cutmix_data(imgs, targets, cutmix_alpha)
    return mixed, y_a, y_b, lam, choice


def set_epoch_lr(optimizer, base_lrs, stage_cfg, epoch: int):
    """Warmup lineal + cosine decay controlado por época."""
    warmup = int(stage_cfg.get("warmup_epochs", 0) or 0)
    epochs = int(stage_cfg["epochs"])
    if warmup and epoch <= warmup:
        factor = epoch / warmup
    elif stage_cfg.get("scheduler") == "cosine":
        denom = max(1, epochs - warmup)
        progress = max(0, epoch - warmup - 1) / denom
        factor = 0.5 * (1.0 + math.cos(math.pi * progress))
    else:
        factor = 1.0

    for param_group, base_lr in zip(optimizer.param_groups, base_lrs):
        param_group["lr"] = base_lr * factor
    return optimizer.param_groups[0]["lr"]


def train_one_epoch(model, loader, criterion, optimizer, device, scaler=None,
                    accum_steps: int = 1, mixup_alpha: float = 0.0,
                    cutmix_alpha: float = 0.0):
    """Una epoch de entrenamiento con soporte para AMP y gradient accumulation."""
    model.train()
    running_loss, correct, total = 0.0, 0, 0
    optimizer.zero_grad(set_to_none=True)
    for step, (imgs, targets) in enumerate(loader):
        imgs, targets = imgs.to(device), targets.to(device)
        imgs, targets_a, targets_b, lam, _ = apply_batch_mixing(
            imgs, targets, mixup_alpha, cutmix_alpha
        )

        if scaler is not None:
            with torch.cuda.amp.autocast():
                outputs = model(imgs)
                if targets_b is not None:
                    loss = mixed_criterion(criterion, outputs, targets_a, targets_b, lam)
                else:
                    loss = criterion(outputs, targets_a)
                loss = loss / accum_steps
            scaler.scale(loss).backward()
            if (step + 1) % accum_steps == 0:
                scaler.step(optimizer)
                scaler.update()
                optimizer.zero_grad(set_to_none=True)
        else:
            outputs = model(imgs)
            if targets_b is not None:
                loss = mixed_criterion(criterion, outputs, targets_a, targets_b, lam)
            else:
                loss = criterion(outputs, targets_a)
            loss = loss / accum_steps
            loss.backward()
            if (step + 1) % accum_steps == 0:
                optimizer.step()
                optimizer.zero_grad(set_to_none=True)

        running_loss += loss.item() * imgs.size(0) * accum_steps
        _, preds = outputs.max(1)
        correct += (preds == targets_a).sum().item()
        total += imgs.size(0)

    if len(loader) % accum_steps != 0:
        if scaler is not None:
            scaler.step(optimizer)
            scaler.update()
        else:
            optimizer.step()
        optimizer.zero_grad(set_to_none=True)

    return running_loss / total, correct / total


@torch.no_grad()
def evaluate(model, loader, criterion, device):
    model.eval()
    running_loss, correct, total = 0.0, 0, 0
    for imgs, targets in loader:
        imgs, targets = imgs.to(device), targets.to(device)
        outputs = model(imgs)
        loss = criterion(outputs, targets)
        running_loss += loss.item() * imgs.size(0)
        _, preds = outputs.max(1)
        correct += (preds == targets).sum().item()
        total += imgs.size(0)
    return running_loss / total, correct / total


def save_training_history(history, arch: str):
    """Guarda historial CSV y una curva PNG simple para reporte académico."""
    if not history:
        return

    latest_csv = config.OUTPUT_DIR / "training_history.csv"
    arch_csv = config.OUTPUT_DIR / f"training_history_{arch}.csv"
    fieldnames = list(history[0].keys())
    for path in (latest_csv, arch_csv):
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(history)

    try:
        import matplotlib.pyplot as plt
    except Exception as exc:
        print(f"[warn] No se pudo importar matplotlib para curvas: {exc}")
        return

    xs = list(range(1, len(history) + 1))
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot(xs, [r["train_loss"] for r in history], label="train")
    axes[0].plot(xs, [r["val_loss"] for r in history], label="val")
    axes[0].set_title("Loss")
    axes[0].set_xlabel("Epoch")
    axes[0].legend()

    axes[1].plot(xs, [r["train_acc"] for r in history], label="train")
    axes[1].plot(xs, [r["val_acc"] for r in history], label="val")
    axes[1].set_title("Accuracy")
    axes[1].set_xlabel("Epoch")
    axes[1].legend()

    plt.tight_layout()
    for path in (
        config.OUTPUT_DIR / "learning_curves.png",
        config.OUTPUT_DIR / f"learning_curves_{arch}.png",
    ):
        fig.savefig(path, dpi=150)
    plt.close(fig)


def run_stage(stage_cfg, model, train_loader, val_loader, criterion, device, stage_name):
    if stage_cfg.get("freeze_backbone", False):
        freeze_backbone(model, model._arch_name)
    else:
        unfreeze_all(model)

    params = [p for p in model.parameters() if p.requires_grad]
    if stage_cfg["optimizer"] == "adam":
        optimizer = Adam(params, lr=stage_cfg["lr"])
    else:
        optimizer = AdamW(params, lr=stage_cfg["lr"], weight_decay=stage_cfg.get("weight_decay", 1e-4))

    base_lrs = [pg["lr"] for pg in optimizer.param_groups]

    # AMP (mixed precision) — usa GPU si está disponible
    scaler = torch.cuda.amp.GradScaler() if (getattr(config, "USE_AMP", False)
                                              and device.type == "cuda") else None
    accum_steps = max(1, getattr(config, "GRADIENT_ACCUM_STEPS", 1))

    best_val_acc = 0.0
    patience = stage_cfg.get("early_stopping_patience", 0)
    epochs_no_improve = 0
    history = []
    mixup_alpha = float(stage_cfg.get("mixup_alpha", 0.0) or 0.0)
    cutmix_alpha = float(stage_cfg.get("cutmix_alpha", 0.0) or 0.0)

    for epoch in range(1, stage_cfg["epochs"] + 1):
        t0 = time.time()
        lr = set_epoch_lr(optimizer, base_lrs, stage_cfg, epoch)
        train_loss, train_acc = train_one_epoch(
            model, train_loader, criterion, optimizer, device,
            scaler=scaler, accum_steps=accum_steps,
            mixup_alpha=mixup_alpha, cutmix_alpha=cutmix_alpha,
        )
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)
        duration = time.time() - t0
        print(f"[{stage_name}] epoch {epoch:03d}/{stage_cfg['epochs']}  "
              f"train_loss={train_loss:.4f} train_acc={train_acc:.4f}  "
              f"val_loss={val_loss:.4f} val_acc={val_acc:.4f}  "
              f"lr={lr:.2e}  ({duration:.1f}s)")
        history.append({
            "stage": stage_name,
            "epoch": epoch,
            "lr": lr,
            "train_loss": train_loss,
            "train_acc": train_acc,
            "val_loss": val_loss,
            "val_acc": val_acc,
            "duration_seconds": duration,
        })
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            checkpoint = model.state_dict()
            torch.save(checkpoint, config.CHECKPOINT_DIR / f"best_{stage_name}.pt")
            torch.save(
                checkpoint,
                config.CHECKPOINT_DIR / f"best_{stage_name}_{model._arch_name}.pt",
            )
            epochs_no_improve = 0
        else:
            epochs_no_improve += 1
            if patience and epochs_no_improve >= patience:
                print(f"[{stage_name}] early stopping at epoch {epoch}")
                break
    return best_val_acc, history


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--arch", default="resnet50",
                        choices=["resnet50", "efficientnet_b3", "mobilenet_v3_large", "convnext_tiny"])
    parser.add_argument("--skip-stage1", action="store_true")
    parser.add_argument("--smoke-test", action="store_true",
                        help="corre solo 1 epoch por etapa con batch chico para verificar que el pipeline funciona")
    args = parser.parse_args()

    set_seed()
    device = config.DEVICE
    print(f"Device: {device}")
    input_size = config.input_size_for_arch(args.arch)
    print(f"Input size: {input_size}x{input_size}")

    if args.smoke_test:
        # Reduce todo a un mínimo para probar end-to-end en pocos minutos
        config.STAGE1.update(epochs=1)
        config.STAGE2.update(epochs=1, early_stopping_patience=0)
        print("\n⚡ Smoke-test mode: 1 epoch por etapa, sólo verifica que el pipeline corre.\n")

    train_loader, val_loader, _ = build_dataloaders(input_size=input_size)
    weights = class_weights(train_loader).to(device)
    criterion = nn.CrossEntropyLoss(weight=weights, label_smoothing=config.STAGE2["label_smoothing"])

    model = build_model(args.arch).to(device)
    model._arch_name = args.arch
    print(f"Modelo {args.arch} | parámetros entrenables: {count_parameters(model):,}")

    full_history = []
    if not args.skip_stage1:
        _, stage1_history = run_stage(
            config.STAGE1, model, train_loader, val_loader,
            criterion, device, "stage1"
        )
        full_history.extend(stage1_history)
        # Recargar el mejor checkpoint de la etapa 1 antes de la 2
        model.load_state_dict(torch.load(config.CHECKPOINT_DIR / "best_stage1.pt"))

    final_acc, stage2_history = run_stage(
        config.STAGE2, model, train_loader, val_loader,
        criterion, device, "stage2"
    )
    full_history.extend(stage2_history)
    save_training_history(full_history, args.arch)
    print(f"\nMejor accuracy en validación (etapa 2): {final_acc:.4f}")
    print(f"Pesos guardados en: {config.CHECKPOINT_DIR / 'best_stage2.pt'}")
    print(f"Historial guardado en: {config.OUTPUT_DIR / f'training_history_{args.arch}.csv'}")


if __name__ == "__main__":
    main()
