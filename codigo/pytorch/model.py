"""
Definición de los modelos — PyTorch.

Soporta cuatro arquitecturas con transfer learning desde ImageNet:
    - resnet50
    - efficientnet_b3
    - mobilenet_v3_large
    - convnext_tiny

Cada modelo es construido con la cabeza clasificadora ajustada al número de clases
del proyecto (config.NUM_CLASSES = 53).
"""
import torch
import torch.nn as nn
from torchvision import models

import config


def build_model(arch: str = "resnet50", pretrained: bool = True) -> nn.Module:
    """Construye uno de los modelos soportados, listo para entrenamiento."""
    arch = arch.lower()

    if arch == "resnet50":
        weights = models.ResNet50_Weights.IMAGENET1K_V2 if pretrained else None
        m = models.resnet50(weights=weights)
        in_features = m.fc.in_features
        m.fc = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(in_features, config.NUM_CLASSES),
        )

    elif arch == "efficientnet_b3":
        weights = models.EfficientNet_B3_Weights.IMAGENET1K_V1 if pretrained else None
        m = models.efficientnet_b3(weights=weights)
        in_features = m.classifier[1].in_features
        m.classifier = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(in_features, config.NUM_CLASSES),
        )

    elif arch == "mobilenet_v3_large":
        weights = models.MobileNet_V3_Large_Weights.IMAGENET1K_V2 if pretrained else None
        m = models.mobilenet_v3_large(weights=weights)
        in_features = m.classifier[-1].in_features
        m.classifier[-1] = nn.Linear(in_features, config.NUM_CLASSES)

    elif arch == "convnext_tiny":
        weights = models.ConvNeXt_Tiny_Weights.IMAGENET1K_V1 if pretrained else None
        m = models.convnext_tiny(weights=weights)
        in_features = m.classifier[-1].in_features
        m.classifier[-1] = nn.Linear(in_features, config.NUM_CLASSES)

    else:
        raise ValueError(f"Arquitectura desconocida: {arch}")

    return m


def freeze_backbone(model: nn.Module, arch: str) -> None:
    """Congela todas las capas excepto la cabeza clasificadora."""
    for param in model.parameters():
        param.requires_grad = False

    arch = arch.lower()
    if arch == "resnet50":
        for param in model.fc.parameters(): param.requires_grad = True
    elif arch == "efficientnet_b3":
        for param in model.classifier.parameters(): param.requires_grad = True
    elif arch == "mobilenet_v3_large":
        for param in model.classifier.parameters(): param.requires_grad = True
    elif arch == "convnext_tiny":
        for param in model.classifier.parameters(): param.requires_grad = True


def unfreeze_all(model: nn.Module) -> None:
    """Libera todas las capas para fine-tuning."""
    for param in model.parameters():
        param.requires_grad = True


def count_parameters(model: nn.Module) -> int:
    """Número de parámetros entrenables."""
    return sum(p.numel() for p in model.parameters() if p.requires_grad)
