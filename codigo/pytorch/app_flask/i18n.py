"""
raptors-cnn — Sistema de internacionalización (i18n) para la app Flask.

Adaptado de raptor_australia/gui/i18n.py. Carga un archivo JSON por idioma
desde ``app_flask/translations/`` y expone:
- ``t(key)`` con fallback a inglés y a la propia clave si no hay traducción.
- ``get_locale()`` resuelve por query param → cookie → Accept-Language → default.
- ``LANGUAGES`` registry de idiomas disponibles (visibles en el picker).

El proyecto raptors-cnn inicia con **español (México) por defecto** y se puede
expandir progresivamente a los 10 idiomas soportados por la base Australia.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from flask import request

TRANSLATIONS_DIR = Path(__file__).parent / "translations"
DEFAULT_LANG     = "es"
COOKIE_NAME      = "raptors_lang"

# Registry de idiomas. El orden aquí es el orden mostrado en el dropdown.
# Cada idioma agregado requiere su correspondiente translations/<code>.json
LANGUAGES: dict[str, dict[str, str]] = {
    "es": {"name": "Spanish",   "native": "Español",     "flag": "🇲🇽"},
    "en": {"name": "English",   "native": "English",     "flag": "🇺🇸"},
    "pt": {"name": "Portuguese","native": "Português",   "flag": "🇧🇷"},
    "fr": {"name": "French",    "native": "Français",    "flag": "🇫🇷"},
}

_TRANSLATIONS: dict[str, dict[str, Any]] = {}


def _load_one(code: str) -> dict[str, Any]:
    path = TRANSLATIONS_DIR / f"{code}.json"
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_translations() -> None:
    """Carga todas las traducciones de los idiomas registrados."""
    _TRANSLATIONS.clear()
    for code in LANGUAGES:
        _TRANSLATIONS[code] = _load_one(code)


def get_locale() -> str:
    """
    Resuelve la localización actual en orden de prioridad:
    1. ``?lang=xx`` (override de una sola petición)
    2. Cookie ``raptors_lang``
    3. Header ``Accept-Language``
    4. Default (es)
    """
    try:
        qlang = (request.args.get("lang") or "").lower()
        if qlang in LANGUAGES:
            return qlang

        clang = (request.cookies.get(COOKIE_NAME) or "").lower()
        if clang in LANGUAGES:
            return clang

        accept = (request.accept_languages.best_match(list(LANGUAGES))
                  if request.accept_languages else None)
        if accept:
            return accept
    except RuntimeError:
        # Fuera de contexto Flask (e.g. tests)
        pass

    return DEFAULT_LANG


def _walk(d: dict, dotted: str) -> Any:
    cur: Any = d
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def t(key: str, **format_args: Any) -> str:
    """
    Traduce ``key`` (path con puntos, e.g. ``'home.title'``) en la
    localización actual, con fallback al idioma por defecto (es), y al
    final a la propia clave si no se encuentra.
    """
    lang = get_locale()

    primary  = _walk(_TRANSLATIONS.get(lang, {}),         key)
    fallback = _walk(_TRANSLATIONS.get(DEFAULT_LANG, {}), key)
    value    = primary if isinstance(primary, str) and primary else fallback
    if not isinstance(value, str) or not value:
        value = key

    if format_args:
        try:
            value = value.format(**format_args)
        except (KeyError, IndexError, ValueError):
            pass
    return value


def get_languages() -> dict[str, dict[str, str]]:
    """Expone LANGUAGES a los templates."""
    return LANGUAGES
