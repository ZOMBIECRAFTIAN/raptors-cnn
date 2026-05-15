"""
Configuración específica de la aplicación Gradio — info enriquecida de las 14
especies (descripción de seña, abundancia, ficha rápida) y constantes de UI.
"""
from dataclasses import dataclass
from pathlib import Path

# ----------------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------------
APP_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = APP_ROOT.parents[2]  # raptors-cnn/
SIGNS_DIR = PROJECT_ROOT / "lengua_de_senas" / "videos"  # videos a futuro
ASSETS_DIR = APP_ROOT / "assets"

# ----------------------------------------------------------------------------
# Datos enriquecidos por especie
# ----------------------------------------------------------------------------
@dataclass
class SpeciesInfo:
    """Información completa de una especie para la UI."""
    code: str                    # BW, SW, etc.
    scientific_name: str         # Buteo platypterus
    common_name_es: str          # Aguililla ala-ancha
    common_name_en: str          # Broad-winged Hawk
    family: str                  # Accipitridae
    abundance: str               # Extrema | Muy alta | Alta | Media | Baja-media | Baja
    field_marks: str             # Caracteres diagnósticos
    sign_description: str        # Descripción de la seña en IS
    sign_palette: tuple          # 2 colores hex para el placeholder SVG


SPECIES_DATA = {
    "Accipiter_striatus": SpeciesInfo(
        code="SS", scientific_name="Accipiter striatus",
        common_name_es="Gavilán pajarero", common_name_en="Sharp-shinned Hawk",
        family="Accipitridae", abundance="Media",
        field_marks="Alas cortas redondeadas, cola larga cuadrada. Tamaño pequeño.",
        sign_description="Dos dedos extendidos junto al rostro indicando aleteos rápidos. Tamaño pequeño se enfatiza con cercanía al cuerpo.",
        sign_palette=("#5A7D9A", "#A8C3D9"),
    ),
    "Astur_cooperii": SpeciesInfo(
        code="CH", scientific_name="Astur cooperii",
        common_name_es="Gavilán de Cooper", common_name_en="Cooper's Hawk",
        family="Accipitridae", abundance="Media",
        field_marks="Similar al Sharp-shinned pero más grande, cola larga redondeada.",
        sign_description="Mano abierta apuntando arriba junto al rostro, con 3 movimientos cortos (aleteos + planeo). Tamaño relativo mayor que SS.",
        sign_palette=("#6B8E23", "#B0C982"),
    ),
    "Buteo_albonotatus": SpeciesInfo(
        code="ZT", scientific_name="Buteo albonotatus",
        common_name_es="Aguililla aura", common_name_en="Zone-tailed Hawk",
        family="Accipitridae", abundance="Baja",
        field_marks="Mimético del Turkey Vulture: vuelo en V, pero cola con bandas blancas.",
        sign_description="Variante de la seña TV (V con los dedos) + modulación de cola bandeada con dedo índice.",
        sign_palette=("#2C2C2C", "#888888"),
    ),
    "Buteo_jamaicensis": SpeciesInfo(
        code="RT", scientific_name="Buteo jamaicensis",
        common_name_es="Aguililla cola roja", common_name_en="Red-tailed Hawk",
        family="Accipitridae", abundance="Media",
        field_marks="Alas anchas, cola roja brillante en adulto. Rasgo diagnóstico inmediato.",
        sign_description="Mano dominante extendida atrás a la altura de la cadera, referencia directa a la cola roja.",
        sign_palette=("#B85042", "#E0998F"),
    ),
    "Buteo_lineatus": SpeciesInfo(
        code="RS", scientific_name="Buteo lineatus",
        common_name_es="Aguililla pecho rojo", common_name_en="Red-shouldered Hawk",
        family="Accipitridae", abundance="Baja-media",
        field_marks="Alas con 'ventanas' translúcidas en primarias internas, hombros rojizos.",
        sign_description="Mano tocando suavemente el hombro — referencia directa a la mancha rojiza del hombro del adulto.",
        sign_palette=("#A0522D", "#D4A574"),
    ),
    "Buteo_platypterus": SpeciesInfo(
        code="BW", scientific_name="Buteo platypterus",
        common_name_es="Aguililla ala-ancha", common_name_en="Broad-winged Hawk",
        family="Accipitridae", abundance="Extrema",
        field_marks="Alas cortas y anchas, cola con bandas blancas y negras anchas. Forma kettles enormes en pico migratorio.",
        sign_description="Antebrazo y mano horizontales con palma hacia abajo, ligero arriba-abajo (ala ancha + kettle).",
        sign_palette=("#4A5D23", "#9CAF88"),
    ),
    "Buteo_swainsoni": SpeciesInfo(
        code="SW", scientific_name="Buteo swainsoni",
        common_name_es="Aguililla de Swainson", common_name_en="Swainson's Hawk",
        family="Accipitridae", abundance="Muy alta",
        field_marks="Alas largas y puntiagudas, contraste primarias oscuras / coberteras claras (vientre).",
        sign_description="Mano dominante en V poco marcada + planeo lateral.",
        sign_palette=("#8B7355", "#D2B48C"),
    ),
    "Cathartes_aura": SpeciesInfo(
        code="TV", scientific_name="Cathartes aura",
        common_name_es="Zopilote aura", common_name_en="Turkey Vulture",
        family="Cathartidae", abundance="Muy alta",
        field_marks="Alas largas y angostas, vuelo en V marcada (diédrico), cabeza roja desnuda en adultos.",
        sign_description="Dos dedos extendidos en V con la mano dominante, representando el diédrico marcado.",
        sign_palette=("#3D2817", "#8B4513"),
    ),
    "Circus_hudsonius": SpeciesInfo(
        code="NH", scientific_name="Circus hudsonius",
        common_name_es="Gavilán rastrero", common_name_en="Northern Harrier",
        family="Accipitridae", abundance="Baja-media",
        field_marks="Alas largas en V poco marcada, parche blanco en grupa muy visible, vuelo bajo.",
        sign_description="Antebrazo horizontal palma abajo + barrido lateral (vuelo bajo en pastizales).",
        sign_palette=("#708090", "#B0C4DE"),
    ),
    "Falco_columbarius": SpeciesInfo(
        code="ML", scientific_name="Falco columbarius",
        common_name_es="Esmerejón", common_name_en="Merlin",
        family="Falconidae", abundance="Baja",
        field_marks="Pequeño, alas puntiagudas, vuelo extremadamente rápido y directo.",
        sign_description="Puño compacto con dedo apuntando adelante, movimiento veloz horizontal.",
        sign_palette=("#36454F", "#778899"),
    ),
    "Falco_peregrinus": SpeciesInfo(
        code="PG", scientific_name="Falco peregrinus",
        common_name_es="Halcón peregrino", common_name_en="Peregrine Falcon",
        family="Falconidae", abundance="Baja",
        field_marks="Alas largas y puntiagudas, 'capucha' negra, cola corta. Stoop a >300 km/h.",
        sign_description="Mano vertical descendente rápida — simboliza el stoop (picada vertical).",
        sign_palette=("#1C2841", "#5B6E8C"),
    ),
    "Falco_sparverius": SpeciesInfo(
        code="AK", scientific_name="Falco sparverius",
        common_name_es="Cernícalo americano", common_name_en="American Kestrel",
        family="Falconidae", abundance="Media",
        field_marks="Pequeño, alas puntiagudas, cola rufa con banda terminal negra. Vuelo cernido (hovering).",
        sign_description="Mano cerrada como garra + movimiento de hovering (vuelo cernido).",
        sign_palette=("#C26B41", "#E8B17D"),
    ),
    "Ictinia_mississippiensis": SpeciesInfo(
        code="MK", scientific_name="Ictinia mississippiensis",
        common_name_es="Elanio Mississippi", common_name_en="Mississippi Kite",
        family="Accipitridae", abundance="Alta",
        field_marks="Cola larga y oscura, cabeza clara, alas largas y puntiagudas. Captura insectos en vuelo.",
        sign_description="Mano abierta vertical junto al hombro con movimiento ascendente-descendente.",
        sign_palette=("#4F6D7A", "#8DA9B4"),
    ),
    "Pandion_haliaetus": SpeciesInfo(
        code="OS", scientific_name="Pandion haliaetus",
        common_name_es="Águila pescadora", common_name_en="Osprey",
        family="Pandionidae", abundance="Baja-media",
        field_marks="Alas con quiebre en muñeca (forma de M), pecho blanco, banda ocular oscura.",
        sign_description="Mano en forma de garra cerrándose sobre la otra — zambullida + captura de pez.",
        sign_palette=("#2C5F2D", "#88AA88"),
    ),
}

# Lista en orden alfabético (mismo orden que ImageFolder)
SPECIES_ORDER = sorted(SPECIES_DATA.keys())


# ----------------------------------------------------------------------------
# Constantes de UI
# ----------------------------------------------------------------------------
APP_TITLE = "🦅 raptors-cnn — Identificación de aves rapaces"
APP_DESCRIPTION = """
Sistema integrado de **identificación visual de aves rapaces migratorias del corredor de Veracruz**
mediante redes neuronales convolucionales, con catálogo de señas en **International Sign** para
inclusión de la comunidad sorda.

Tesis de Maestría · Brian Fernández Báez · 2026
"""

THEME_PRIMARY = "#2C5F2D"
THEME_ACCENT = "#B85042"
THEME_BG = "#F5F5F5"

# Configuración de procesamiento de video
VIDEO_SAMPLE_EVERY_SECS = 2.0      # extraer 1 frame cada N segundos
VIDEO_MAX_DURATION_SECS = 60       # video máx 60s para no tronar
VIDEO_MIN_CONFIDENCE = 0.30        # umbral de confianza para considerar predicción
