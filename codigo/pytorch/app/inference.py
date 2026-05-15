"""
Motor de inferencia — carga modelo entrenado, predice especie sobre imagen,
y genera mapa Grad-CAM como verificación visual.

Diseñado para ser importado por main.py (Gradio). Mantiene el modelo en memoria.
"""
from __future__ import annotations
import io
from pathlib import Path
from typing import Optional

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Imports del proyecto (relativos a codigo/pytorch/)
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config
from model import build_model
from data_loader import get_transforms
from gradcam import GradCAM, get_target_layer

DEVICE = config.DEVICE
DEFAULT_CKPT = config.CHECKPOINT_DIR / "best_stage2.pt"
DEFAULT_ARCH = "resnet50"


class RaptorClassifier:
    """Wrapper de inferencia con modelo cargado en memoria."""

    def __init__(self, arch: str = DEFAULT_ARCH, weights: Optional[Path] = None):
        self.arch = arch
        self.weights_path = Path(weights) if weights else DEFAULT_CKPT
        self.model = None
        self.eval_tf = None
        self._loaded = False

    # --------------------------------------------------------------
    def load(self) -> tuple[bool, str]:
        """Carga el modelo. Devuelve (ok, mensaje)."""
        try:
            if not self.weights_path.exists():
                return False, f"No se encontró el checkpoint en {self.weights_path}. " \
                              "Entrena con `python train.py --arch {arch} --smoke-test` antes."

            self.model = build_model(self.arch).to(DEVICE)
            self.model._arch_name = self.arch
            state = torch.load(self.weights_path, map_location=DEVICE)
            self.model.load_state_dict(state)
            self.model.eval()
            _, self.eval_tf = get_transforms()
            self._loaded = True
            return True, f"Modelo {self.arch} cargado en {DEVICE} ({self.weights_path.name})."
        except Exception as e:
            return False, f"Error cargando modelo: {e}"

    @property
    def loaded(self) -> bool:
        return self._loaded

    # --------------------------------------------------------------
    @torch.no_grad()
    def predict(self, pil_image: Image.Image, top_k: int = 5) -> dict:
        """Devuelve el top-k de predicciones para una imagen."""
        if not self._loaded:
            ok, msg = self.load()
            if not ok:
                return {"error": msg}

        x = self.eval_tf(pil_image.convert("RGB")).unsqueeze(0).to(DEVICE)
        logits = self.model(x)
        probs = F.softmax(logits, dim=1).cpu().numpy()[0]
        topk_idx = probs.argsort()[::-1][:top_k]
        return {
            "top1_idx": int(topk_idx[0]),
            "top1_species": config.SPECIES[topk_idx[0]],
            "top1_code": config.SPECIES_CODE[topk_idx[0]],
            "top1_common": config.SPECIES_COMMON[topk_idx[0]],
            "top1_prob": float(probs[topk_idx[0]]),
            "topk": [
                {
                    "species": config.SPECIES[i],
                    "code": config.SPECIES_CODE[i],
                    "common": config.SPECIES_COMMON[i],
                    "prob": float(probs[i]),
                }
                for i in topk_idx
            ],
            "all_probs": probs.tolist(),
        }

    # --------------------------------------------------------------
    def gradcam(self, pil_image: Image.Image, target_idx: Optional[int] = None) -> Image.Image:
        """Genera un PIL.Image con el mapa Grad-CAM superpuesto."""
        if not self._loaded:
            self.load()

        x = self.eval_tf(pil_image.convert("RGB")).unsqueeze(0).to(DEVICE)
        cam_engine = GradCAM(self.model, get_target_layer(self.model, self.arch))
        cam, pred = cam_engine(x, class_idx=torch.tensor([target_idx], device=DEVICE)
                                if target_idx is not None else None)

        img_resized = pil_image.convert("RGB").resize((config.INPUT_SIZE, config.INPUT_SIZE))
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(img_resized)
        ax.imshow(cam, cmap="jet", alpha=0.5)
        ax.axis("off")
        ax.set_title(f"Grad-CAM — {config.SPECIES_COMMON[pred]} ({config.SPECIES_CODE[pred]})",
                     fontsize=12)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=100, bbox_inches="tight")
        plt.close(fig)
        buf.seek(0)
        return Image.open(buf)


# Singleton del clasificador (un solo modelo en memoria por proceso)
_classifier = None


def get_classifier(arch: str = DEFAULT_ARCH, weights: Optional[Path] = None) -> RaptorClassifier:
    """Devuelve la instancia singleton del clasificador."""
    global _classifier
    if _classifier is None:
        _classifier = RaptorClassifier(arch=arch, weights=weights)
        _classifier.load()
    return _classifier
