"""Iconos y glifos reutilizados en toda la interfaz.

Centralizar los símbolos evita inconsistencias (p.ej. mezclar ">" y
"❯" en distintos módulos) y facilita cambiar el set completo de
iconos en un solo lugar, incluyendo un modo ASCII de respaldo para
terminales sin soporte Unicode/Nerd Fonts.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Icons:
    # Marca / prompt
    brand_mark: str = "▲"
    arrow: str = "❯"

    # Estados
    success: str = "✓"
    warning: str = "⚠"
    error: str = "✗"
    info: str = "ℹ"

    # Dominio
    provider: str = "⚙"
    model: str = "◆"
    help: str = "?"

    # Estructura
    bullet: str = "·"
    separator: str = "│"
    ellipsis: str = "…"
    chevron_right: str = "›"


@dataclass(frozen=True, slots=True)
class AsciiIcons:
    brand_mark: str = "A"
    arrow: str = ">"

    success: str = "OK"
    warning: str = "!"
    error: str = "x"
    info: str = "i"

    provider: str = "#"
    model: str = "*"
    help: str = "?"

    bullet: str = "-"
    separator: str = "|"
    ellipsis: str = "..."
    chevron_right: str = ">"


ICONS = Icons()
ICONS_ASCII = AsciiIcons()