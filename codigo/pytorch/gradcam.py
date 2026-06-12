"""
Explicabilidad con Grad-CAM — PyTorch.

Genera mapas de calor sobre imágenes de prueba para verificar que el modelo
atiende a los caracteres morfológicos correctos (silueta de ala, cola, etc.).

Uso:
    python gradcam.py --image path/a/imagen.jpg --weights outputs/checkpoints/best_stage2.pt
"""
import argparse
from pathlib import Path

import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

import config
from model import build_model
from data_loader import get_transforms


class GradCAM:
    """Implementación mínima de Grad-CAM para una capa target dada."""
    def __init__(self, model, target_layer):
        self.model = model.eval()
        self.activations = None
        self.gradients = None
        target_layer.register_forward_hook(self._save_activation)
        target_layer.register_full_backward_hook(self._save_gradient)

    def _save_activation(self, module, inp, out): self.activations = out.detach()
    def _save_gradient(self, module, grad_in, grad_out): self.gradients = grad_out[0].detach()

    def __call__(self, x, class_idx=None):
        logits = self.model(x)
        if class_idx is None: class_idx = logits.argmax(dim=1)
        score = logits[0, class_idx]
        self.model.zero_grad()
        score.backward()

        weights = self.gradients.mean(dim=(2, 3), keepdim=True)
        cam = F.relu((weights * self.activations).sum(dim=1, keepdim=True))
        cam = F.interpolate(cam, size=x.shape[-2:], mode="bilinear", align_corners=False)
        cam = cam.squeeze().cpu().numpy()
        cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)
        return cam, class_idx.item()


def get_target_layer(model, arch):
    """Última capa convolucional de cada arquitectura."""
    if arch == "resnet50": return model.layer4[-1]
    if arch == "efficientnet_b3": return model.features[-1]
    if arch == "mobilenet_v3_large": return model.features[-1]
    if arch == "convnext_tiny": return model.features[-1]
    raise ValueError(f"arch desconocida: {arch}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True)
    parser.add_argument("--arch", default="resnet50")
    parser.add_argument("--weights", required=True)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    device = config.DEVICE
    model = build_model(args.arch, pretrained=False).to(device)
    model.load_state_dict(torch.load(args.weights, map_location=device))

    input_size = config.input_size_for_arch(args.arch)
    _, eval_tf = get_transforms(input_size)
    img = Image.open(args.image).convert("RGB")
    x = eval_tf(img).unsqueeze(0).to(device)

    cam_engine = GradCAM(model, get_target_layer(model, args.arch))
    cam, pred = cam_engine(x)

    img_resized = img.resize((input_size, input_size))
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    ax[0].imshow(img_resized); ax[0].set_title("Original"); ax[0].axis("off")
    ax[1].imshow(img_resized); ax[1].imshow(cam, cmap="jet", alpha=0.5)
    ax[1].set_title(f"Grad-CAM — {config.SPECIES[pred]}"); ax[1].axis("off")
    out_path = args.out or (config.OUTPUT_DIR / f"gradcam_{Path(args.image).stem}.png")
    plt.tight_layout(); plt.savefig(out_path, dpi=150); plt.close(fig)
    print(f"Guardado en {out_path}")


if __name__ == "__main__":
    main()
