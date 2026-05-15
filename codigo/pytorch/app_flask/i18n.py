"""
Internacionalización (i18n) para la app Flask.

Adaptado de raptor_australia/gui/i18n.py.

Lee archivos JSON de translations/<lang>.json y expone:
  - load_translations()          → carga todos los JSON al iniciar la app
  - t("clave.anidada")           → traduce a la lengua actual (cookie)
  - get_locale()                 → devuelve el código del idioma actual
  - get_languages()              → lista de idiomas con su etiqueta

Para agregar un idioma: crea translations/<código>.json y agrégalo a LANGUAGES.
"""
import json
from pathlib import Path
from flask import request

COOKIE_NAME = "raptors_cnn_lang"
DEFAULT_LANG = "es"

# Lista de idiomas soportados (orden = orden en el selector de la UI)
LANGUAGES: dict[str, str] = {
    "es": "Español",
    "en": "English",
    # Próximos: "fr": "Français", "pt": "Português", ...
}

# Caché de traducciones cargadas en memoria
_TRANSLATIONS: dict[str, dict] = {}


def load_translations() -> None:
    """Carga todos los JSON de translations/ al iniciar la app."""
    base = Path(__file__).parent / "translations"
    for code in LANGUAGES:
        path = base / f"{code}.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                _TRANSLATIONS[code] = json.load(f)
        else:
            _TRANSLATIONS[code] = {}


def get_locale() -> str:
    """
    Devuelve el código del idioma actual.

    Orden de prioridad:
      1. Cookie del usuario (set por /set_lang/<code>)
      2. Header Accept-Language del navegador
      3. DEFAULT_LANG (es)
    """
    try:
        cookie_lang = request.cookies.get(COOKIE_NAME)
        if cookie_lang and cookie_lang in LANGUAGES:
            return cookie_lang
        accept = request.headers.get("Accept-Language", "")
        for chunk in accept.split(","):
            code = chunk.split(";")[0].split("-")[0].strip()
            if code in LANGUAGES:
                return code
    except RuntimeError:
        # Fuera de contexto Flask (e.g. en tests)
        pass
    return DEFAULT_LANG


def get_languages() -> list[tuple[str, str]]:
    """[(code, etiqueta_visual)] para renderizar el selector de idioma."""
    return list(LANGUAGES.items())


def t(key: str, default: str | None = None) -> str:
    """
    Traduce una clave anidada con notación de puntos.

    Ejemplo:
        t("nav.identify")  busca _TRANSLATIONS[locale]["nav"]["identify"]
                           fallback a la traducción inglesa si falta
                           fallback al `default` si tampoco existe
                           fallback al string clave si todo falla.
    """
    locale = get_locale()
    keys = key.split(".")
    for lang_to_try in (locale, "en", DEFAULT_LANG):
        node = _TRANSLATIONS.get(lang_to_try, {})
        for k in keys:
            if isinstance(node, dict) and k in node:
                node = node[k]
            else:
                node = None
                break
        if isinstance(node, str):
            return node
    return default if default is not None else key
