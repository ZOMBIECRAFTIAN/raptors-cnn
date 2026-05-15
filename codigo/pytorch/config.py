"""
Configuración del proyecto — implementación PyTorch.

Centraliza las constantes del experimento. Modificar aquí evita tocar el resto
del código y mantiene la trazabilidad de los hiperparámetros.
"""
from pathlib import Path
import torch

# -----------------------------------------------------------------------------
# Paths del proyecto
# -----------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "datos"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
ANNOTATIONS_DIR = DATA_DIR / "annotations"
OUTPUT_DIR = PROJECT_ROOT / "codigo" / "pytorch" / "outputs"
CHECKPOINT_DIR = OUTPUT_DIR / "checkpoints"
LOGS_DIR = OUTPUT_DIR / "logs"

for d in (OUTPUT_DIR, CHECKPOINT_DIR, LOGS_DIR):
    d.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# Especies objetivo (23 — orden ALFABÉTICO por nombre científico, AOS 2023).
# IMPORTANTE: este orden DEBE coincidir con el orden alfabético de las
# carpetas en disco, porque torchvision.datasets.ImageFolder asigna los
# índices de clase ordenando alfabéticamente.
#
# Reclasificaciones AOS 2023 aplicadas:
#   Accipiter cooperii → Astur cooperii
#   Accipiter gentilis → Astur atricapillus  (split: nominal gentilis queda en Eurasia)
#   Buteo nitidus      → Buteo plagiatus     (split: nominal nitidus queda en Sudamérica)
# -----------------------------------------------------------------------------
SPECIES = [
    "Accipiter_striatus",       # 0  — SS  — Sharp-shinned Hawk      — Gavilán pecho rufo
    "Aquila_chrysaetos",        # 1  — GE  — Golden Eagle            — Águila real
    "Astur_atricapillus",       # 2  — NG  — Northern Goshawk        — Gavilán azor norteño (AOS 2023)
    "Astur_cooperii",           # 3  — CH  — Cooper's Hawk           — Gavilán de Cooper (AOS 2023)
    "Buteo_albonotatus",        # 4  — ZT  — Zone-tailed Hawk        — Aguililla aura
    "Buteo_brachyurus",         # 5  — STH — Short-tailed Hawk       — Aguililla colicorta
    "Buteo_jamaicensis",        # 6  — RT  — Red-tailed Hawk         — Aguililla cola roja
    "Buteo_lagopus",            # 7  — RL  — Rough-legged Hawk       — Aguililla patas ásperas
    "Buteo_lineatus",           # 8  — RS  — Red-shouldered Hawk     — Aguililla pecho rojo
    "Buteo_plagiatus",          # 9  — GH  — Gray Hawk               — Aguililla gris (AOS split)
    "Buteo_platypterus",        # 10 — BW  — Broad-winged Hawk       — Aguililla alas anchas
    "Buteo_regalis",            # 11 — FH  — Ferruginous Hawk        — Aguililla de Ferruginous
    "Buteo_swainsoni",          # 12 — SW  — Swainson's Hawk         — Aguililla de Swainson
    "Cathartes_aura",           # 13 — TV  — Turkey Vulture          — Zopilote aura
    "Chondrohierax_uncinatus",  # 14 — HK  — Hook-billed Kite        — Milano picogarfio
    "Circus_hudsonius",         # 15 — NH  — Northern Harrier        — Gavilán rastrero
    "Elanoides_forficatus",     # 16 — STK — Swallow-tailed Kite     — Milano tijereta
    "Falco_columbarius",        # 17 — ML  — Merlin                  — Halcón esmerejón
    "Falco_peregrinus",         # 18 — PG  — Peregrine Falcon        — Halcón peregrino
    "Falco_sparverius",         # 19 — AK  — American Kestrel        — Halcón cernícalo americano
    "Haliaeetus_leucocephalus", # 20 — BE  — Bald Eagle              — Águila calva
    "Ictinia_mississippiensis", # 21 — MK  — Mississippi Kite        — Milano de Mississippi
    "Pandion_haliaetus",        # 22 — OS  — Osprey                  — Águila pescadora
]
NUM_CLASSES = len(SPECIES)  # = 23

# Códigos de 2-3 letras alineados con el orden alfabético de SPECIES
SPECIES_CODE = [
    "SS",  "GE",  "NG",  "CH",  "ZT",  "STH", "RT",  "RL",
    "RS",  "GH",  "BW",  "FH",  "SW",  "TV",  "HK",  "NH",
    "STK", "ML",  "PG",  "AK",  "BE",  "MK",  "OS",
]
SPECIES_COMMON = [
    "Sharp-shinned Hawk",  "Golden Eagle",          "Northern Goshawk",  "Cooper's Hawk",
    "Zone-tailed Hawk",    "Short-tailed Hawk",     "Red-tailed Hawk",   "Rough-legged Hawk",
    "Red-shouldered Hawk", "Gray Hawk",             "Broad-winged Hawk", "Ferruginous Hawk",
    "Swainson's Hawk",     "Turkey Vulture",        "Hook-billed Kite",  "Northern Harrier",
    "Swallow-tailed Kite", "Merlin",                "Peregrine Falcon",  "American Kestrel",
    "Bald Eagle",          "Mississippi Kite",      "Osprey",
]
SPECIES_COMMON_ES = [
    "Gavilán pecho rufo",            "Águila real",              "Gavilán azor norteño",      "Gavilán de Cooper",
    "Aguililla aura",                "Aguililla colicorta",      "Aguililla cola roja",       "Aguililla patas ásperas",
    "Aguililla pecho rojo",          "Aguililla gris",           "Aguililla alas anchas",     "Aguililla de Ferruginous",
    "Aguililla de Swainson",         "Zopilote aura",            "Milano picogarfio",         "Gavilán rastrero",
    "Milano tijereta",               "Halcón esmerejón",         "Halcón peregrino",          "Halcón cernícalo americano",
    "Águila calva",                  "Milano de Mississippi",    "Águila pescadora",
]
# Verificación de consistencia (siempre debe pasar)
assert len(SPECIES) == len(SPECIES_CODE) == len(SPECIES_COMMON) == len(SPECIES_COMMON_ES) == 23

# -----------------------------------------------------------------------------
# Dispositivo
# -----------------------------------------------------------------------------
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -----------------------------------------------------------------------------
# Hiperparámetros — etapa 1 (feature extraction) y etapa 2 (fine-tuning)
# -----------------------------------------------------------------------------
INPUT_SIZE = 224  # cambia a 300 para EfficientNet-B3, 232 para ConvNeXt-Tiny
BATCH_SIZE = 16   # reducido de 32 → 16 para RTX 3050 4GB. Sube a 32 si tienes ≥ 8GB.

# Activar mixed precision (AMP) para reducir VRAM y acelerar. Recomendado en
# GPUs con Tensor Cores (RTX 20/30/40 series, A100, etc.). En CPU se ignora.
USE_AMP = True

# Acumulación de gradientes: simula un batch efectivo mayor sin más VRAM.
# Si BATCH_SIZE=16 y ACCUM_STEPS=2 → batch efectivo = 32.
GRADIENT_ACCUM_STEPS = 2

STAGE1 = dict(
    epochs=10,
    lr=1e-3,
    optimizer="adam",
    freeze_backbone=True,
    label_smoothing=0.0,
    mixup_alpha=0.0,
    cutmix_alpha=0.0,
)

STAGE2 = dict(
    epochs=60,
    lr=1e-4,
    optimizer="adamw",
    freeze_backbone=False,
    weight_decay=5e-4,
    label_smoothing=0.1,
    mixup_alpha=0.2,
    cutmix_alpha=1.0,
    scheduler="cosine",      # cosine annealing
    warmup_epochs=3,
    early_stopping_patience=10,
)

# Para GPUs muy limitadas: arquitectura recomendada con su batch_size sugerido
RECOMMENDED_BATCH = {
    "resnet50":           {"4GB": 16, "8GB": 32, "16GB": 64},
    "efficientnet_b3":    {"4GB": 8,  "8GB": 16, "16GB": 32},
    "mobilenet_v3_large": {"4GB": 32, "8GB": 64, "16GB": 128},
    "convnext_tiny":      {"4GB": 8,  "8GB": 16, "16GB": 32},
}

# -----------------------------------------------------------------------------
# Reproducibilidad
# -----------------------------------------------------------------------------
SEED = 42

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
USE_WANDB = False        # poner True cuando se configure W&B
WANDB_PROJECT = "raptors-veracruz-cnn"
