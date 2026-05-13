"""
Carga de datos para el entrenamiento — PyTorch.

Espera la siguiente estructura en datos/processed/:
    train/<especie>/imagen_*.jpg
    val/<especie>/imagen_*.jpg
    test/<especie>/imagen_*.jpg

Donde <especie> coincide con los nombres en config.SPECIES.
"""
from pathlib import Path
from typing import Tuple

import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

import config


def get_transforms(input_size: int = config.INPUT_SIZE):
    """Devuelve las transformaciones de train y eval.

    Train: augmentation rica (rotation, flip, color jitter, RandomResizedCrop).
    Eval: solo resize + center crop + normalización ImageNet.
    """
    imagenet_mean = [0.485, 0.456, 0.406]
    imagenet_std  = [0.229, 0.224, 0.225]

    train_tf = transforms.Compose([
        transforms.Resize(int(input_size * 1.15)),
        transforms.RandomResizedCrop(input_size, scale=(0.7, 1.0)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize(imagenet_mean, imagenet_std),
        transforms.RandomErasing(p=0.25, scale=(0.02, 0.15)),
    ])

    eval_tf = transforms.Compose([
        transforms.Resize(int(input_size * 1.15)),
        transforms.CenterCrop(input_size),
        transforms.ToTensor(),
        transforms.Normalize(imagenet_mean, imagenet_std),
    ])

    return train_tf, eval_tf


def build_dataloaders(
    processed_dir: Path = config.PROCESSED_DIR,
    batch_size: int = config.BATCH_SIZE,
    num_workers: int = 4,
) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """Construye los DataLoaders de train, val y test."""
    train_tf, eval_tf = get_transforms()

    train_ds = datasets.ImageFolder(processed_dir / "train", transform=train_tf)
    val_ds   = datasets.ImageFolder(processed_dir / "val",   transform=eval_tf)
    test_ds  = datasets.ImageFolder(processed_dir / "test",  transform=eval_tf)

    # Verificación de coherencia con config.SPECIES
    assert train_ds.classes == config.SPECIES, (
        f"Las clases en disco {train_ds.classes} no coinciden con config.SPECIES {config.SPECIES}"
    )

    pin = torch.cuda.is_available()
    common = dict(num_workers=num_workers, pin_memory=pin)

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, **common)
    val_loader   = DataLoader(val_ds,   batch_size=batch_size, shuffle=False, **common)
    test_loader  = DataLoader(test_ds,  batch_size=batch_size, shuffle=False, **common)

    return train_loader, val_loader, test_loader


def class_weights(train_loader: DataLoader) -> torch.Tensor:
    """Calcula pesos por clase para mitigar desbalance: w_i = N / (C * n_i)."""
    counts = torch.zeros(config.NUM_CLASSES)
    for _, target in train_loader.dataset.samples:
        counts[target] += 1
    total = counts.sum()
    weights = total / (config.NUM_CLASSES * counts.clamp(min=1.0))
    return weights
