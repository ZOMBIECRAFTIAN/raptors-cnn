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
# Especies objetivo (14 — orden ALFABÉTICO por nombre científico).
# IMPORTANTE: este orden DEBE coincidir con el orden alfabético de las
# carpetas en disco, porque torchvision.datasets.ImageFolder asigna los
# índices de clase ordenando alfabéticamente. Cualquier otro orden romper
# la correspondencia entre etiqueta predicha y especie real.
# -----------------------------------------------------------------------------
SPECIES = [
    "Accipiter_striatus",       # 0 — SS — Sharp-shinned Hawk
    "Astur_cooperii",           # 1 — CH — Cooper's Hawk (reclasificado de Accipiter por AOS 2023)
    "Buteo_albonotatus",        # 2 — ZT — Zone-tailed Hawk
    "Buteo_jamaicensis",        # 3 — RT — Red-tailed Hawk
    "Buteo_lineatus",           # 4 — RS — Red-shouldered Hawk
    "Buteo_platypterus",        # 5 — BW — Broad-winged Hawk
    "Buteo_swainsoni",          # 6 — SW — Swainson's Hawk
    "Cathartes_aura",           # 7 — TV — Turkey Vulture
    "Circus_hudsonius",         # 8 — NH — Northern Harrier
    "Falco_columbarius",        # 9 — ML — Merlin
    "Falco_peregrinus",         # 10 — PG — Peregrine Falcon
    "Falco_sparverius",         # 11 — AK — American Kestrel
    "Ictinia_mississippiensis", # 12 — MK — Mississippi Kite
    "Pandion_haliaetus",        # 13 — OS — Osprey
]
NUM_CLASSES = len(SPECIES)

# Códigos de dos letras alineados con el orden alfabético de SPECIES
SPECIES_CODE = ["SS", "CH", "ZT", "RT", "RS", "BW", "SW", "TV", "NH", "ML", "PG", "AK", "MK", "OS"]
SPECIES_COMMON = [
    "Sharp-shinned Hawk", "Cooper's Hawk", "Zone-tailed Hawk", "Red-tailed Hawk",
    "Red-shouldered Hawk", "Broad-winged Hawk", "Swainson's Hawk", "Turkey Vulture",
    "Northern Harrier", "Merlin", "Peregrine Falcon", "American Kestrel",
    "Mississippi Kite", "Osprey",
]

# -----------------------------------------------------------------------------
# Dispositivo
# -----------------------------------------------------------------------------
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -----------------------------------------------------------------------------
# Hiperparámetros — etapa 1 (feature extraction) y etapa 2 (fine-tuning)
# -----------------------------------------------------------------------------
INPUT_SIZE = 224  # cambia a 300 para EfficientNet-B3, 232 para ConvNeXt-Tiny
BATCH_SIZE = 32

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

# -----------------------------------------------------------------------------
# Reproducibilidad
# -----------------------------------------------------------------------------
SEED = 42

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
USE_WANDB = False        # poner True cuando se configure W&B
WANDB_PROJECT = "raptors-veracruz-cnn"
