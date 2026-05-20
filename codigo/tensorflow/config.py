"""
Configuración del proyecto — implementación TensorFlow / Keras.

Espejo del config.py de PyTorch para garantizar paridad experimental.
Alcance V1.1 (mayo 2026): TODAS las rapaces diurnas de México — 53 especies.
Ver `documentacion/LISTA_OFICIAL_RAPACES_MEXICO.md`.
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
# Especies (53 — TODAS las rapaces diurnas de México, orden ALFABÉTICO).
# Coincide con tf.keras.utils.image_dataset_from_directory que ordena por nombre.
# Reclasificaciones AOS 2023: Astur cooperii, Astur atricapillus, Buteo plagiatus.
# Fuente: documentacion/LISTA_OFICIAL_RAPACES_MEXICO.md
# -----------------------------------------------------------------------------
SPECIES = [
    "Accipiter_striatus", "Aquila_chrysaetos", "Astur_atricapillus", "Astur_cooperii",
    "Busarellus_nigricollis", "Buteo_albonotatus", "Buteo_brachyurus", "Buteo_jamaicensis",
    "Buteo_lagopus", "Buteo_lineatus", "Buteo_plagiatus", "Buteo_platypterus",
    "Buteo_regalis", "Buteo_swainsoni", "Buteogallus_anthracinus", "Buteogallus_solitarius",
    "Buteogallus_urubitinga", "Caracara_plancus", "Cathartes_aura", "Cathartes_burrovianus",
    "Chondrohierax_uncinatus", "Circus_hudsonius", "Coragyps_atratus", "Daptrius_americanus",
    "Elanoides_forficatus", "Elanus_leucurus", "Falco_columbarius", "Falco_deiroleucus",
    "Falco_femoralis", "Falco_peregrinus", "Falco_rufigularis", "Falco_sparverius",
    "Geranoaetus_albicaudatus", "Geranospiza_caerulescens", "Haliaeetus_leucocephalus",
    "Harpagus_bidentatus", "Harpia_harpyja", "Herpetotheres_cachinnans",
    "Ictinia_mississippiensis", "Ictinia_plumbea", "Leptodon_cayanensis",
    "Micrastur_ruficollis", "Micrastur_semitorquatus", "Morphnus_guianensis",
    "Pandion_haliaetus", "Parabuteo_unicinctus", "Pseudastur_albicollis",
    "Rostrhamus_sociabilis", "Rupornis_magnirostris", "Sarcoramphus_papa",
    "Spizaetus_melanoleucus", "Spizaetus_ornatus", "Spizaetus_tyrannus",
]
NUM_CLASSES = len(SPECIES)  # = 53

SPECIES_CODE = [
    "SSHA", "GOEA", "NOGO", "COHA", "BCHA", "ZTHA", "STHA", "RTHA",
    "RLHA", "RSHA", "GRHA", "BWHA", "FEHA", "SWHA", "COBH", "SOEA",
    "GBHA", "CRCA", "TUVU", "LYHV", "HBKI", "NOHA", "BLVU", "RTCA",
    "STKI", "WTKI", "MERL", "OBFA", "APFA", "PEFA", "BAFA", "AMKE",
    "WTHA", "CRHA", "BAEA", "DTKI", "HAEA", "LAFA", "MIKI", "PLKI",
    "GHKI", "BFFA", "CFFA", "CREA", "OSPR", "HASH", "WHHA", "SNKI",
    "ROHA", "KIVU", "BAWE", "ORHE", "BLHE",
]

SPECIES_COMMON = [
    "Sharp-shinned Hawk",         "Golden Eagle",                "American Goshawk",            "Cooper's Hawk",
    "Black-collared Hawk",        "Zone-tailed Hawk",            "Short-tailed Hawk",           "Red-tailed Hawk",
    "Rough-legged Hawk",          "Red-shouldered Hawk",         "Gray Hawk",                   "Broad-winged Hawk",
    "Ferruginous Hawk",           "Swainson's Hawk",             "Common Black Hawk",           "Solitary Eagle",
    "Great Black Hawk",           "Crested Caracara",            "Turkey Vulture",              "Lesser Yellow-headed Vulture",
    "Hook-billed Kite",           "Northern Harrier",            "Black Vulture",               "Red-throated Caracara",
    "Swallow-tailed Kite",        "White-tailed Kite",           "Merlin",                      "Orange-breasted Falcon",
    "Aplomado Falcon",            "Peregrine Falcon",            "Bat Falcon",                  "American Kestrel",
    "White-tailed Hawk",          "Crane Hawk",                  "Bald Eagle",                  "Double-toothed Kite",
    "Harpy Eagle",                "Laughing Falcon",             "Mississippi Kite",            "Plumbeous Kite",
    "Gray-headed Kite",           "Barred Forest-Falcon",        "Collared Forest-Falcon",      "Crested Eagle",
    "Osprey",                     "Harris's Hawk",               "White Hawk",                  "Snail Kite",
    "Roadside Hawk",              "King Vulture",                "Black-and-white Hawk-Eagle",  "Ornate Hawk-Eagle",
    "Black Hawk-Eagle",
]

SPECIES_COMMON_ES = [
    "Gavilán pajarero",           "Águila real",                 "Gavilán azor americano",      "Gavilán de Cooper",
    "Aguililla canela",           "Aguililla aura",              "Aguililla cola corta",        "Aguililla cola roja",
    "Aguililla ártica",           "Aguililla pecho rojo",        "Aguililla gris",              "Aguililla ala ancha",
    "Aguililla real",             "Aguililla de Swainson",       "Aguililla negra menor",       "Águila solitaria",
    "Aguililla negra mayor",      "Caracara quebrantahuesos",    "Zopilote aura",               "Zopilote sabanero",
    "Gavilán pico de gancho",     "Aguilucho norteño",           "Zopilote común",              "Caracara comecacao",
    "Milano tijereta",            "Milano coliblanco",           "Esmerejón",                   "Halcón pechirrufo",
    "Halcón fajado",              "Halcón peregrino",            "Halcón murcielaguero",        "Cernícalo americano",
    "Aguililla cola blanca",      "Gavilán zancón",              "Águila calva",                "Gavilán bidentado",
    "Águila arpía",               "Halcón guaco",                "Milano de Mississippi",       "Milano plomizo",
    "Milano cabecigris",          "Halcón selvático barrado",    "Halcón selvático de collar",  "Águila monera",
    "Águila pescadora",           "Aguililla rojinegra",         "Aguililla blanca",            "Caracolero común",
    "Aguililla caminera",         "Zopilote rey",                "Águila blanquinegra",         "Águila elegante",
    "Águila tirana",
]

SPECIES_FAMILY = [
    "Accipitridae", "Accipitridae", "Accipitridae", "Accipitridae",
    "Accipitridae", "Accipitridae", "Accipitridae", "Accipitridae",
    "Accipitridae", "Accipitridae", "Accipitridae", "Accipitridae",
    "Accipitridae", "Accipitridae", "Accipitridae", "Accipitridae",
    "Accipitridae", "Falconidae",   "Cathartidae",  "Cathartidae",
    "Accipitridae", "Accipitridae", "Cathartidae",  "Falconidae",
    "Accipitridae", "Accipitridae", "Falconidae",   "Falconidae",
    "Falconidae",   "Falconidae",   "Falconidae",   "Falconidae",
    "Accipitridae", "Accipitridae", "Accipitridae", "Accipitridae",
    "Accipitridae", "Falconidae",   "Accipitridae", "Accipitridae",
    "Accipitridae", "Falconidae",   "Falconidae",   "Accipitridae",
    "Pandionidae",  "Accipitridae", "Accipitridae", "Accipitridae",
    "Accipitridae", "Cathartidae",  "Accipitridae", "Accipitridae",
    "Accipitridae",
]

assert len(SPECIES) == len(SPECIES_CODE) == len(SPECIES_COMMON) \
    == len(SPECIES_COMMON_ES) == len(SPECIES_FAMILY) == 53
assert SPECIES == sorted(SPECIES), "SPECIES debe estar ordenado alfabéticamente."

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
    epochs=80, lr=1e-4, freeze_backbone=False,
    weight_decay=5e-4, label_smoothing=0.1,
    early_stopping_patience=15,
)

USE_CLASS_WEIGHTS = True

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
USE_WANDB = False
WANDB_PROJECT = "raptors-mexico-cnn-tf"
