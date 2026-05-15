"""
Generador de placeholders visuales para las señas en International Sign.

Mientras los videos reales se graban con la comunidad sorda, esta función
crea una tarjeta SVG con: código de especie, nombre científico, descripción
de la seña y un icono representativo.

Cuando estén los videos, simplemente se reemplazará la llamada por la carga
del .mp4 correspondiente en `lengua_de_senas/videos/<COD>.mp4`.
"""
from __future__ import annotations
import io
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from .config_app import SPECIES_DATA, SIGNS_DIR


def get_sign_for_species(scientific_name: str) -> tuple[Image.Image, str, Path | None]:
    """
    Devuelve:
      - PIL.Image con el placeholder/tarjeta de la seña
      - Descripción textual
      - Path al video real si existe, None si solo hay placeholder
    """
    info = SPECIES_DATA.get(scientific_name)
    if info is None:
        return _error_card("Especie desconocida"), "—", None

    # ¿Existe video real?
    video_path = SIGNS_DIR / f"{info.code}_{scientific_name}.mp4"
    real_video = video_path if video_path.exists() else None

    card = _make_sign_card(info)
    return card, info.sign_description, real_video


def _make_sign_card(info) -> Image.Image:
    """
    Genera una tarjeta visual estilo 'flashcard' con la seña.
    Tamaño 800x600, paleta personalizada por especie.
    """
    W, H = 800, 600
    primary = _hex_to_rgb(info.sign_palette[0])
    secondary = _hex_to_rgb(info.sign_palette[1])

    img = Image.new("RGB", (W, H), (245, 245, 245))
    draw = ImageDraw.Draw(img)

    # Banner superior con gradiente vertical aproximado
    for y in range(120):
        t = y / 120
        r = int(primary[0] * (1 - t) + secondary[0] * t)
        g = int(primary[1] * (1 - t) + secondary[1] * t)
        b = int(primary[2] * (1 - t) + secondary[2] * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Código de especie - círculo grande
    cx, cy, r = 150, 300, 80
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=primary, outline=secondary, width=4)

    # Cargar fuentes
    try:
        font_huge = ImageFont.truetype("DejaVuSans-Bold.ttf", 64)
        font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 28)
        font_subtitle = ImageFont.truetype("DejaVuSans-Oblique.ttf", 20)
        font_body = ImageFont.truetype("DejaVuSans.ttf", 16)
        font_small = ImageFont.truetype("DejaVuSans.ttf", 14)
    except OSError:
        font_huge = ImageFont.load_default()
        font_title = font_subtitle = font_body = font_small = font_huge

    # Texto del código en el círculo
    code_bbox = draw.textbbox((0, 0), info.code, font=font_huge)
    code_w = code_bbox[2] - code_bbox[0]
    code_h = code_bbox[3] - code_bbox[1]
    draw.text((cx - code_w // 2, cy - code_h // 2 - 8), info.code,
              fill="white", font=font_huge)

    # Header en el banner
    draw.text((20, 20), "Seña en International Sign", fill="white", font=font_title)
    draw.text((20, 60), info.common_name_en, fill="white", font=font_subtitle)

    # Nombre científico (italic en panel derecho)
    draw.text((280, 180), info.scientific_name, fill=primary, font=font_subtitle)
    draw.text((280, 215), info.common_name_es, fill=(70, 70, 70), font=font_body)
    draw.text((280, 245), f"Familia: {info.family}", fill=(120, 120, 120), font=font_small)
    draw.text((280, 268), f"Abundancia: {info.abundance}", fill=(120, 120, 120), font=font_small)

    # Línea separadora
    draw.line([(280, 305), (W - 30, 305)], fill=secondary, width=2)

    # Descripción de la seña
    draw.text((280, 325), "Descripción de la seña:",
              fill=primary, font=font_subtitle)
    _wrap_text(draw, info.sign_description, font_body,
               x=280, y=360, max_width=W - 310,
               max_lines=5, fill=(40, 40, 40))

    # Footer
    draw.line([(20, H - 50), (W - 20, H - 50)], fill=secondary, width=1)
    draw.text((20, H - 38), "Placeholder visual mientras se graban los videos con la comunidad sorda.",
              fill=(100, 100, 100), font=font_small)
    draw.text((20, H - 18), "raptors-cnn — Tesis de Maestría — Brian Fernández Báez",
              fill=(120, 120, 120), font=font_small)

    return img


def _wrap_text(draw, text: str, font, x: int, y: int, max_width: int,
               max_lines: int = 5, fill=(0, 0, 0), line_height: int = 22) -> None:
    """Word-wrap manual para texto largo."""
    words = text.split()
    lines = []
    current = ""
    for w in words:
        test = (current + " " + w).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
        if len(lines) >= max_lines:
            break
    if current and len(lines) < max_lines:
        lines.append(current)
    for i, line in enumerate(lines):
        draw.text((x, y + i * line_height), line, fill=fill, font=font)


def _error_card(message: str) -> Image.Image:
    img = Image.new("RGB", (800, 200), (245, 245, 245))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
    draw.text((20, 80), message, fill=(184, 80, 66), font=font)
    return img


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
