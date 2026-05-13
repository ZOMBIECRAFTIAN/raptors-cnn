"""
Configuración del proyecto — implementación TensorFlow / Keras.

Espejo del config.py de PyTorch para garantizar paridad experimental.
"""
from pathlib import Path
import tensorflow as tf

# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "datos"
PROCESSED_DIR = DATA_DIR / "processed"
ANNOTATIONS_DIR = DATA_DIR / "annotations"
OUTPUT_DIR = PROJECT_ROOT / "codigo" / "tensorflow" / "outputs"
CHECKPOINT_DIR = OUTPUT_DIR / "checkpoints"
LOGS_DIR = OUTPUT_DIR / "logs"
for d in (OUTPUT_DIR, CHECKPOINT_DIR, LOGS_DIR):
    d.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# Especies (14 — orden ALFABÉTICO; coincide con tf.keras.utils.image_dataset_from_directory
# y con el orden alfabético de las carpetas en disco)
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

SPECIES_CODE = ["SS", "CH", "ZT", "RT", "RS", "BW", "SW", "TV", "NH", "ML", "PG", "AK", "MK", "OS"]
SPECIES_COMMON = [
    "Sharp-shinned Hawk", "Cooper's Hawk", "Zone-tailed Hawk", "Red-tailed Hawk",
    "Red-shouldered Hawk", "Broad-winged Hawk", "Swainson's Hawk", "Turkey Vulture",
    "Northern Harrier", "Merlin", "Peregrine Falcon", "American Kestrel",
    "Mississippi Kite", "Osprey",
]

# -----------------------------------------------------------------------------
# GPUs y reproducibilidad
# -----------------------------------------------------------------------------
gpus = tf.config.list_physical_devices("GPU")
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

SEED = 42

# -----------------------------------------------------------------------------
# Hiperparámetros
# -----------------------------------------------------------------------------
INPUT_SIZE = 224
BATCH_SIZE = 32

STAGE1 = dict(epochs=10, lr=1e-3, freeze_backbone=True, label_smoothing=0.0)
STAGE2 = dict(
    epochs=60, lr=1e-4, freeze_backbone=False,
    weight_decay=5e-4, label_smoothing=0.1,
    early_stopping_patience=10,
)
