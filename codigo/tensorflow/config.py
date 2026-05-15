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
# Especies (23 — orden ALFABÉTICO; coincide con tf.keras.utils.image_dataset_from_directory.
# Reclasificaciones AOS 2023: Astur cooperii, Astur atricapillus, Buteo plagiatus.
# -----------------------------------------------------------------------------
SPECIES = [
    "Accipiter_striatus", "Aquila_chrysaetos", "Astur_atricapillus", "Astur_cooperii",
    "Buteo_albonotatus", "Buteo_brachyurus", "Buteo_jamaicensis", "Buteo_lagopus",
    "Buteo_lineatus", "Buteo_plagiatus", "Buteo_platypterus", "Buteo_regalis",
    "Buteo_swainsoni", "Cathartes_aura", "Chondrohierax_uncinatus", "Circus_hudsonius",
    "Elanoides_forficatus", "Falco_columbarius", "Falco_peregrinus", "Falco_sparverius",
    "Haliaeetus_leucocephalus", "Ictinia_mississippiensis", "Pandion_haliaetus",
]
NUM_CLASSES = len(SPECIES)  # = 23

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
assert len(SPECIES) == len(SPECIES_CODE) == len(SPECIES_COMMON) == len(SPECIES_COMMON_ES) == 23

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
