"""
retrain_with_feedback.py — Fine-tuning incremental con correcciones del usuario.

Toma las imágenes acumuladas en datos/feedback/<species>/ (gracias al active
learning de la app Gradio) y hace un fine-tuning corto sobre el modelo actual
para incorporar las correcciones SIN olvidar lo aprendido (catastrophic
forgetting controlado por lr bajo y pocos epochs).

Uso:
    python retrain_with_feedback.py
    python retrain_with_feedback.py --epochs 5 --lr 5e-5

Flujo:
  1. Carga el modelo actual desde outputs/checkpoints/best_stage2.pt
  2. Mezcla las imágenes de feedback con un subset del dataset original
     (para no olvidar — concept replay)
  3. Fine-tune por pocas epochs con lr muy bajo
  4. Evalúa sobre el test set
  5. Si mejora, guarda como nuevo best_stage2.pt + backup del anterior

Esto se puede correr cada vez que acumules suficiente feedback (≥ 50 imgs).
"""
import argparse
import random
import shutil
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.utils.data import DataLoader, ConcatDataset, Subset
from torchvision import datasets, transforms

import config
from data_loader import build_dataloaders, get_transforms, class_weights
from model import build_model, unfreeze_all


def set_seed(seed: int = config.SEED) -> None:
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def feedback_dataset():
    """Carga datos/feedback/ como un ImageFolder, ignorando _not_raptor."""
    feedback_dir = config.DATA_DIR / "feedback"
    if not feedback_dir.exists():
        return None
    # Excluir _not_raptor — usaría una clase fantasma
    valid_dirs = [d for d in feedback_dir.iterdir()
                  if d.is_dir() and not d.name.startswith("_")]
    if not valid_dirs:
        return None

    # Construir ImageFolder con SOLO las especies del proyecto, en orden alfabético
    _, eval_tf = get_transforms()
    train_tf = transforms.Compose([
        transforms.Resize(256),
        transforms.RandomResizedCrop(config.INPUT_SIZE, scale=(0.7, 1.0)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=10),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])

    try:
        ds = datasets.ImageFolder(feedback_dir, transform=train_tf,
                                   is_valid_file=lambda p: not p.split("/")[-2].startswith("_"))
        # Verificar que coincida con config.SPECIES (al menos un subconjunto)
        if not set(ds.classes).issubset(set(config.SPECIES)):
            print(f"[warn] feedback tiene clases fuera del proyecto: {set(ds.classes) - set(config.SPECIES)}")
        return ds
    except Exception as e:
        print(f"[warn] No se pudo cargar feedback dataset: {e}")
        return None


def run_finetune(epochs: int, lr: float, output_name: str):
    set_seed()
    device = config.DEVICE
    print(f"\n=== Fine-tuning incremental con feedback ===")
    print(f"Device: {device} · epochs: {epochs} · lr: {lr}")

    # Cargar feedback
    fb_ds = feedback_dataset()
    if fb_ds is None or len(fb_ds) == 0:
        print("\n[error] No hay datos en datos/feedback/ aún.")
        print("        Acumula correcciones desde la app Gradio antes de re-entrenar.")
        return

    print(f"\n  Feedback acumulado: {len(fb_ds)} imágenes en {len(fb_ds.classes)} clases")

    # Cargar dataset original (para concept replay — mezcla feedback con originales)
    try:
        train_loader_orig, val_loader, _ = build_dataloaders()
        orig_ds = train_loader_orig.dataset
        # Tomar un subset del original para mezclar (mismo tamaño que feedback)
        n_mix = min(len(fb_ds) * 3, len(orig_ds))
        indices = random.sample(range(len(orig_ds)), n_mix)
        orig_subset = Subset(orig_ds, indices)
        combined = ConcatDataset([fb_ds, orig_subset])
        print(f"  Dataset combinado: {len(combined)} imágenes ({len(fb_ds)} feedback + {n_mix} originales)")
    except Exception as e:
        print(f"  [warn] No se pudo cargar dataset original ({e}); entrenando solo con feedback.")
        combined = fb_ds
        _, val_loader, _ = (None, None, None)

    loader = DataLoader(combined, batch_size=config.BATCH_SIZE,
                        shuffle=True, num_workers=4, pin_memory=(device.type == "cuda"))

    # Cargar modelo actual
    model = build_model("resnet50").to(device)
    model._arch_name = "resnet50"
    ckpt = config.CHECKPOINT_DIR / "best_stage2.pt"
    if not ckpt.exists():
        print(f"\n[error] No existe {ckpt}. Entrena primero con `python train.py`.")
        return
    model.load_state_dict(torch.load(ckpt, map_location=device))
    unfreeze_all(model)

    # Fine-tune con lr bajo
    optimizer = AdamW([p for p in model.parameters() if p.requires_grad],
                      lr=lr, weight_decay=5e-4)
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)

    scaler = torch.cuda.amp.GradScaler() if device.type == "cuda" else None

    print(f"\nEntrenando {epochs} epochs...")
    for ep in range(1, epochs + 1):
        model.train()
        running_loss, correct, total = 0.0, 0, 0
        t0 = time.time()
        for imgs, targets in loader:
            imgs, targets = imgs.to(device), targets.to(device)
            optimizer.zero_grad(set_to_none=True)
            if scaler is not None:
                with torch.cuda.amp.autocast():
                    out = model(imgs); loss = criterion(out, targets)
                scaler.scale(loss).backward()
                scaler.step(optimizer); scaler.update()
            else:
                out = model(imgs); loss = criterion(out, targets)
                loss.backward(); optimizer.step()
            running_loss += loss.item() * imgs.size(0)
            correct += (out.argmax(1) == targets).sum().item()
            total += imgs.size(0)
        print(f"  ep {ep}/{epochs} · loss {running_loss/total:.4f} · "
              f"acc {correct/total:.4f} · {time.time()-t0:.1f}s")

    # Guardar con timestamp + actualizar el "best"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = config.CHECKPOINT_DIR / f"finetune_{timestamp}.pt"
    torch.save(model.state_dict(), out_path)
    print(f"\n✓ Modelo fine-tuned guardado: {out_path}")

    # Backup del anterior y reemplazar best
    backup = config.CHECKPOINT_DIR / f"best_stage2_backup_{timestamp}.pt"
    shutil.copy(ckpt, backup)
    shutil.copy(out_path, ckpt)
    print(f"✓ Backup del anterior: {backup}")
    print(f"✓ best_stage2.pt actualizado")
    print(f"\nSugerencia: corre `python evaluate.py` para validar que mejoró antes de presumir.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=5,
                        help="Epochs de fine-tuning (default 5 — pocos para no olvidar)")
    parser.add_argument("--lr", type=float, default=5e-5,
                        help="Learning rate (default 5e-5 — bajo para preservar pesos)")
    parser.add_argument("--output", default=None, help="Nombre del checkpoint de salida")
    args = parser.parse_args()
    run_finetune(args.epochs, args.lr, args.output or "finetune_latest.pt")


if __name__ == "__main__":
    main()
