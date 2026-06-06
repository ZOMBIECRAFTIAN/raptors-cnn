"""
Configuración del proyecto — implementación PyTorch.

Proyecto: Sistema de Identificación de Aves Rapaces por Silueta y
Comportamiento de Vuelo Utilizando IA y Diseño de Lenguaje de Señas
para su Comunicación y Reconocimiento (raptors-cnn).

Centraliza las constantes del experimento. Modificar aquí evita tocar el resto
del código y mantiene la trazabilidad de los hiperparámetros.

Alcance (V1.1, mayo 2026): TODAS las rapaces diurnas de México — 53 especies.
Sustituye al alcance V1 (23 rapaces del corredor de Veracruz).
Ver `documentacion/LISTA_OFICIAL_RAPACES_MEXICO.md` para la justificación
taxonómica completa.
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
# Especies objetivo (53 — TODAS las rapaces diurnas de México).
# Orden ALFABÉTICO por nombre científico (AOS 2024).
# IMPORTANTE: este orden DEBE coincidir con el orden alfabético de las
# carpetas en disco, porque torchvision.datasets.ImageFolder asigna los
# índices de clase ordenando alfabéticamente.
#
# Reclasificaciones AOS 2023 aplicadas:
#   Accipiter cooperii → Astur cooperii
#   Accipiter gentilis → Astur atricapillus  (split: nominal gentilis queda en Eurasia)
#   Buteo nitidus      → Buteo plagiatus     (split: nominal nitidus queda en Sudamérica)
#
# Fuente: documentacion/LISTA_OFICIAL_RAPACES_MEXICO.md
# -----------------------------------------------------------------------------
SPECIES = [
    "Accipiter_striatus",       # 0  — SSHA — Sharp-shinned Hawk          — Gavilán pajarero
    "Aquila_chrysaetos",        # 1  — GOEA — Golden Eagle                — Águila real
    "Astur_atricapillus",       # 2  — NOGO — American Goshawk            — Gavilán azor americano (AOS 2023)
    "Astur_cooperii",           # 3  — COHA — Cooper's Hawk               — Gavilán de Cooper (AOS 2023)
    "Busarellus_nigricollis",   # 4  — BCHA — Black-collared Hawk         — Aguililla canela
    "Buteo_albonotatus",        # 5  — ZTHA — Zone-tailed Hawk            — Aguililla aura
    "Buteo_brachyurus",         # 6  — STHA — Short-tailed Hawk           — Aguililla cola corta
    "Buteo_jamaicensis",        # 7  — RTHA — Red-tailed Hawk             — Aguililla cola roja
    "Buteo_lagopus",            # 8  — RLHA — Rough-legged Hawk           — Aguililla ártica
    "Buteo_lineatus",           # 9  — RSHA — Red-shouldered Hawk         — Aguililla pecho rojo
    "Buteo_plagiatus",          # 10 — GRHA — Gray Hawk                   — Aguililla gris (AOS split)
    "Buteo_platypterus",        # 11 — BWHA — Broad-winged Hawk           — Aguililla ala ancha
    "Buteo_regalis",            # 12 — FEHA — Ferruginous Hawk            — Aguililla real
    "Buteo_swainsoni",          # 13 — SWHA — Swainson's Hawk             — Aguililla de Swainson
    "Buteogallus_anthracinus",  # 14 — COBH — Common Black Hawk           — Aguililla negra menor
    "Buteogallus_solitarius",   # 15 — SOEA — Solitary Eagle              — Águila solitaria
    "Buteogallus_urubitinga",   # 16 — GBHA — Great Black Hawk            — Aguililla negra mayor
    "Caracara_plancus",         # 17 — CRCA — Crested Caracara            — Caracara quebrantahuesos
    "Cathartes_aura",           # 18 — TUVU — Turkey Vulture              — Zopilote aura
    "Cathartes_burrovianus",    # 19 — LYHV — Lesser Yellow-headed Vulture — Zopilote sabanero
    "Chondrohierax_uncinatus",  # 20 — HBKI — Hook-billed Kite            — Gavilán pico de gancho
    "Circus_hudsonius",         # 21 — NOHA — Northern Harrier            — Aguilucho norteño
    "Coragyps_atratus",         # 22 — BLVU — Black Vulture               — Zopilote común
    "Daptrius_americanus",      # 23 — RTCA — Red-throated Caracara       — Caracara comecacao
    "Elanoides_forficatus",     # 24 — STKI — Swallow-tailed Kite         — Milano tijereta
    "Elanus_leucurus",          # 25 — WTKI — White-tailed Kite           — Milano coliblanco
    "Falco_columbarius",        # 26 — MERL — Merlin                      — Esmerejón
    "Falco_deiroleucus",        # 27 — OBFA — Orange-breasted Falcon      — Halcón pechirrufo
    "Falco_femoralis",          # 28 — APFA — Aplomado Falcon             — Halcón fajado
    "Falco_peregrinus",         # 29 — PEFA — Peregrine Falcon            — Halcón peregrino
    "Falco_rufigularis",        # 30 — BAFA — Bat Falcon                  — Halcón murcielaguero
    "Falco_sparverius",         # 31 — AMKE — American Kestrel            — Cernícalo americano
    "Geranoaetus_albicaudatus", # 32 — WTHA — White-tailed Hawk           — Aguililla cola blanca
    "Geranospiza_caerulescens", # 33 — CRHA — Crane Hawk                  — Gavilán zancón
    "Haliaeetus_leucocephalus", # 34 — BAEA — Bald Eagle                  — Águila calva
    "Harpagus_bidentatus",      # 35 — DTKI — Double-toothed Kite         — Gavilán bidentado
    "Harpia_harpyja",           # 36 — HAEA — Harpy Eagle                 — Águila arpía
    "Herpetotheres_cachinnans", # 37 — LAFA — Laughing Falcon             — Halcón guaco
    "Ictinia_mississippiensis", # 38 — MIKI — Mississippi Kite            — Milano de Mississippi
    "Ictinia_plumbea",          # 39 — PLKI — Plumbeous Kite              — Milano plomizo
    "Leptodon_cayanensis",      # 40 — GHKI — Gray-headed Kite            — Milano cabecigris
    "Micrastur_ruficollis",     # 41 — BFFA — Barred Forest-Falcon        — Halcón selvático barrado
    "Micrastur_semitorquatus",  # 42 — CFFA — Collared Forest-Falcon      — Halcón selvático de collar
    "Morphnus_guianensis",      # 43 — CREA — Crested Eagle               — Águila monera
    "Pandion_haliaetus",        # 44 — OSPR — Osprey                      — Águila pescadora
    "Parabuteo_unicinctus",     # 45 — HASH — Harris's Hawk               — Aguililla rojinegra
    "Pseudastur_albicollis",    # 46 — WHHA — White Hawk                  — Aguililla blanca
    "Rostrhamus_sociabilis",    # 47 — SNKI — Snail Kite                  — Caracolero común
    "Rupornis_magnirostris",    # 48 — ROHA — Roadside Hawk               — Aguililla caminera
    "Sarcoramphus_papa",        # 49 — KIVU — King Vulture                — Zopilote rey
    "Spizaetus_melanoleucus",   # 50 — BAWE — Black-and-white Hawk-Eagle  — Águila blanquinegra
    "Spizaetus_ornatus",        # 51 — ORHE — Ornate Hawk-Eagle           — Águila elegante
    "Spizaetus_tyrannus",       # 52 — BLHE — Black Hawk-Eagle            — Águila tirana
]
NUM_CLASSES = len(SPECIES)  # = 53

# Códigos de 4 letras (alpha codes estilo AOU/eBird) alineados con SPECIES
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

# Familia taxonómica por especie (paralela a SPECIES) — útil para coarse classifier
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

# Verificación de consistencia (siempre debe pasar)
assert len(SPECIES) == len(SPECIES_CODE) == len(SPECIES_COMMON) \
    == len(SPECIES_COMMON_ES) == len(SPECIES_FAMILY) == 53, \
    f"Inconsistencia: SPECIES={len(SPECIES)} CODE={len(SPECIES_CODE)} " \
    f"EN={len(SPECIES_COMMON)} ES={len(SPECIES_COMMON_ES)} " \
    f"FAM={len(SPECIES_FAMILY)} (esperado 53)"

# Verificación de orden alfabético (crítico para alinear con ImageFolder)
assert SPECIES == sorted(SPECIES), \
    "SPECIES debe estar en orden alfabético para coincidir con ImageFolder."

# -----------------------------------------------------------------------------
# Dispositivo (auto-detección multiplataforma)
#   - cuda   → NVIDIA con CUDA instalado (Windows / Linux)
#   - mps    → Apple Silicon (M1/M2/M3/M4) en macOS 12.3+
#   - cpu    → fallback universal (mucho más lento)
# -----------------------------------------------------------------------------
def _detect_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")

DEVICE = _detect_device()

# -----------------------------------------------------------------------------
# Hiperparámetros — etapa 1 (feature extraction) y etapa 2 (fine-tuning)
# -----------------------------------------------------------------------------
INPUT_SIZE = 224
ARCH_INPUT_SIZE = {
    "resnet50": 224,
    "mobilenet_v3_large": 224,
    "efficientnet_b3": 300,
    "convnext_tiny": 232,
}


def input_size_for_arch(arch: str) -> int:
    """Devuelve el tamaño de entrada recomendado para cada arquitectura."""
    return ARCH_INPUT_SIZE.get(arch.lower(), INPUT_SIZE)


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
    epochs=80,                # Más épocas para 53 clases (antes 60 para 23)
    lr=1e-4,
    optimizer="adamw",
    freeze_backbone=False,
    weight_decay=5e-4,
    label_smoothing=0.1,
    mixup_alpha=0.2,
    cutmix_alpha=1.0,
    scheduler="cosine",      # cosine annealing
    warmup_epochs=3,
    early_stopping_patience=15,  # paciencia extendida (53 clases tardan más en converger)
)

# Para GPUs muy limitadas: arquitectura recomendada con su batch_size sugerido
RECOMMENDED_BATCH = {
    "resnet50":           {"4GB": 16, "8GB": 32, "16GB": 64},
    "efficientnet_b3":    {"4GB": 8,  "8GB": 16, "16GB": 32},
    "mobilenet_v3_large": {"4GB": 32, "8GB": 64, "16GB": 128},
    "convnext_tiny":      {"4GB": 8,  "8GB": 16, "16GB": 32},
}

# Class weighting para clases raras (Harpia, Morphnus, Falco deiroleucus,
# Spizaetus spp., Buteogallus solitarius). Activar al entrenar.
USE_CLASS_WEIGHTS = True

# -----------------------------------------------------------------------------
# Reproducibilidad
# -----------------------------------------------------------------------------
SEED = 42

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
USE_WANDB = False        # poner True cuando se configure W&B
WANDB_PROJECT = "raptors-mexico-cnn"   # antes: "raptors-veracruz-cnn"
