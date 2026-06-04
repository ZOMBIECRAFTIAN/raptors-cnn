"""
raptors-cnn — Metadatos por especie para la GUI Flask.

Construye SPECIES_INFO desde `config.py` + `species_data.py`, añadiendo:
- color por especie (paleta por familia)
- estatus IUCN + NOM-059
- nombre del archivo de seña (International Sign)
- hábitat resumido
- diagnóstico de campo

Esto reemplaza el dict hardcoded de Australia (gui/app.py:SPECIES_INFO)
adaptándolo a las 53 rapaces mexicanas y a la nomenclatura del proyecto.

Las claves coinciden con `config.SPECIES` (formato Genus_species) para que
los templates puedan iterar sobre `species_info.items()` sin transformaciones.
"""
from __future__ import annotations
import sys
from pathlib import Path

# Imports del proyecto principal
_BASE = Path(__file__).resolve().parent
_PYTORCH = _BASE.parent
sys.path.insert(0, str(_PYTORCH))
import config  # noqa: E402

sys.path.insert(0, str(_BASE))
from species_data import SPECIES_DETAILS  # noqa: E402

# Optional English translation overrides (work in progress).
# Falls back silently to Spanish when a species/field is not yet translated.
try:
    from species_data_en import (
        SPECIES_DETAILS_EN,
        IUCN_STATUS_EN,
        SHORT_PHRASE_EN,
    )
except ImportError:
    SPECIES_DETAILS_EN: dict[str, dict[str, str]] = {}
    IUCN_STATUS_EN: dict[str, str] = {}
    SHORT_PHRASE_EN: dict[str, str] = {}


_PAREN_ES_TO_EN = {
    "declinante regional":   "regionally declining",
    "estable":               "stable",
    "en aumento":            "increasing",
    "estable regional":      "regionally stable",
    "amenazada regional":    "regionally threatened",
}


def _clean_iucn_status(raw: str, lang: str) -> str:
    """Map the IUCN headline to English while preserving any parenthetical
    note (translating the few common Spanish phrases). Does not delete info.
    Examples:
        'Least Concern (declinante regional)' + lang='en'
            -> 'Least Concern (regionally declining)'
        'Preocupacion Menor' + lang='en'
            -> 'Least Concern'
    """
    if not raw or raw == "—":
        return raw
    # Split head and optional parenthetical note
    if "(" in raw and raw.endswith(")"):
        head, _, rest = raw.partition("(")
        note = rest.rstrip(")").strip()
    else:
        head, note = raw, ""
    head = head.strip()
    if lang == "en":
        head = IUCN_STATUS_EN.get(head, IUCN_STATUS_EN.get(raw, head))
        if note:
            note = _PAREN_ES_TO_EN.get(note, note)
    return f"{head} ({note})" if note else head


def _translate_short(text: str, lang: str) -> str:
    """Apply short Spanish->English phrase substitutions when lang='en'.

    Used for habitat lines and the first sentence of distribution. Does not
    attempt full translation; if no entry in `SHORT_PHRASE_EN` matches, the
    original Spanish is returned unchanged.
    """
    if lang != "en" or not text:
        return text
    out = text
    for es, en in SHORT_PHRASE_EN.items():
        out = out.replace(es, en)
    return out


def localized_field(species_key: str, field: str, lang: str,
                    default: str = "—") -> str:
    """Return `field` for `species_key` in the requested locale.

    Priority: SPECIES_DETAILS_EN[species_key][field] (if lang='en' and present)
              -> SPECIES_DETAILS[species_key][field] (Spanish fallback)
              -> default ('—')
    """
    es_details = SPECIES_DETAILS.get(species_key, {})
    if lang == "en":
        en_details = SPECIES_DETAILS_EN.get(species_key, {})
        if field in en_details and en_details[field]:
            return en_details[field]
    return es_details.get(field, default)

# ─── Paleta por familia (3 tonos por familia para variedad) ───────────────
# Cathartidae: marrones tierra; Pandionidae: azul agua; Accipitridae:
# variedad amplia (gavilanes-verde, águilas-bordó, milanos-turquesa);
# Falconidae: tonos cálidos (rojo-naranja-púrpura).
_FAMILY_PALETTES = {
    "Cathartidae":  ["#5D4037", "#8D6E63", "#6D4C41", "#4E342E"],
    "Pandionidae":  ["#1976D2"],
    "Accipitridae": [
        "#2E7D32", "#558B2F", "#33691E", "#827717", "#1B5E20", "#4CAF50",
        "#388E3C", "#689F38", "#7CB342", "#9E9D24", "#AFB42B", "#C0CA33",
        "#00897B", "#00695C", "#26A69A", "#80CBC4", "#004D40", "#00ACC1",
        "#0097A7", "#0277BD", "#01579B", "#3949AB", "#283593", "#5E35B1",
        "#4527A0", "#7B1FA2", "#6A1B9A", "#AD1457", "#880E4F", "#C2185B",
        "#B71C1C", "#D32F2F", "#E64A19", "#BF360C", "#5D4037", "#6D4C41",
        "#3E2723", "#212121",
    ],
    "Falconidae":   [
        "#E53935", "#FF5722", "#FF6F00", "#F57C00", "#E64A19",
        "#C62828", "#AD1457", "#8E24AA", "#6A1B9A", "#4527A0",
    ],
}


def _build_species_info() -> dict[str, dict]:
    """Construye el dict completo SPECIES_INFO desde config + species_data."""
    cat_idx = 0
    pan_idx = 0
    acc_idx = 0
    fal_idx = 0

    info: dict[str, dict] = {}
    for class_idx, (sci, code, common_en, common_es, family) in enumerate(zip(
            config.SPECIES, config.SPECIES_CODE,
            config.SPECIES_COMMON, config.SPECIES_COMMON_ES,
            config.SPECIES_FAMILY)):

        # Selecciona color de la paleta de la familia
        if family == "Cathartidae":
            color = _FAMILY_PALETTES["Cathartidae"][cat_idx % 4]
            cat_idx += 1
        elif family == "Pandionidae":
            color = _FAMILY_PALETTES["Pandionidae"][pan_idx % 1]
            pan_idx += 1
        elif family == "Accipitridae":
            color = _FAMILY_PALETTES["Accipitridae"][acc_idx % 38]
            acc_idx += 1
        else:  # Falconidae
            color = _FAMILY_PALETTES["Falconidae"][fal_idx % 10]
            fal_idx += 1

        details = SPECIES_DETAILS.get(sci, {})
        info[sci] = {
            "common_name":     common_es,                  # Default es-MX
            "common_name_en":  common_en,
            "scientific_name": sci.replace("_", " "),
            "scientific_underscored": sci,
            "class_idx":       class_idx,
            "code":            code,
            "family":          family,
            "epbc_status":     details.get("iucn_status", "—"),  # mapeado al campo del template
            "iucn_status":     details.get("iucn_status", "—"),
            "habitat":         _habitat_from_distribution(details.get("distribution", "")),
            "wingspan_cm":     details.get("wingspan_cm", "—"),
            "length_cm":       details.get("length_cm", "—"),
            "diagnostic":      details.get("diagnostic", "—"),
            "is_sign":         _is_sign_for(sci),          # International Sign
            "is_video":        f"{sci}.svg",
            # Aliases que los templates de Australia usan
            "auslan_sign":     _is_sign_for(sci),
            "auslan_video":    f"{sci}.svg",
            "color":           color,
        }
    return info


def _habitat_from_distribution(dist: str) -> str:
    """Extrae un resumen corto de hábitat a partir de la descripción larga."""
    if not dist:
        return "—"
    # Primera oración hasta 90 caracteres
    first = dist.split(".")[0]
    return first[:90].strip() + ("…" if len(first) > 90 else "")


# Mini-catálogo de descripciones de seña en International Sign (placeholder).
# La descripción definitiva proviene del módulo lengua_de_senas/ validado con
# la comunidad sorda. Aquí incluimos descripciones provisionales útiles para la
# GUI mientras se completan los videos.
_IS_SIGNS = {
    "Aquila_chrysaetos": "Manos en V invertida descendente — alas largas en planeo elevado.",
    "Astur_cooperii":    "Mano dominante imitando rabieta corta — caza con emboscada.",
    "Astur_atricapillus": "Ambas manos en garras abiertas — agresividad y tamaño grande.",
    "Accipiter_striatus":"Dedos juntos batiendo rápido — alas cortas y veloces.",
    "Pandion_haliaetus": "Mano en pinza descendente sobre agua — picada al pez.",
    "Falco_peregrinus":  "Índice en picada vertical rápida — stoop.",
    "Falco_sparverius":  "Mano cernida estática — hovering pequeño.",
    "Falco_columbarius": "Puño compacto en vuelo recto — velocidad y agresividad pequeñas.",
    "Cathartes_aura":    "Brazos en V abierta + olfato — soaring + detección por olor.",
    "Coragyps_atratus":  "Manos descendentes en círculo + bandeo lateral — kettle agrupado.",
    "Buteo_jamaicensis": "Mano abierta en planeo amplio + apuntar a cola — cola roja.",
    "Buteo_platypterus": "Manos juntas formando espiral ascendente — kettle migratorio.",
    "Caracara_plancus":  "Caminar con los dedos + cabeza arriba — caracara terrestre.",
    "Harpia_harpyja":    "Manos en garras enormes — fuerza y selva.",
}


def _is_sign_for(sci: str) -> str:
    return _IS_SIGNS.get(sci, "Seña en preparación — pendiente de validación comunitaria.")


# Construye el dict una sola vez al importar
SPECIES_INFO: dict[str, dict] = _build_species_info()

# Verificación
assert len(SPECIES_INFO) == 53, f"Esperaba 53, hay {len(SPECIES_INFO)}"
