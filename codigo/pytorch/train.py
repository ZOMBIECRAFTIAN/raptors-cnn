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
import random
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torch.optim import Adam, AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR

import config
from data_loader import build_dataloaders, class_weights
from model import build_model, freeze_backbone, unfreeze_all, count_parameters


def set_seed(seed: int = config.SEED) -> None:
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def train_one_epoch(model, loader, criterion, optimizer, device):
    model.train()
    running_loss, correct, total = 0.0, 0, 0
    for imgs, targets in loader:
        imgs, targets = imgs.to(device), targets.to(device)
        optimizer.zero_grad(set_to_none=True)
        outputs = model(imgs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * imgs.size(0)
        _, preds = outputs.max(1)
        correct += (preds == targets).sum().item()
        total += imgs.size(0)
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

    scheduler = None
    if stage_cfg.get("scheduler") == "cosine":
        scheduler = CosineAnnealingLR(optimizer, T_max=stage_cfg["epochs"])

    best_val_acc = 0.0
    patience = stage_cfg.get("early_stopping_patience", 0)
    epochs_no_improve = 0

    for epoch in range(1, stage_cfg["epochs"] + 1):
        t0 = time.time()
        train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)
        if scheduler is not None: scheduler.step()
        print(f"[{stage_name}] epoch {epoch:03d}/{stage_cfg['epochs']}  "
              f"train_loss={train_loss:.4f} train_acc={train_acc:.4f}  "
              f"val_loss={val_loss:.4f} val_acc={val_acc:.4f}  "
              f"({time.time()-t0:.1f}s)")
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), config.CHECKPOINT_DIR / f"best_{stage_name}.pt")
            epochs_no_improve = 0
        else:
            epochs_no_improve += 1
            if patience and epochs_no_improve >= patience:
                print(f"[{stage_name}] early stopping at epoch {epoch}")
                break
    return best_val_acc


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

    if args.smoke_test:
        # Reduce todo a un mínimo para probar end-to-end en pocos minutos
        config.STAGE1.update(epochs=1)
        config.STAGE2.update(epochs=1, early_stopping_patience=0)
        print("\n⚡ Smoke-test mode: 1 epoch por etapa, sólo verifica que el pipeline corre.\n")

    train_loader, val_loader, _ = build_dataloaders()
    weights = class_weights(train_loader).to(device)
    criterion = nn.CrossEntropyLoss(weight=weights, label_smoothing=config.STAGE2["label_smoothing"])

    model = build_model(args.arch).to(device)
    model._arch_name = args.arch
    print(f"Modelo {args.arch} | parámetros entrenables: {count_parameters(model):,}")

    if not args.skip_stage1:
        run_stage(config.STAGE1, model, train_loader, val_loader, criterion, device, "stage1")
        # Recargar el mejor checkpoint de la etapa 1 antes de la 2
        model.load_state_dict(torch.load(config.CHECKPOINT_DIR / "best_stage1.pt"))

    final_acc = run_stage(config.STAGE2, model, train_loader, val_loader, criterion, device, "stage2")
    print(f"\nMejor accuracy en validación (etapa 2): {final_acc:.4f}")
    print(f"Pesos guardados en: {config.CHECKPOINT_DIR / 'best_stage2.pt'}")


if __name__ == "__main__":
    main()
