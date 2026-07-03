"""Tema centralizado de AegisCode CLI.

Toda la paleta de colores vive aquí. Ningún otro módulo debe declarar
colores hardcodeados: deben importar `Palette` o `RICH_STYLES` desde
este archivo.

La paleta está inspirada en Nord / Catppuccin (Mocha): fondos oscuros,
acentos fríos, buen contraste para terminales tanto claras como oscuras.
"""

from __future__ import annotations

from dataclasses import dataclass

from prompt_toolkit.styles import Style as PTStyle


@dataclass(frozen=True, slots=True)
class Palette:
    """Paleta de colores hexadecimales de la aplicación."""

    # Marca / acentos
    brand: str = "#89b4fa"       # azul suave (blue)
    accent: str = "#cba6f7"      # lavanda (mauve)

    # Estados semánticos
    success: str = "#a6e3a1"     # verde (green)
    warning: str = "#f9e2af"     # amarillo (yellow)
    error: str = "#f38ba8"       # rojo (red)
    info: str = "#89dceb"        # cian (sky)

    # Texto
    text: str = "#cdd6f4"        # texto principal
    muted: str = "#7f849c"       # texto secundario / dim
    subtle: str = "#585b70"      # bordes, separadores

    # Superficies
    surface: str = "#181825"     # fondo de paneles
    surface_alt: str = "#1e1e2e" # fondo alterno / filas de tabla

    # Sintaxis (lexer de comandos)
    syntax_command: str = "#89b4fa"     # /providers, /models
    syntax_subcommand: str = "#cba6f7"  # list, add, remove
    syntax_argument: str = "#a6e3a1"    # argumentos libres
    syntax_flag: str = "#f9e2af"        # --flags
    syntax_string: str = "#94e2d5"      # "strings" entre comillas


PALETTE = Palette()


class RichStyles:
    """Nombres de estilo listos para usar como `style="..."` en Rich.

    Se centralizan aquí como strings de marcado Rich (no objetos Style)
    porque así se pueden componer directamente en f-strings de consola,
    p.ej. `console.print(f"[{RichStyles.SUCCESS}]OK[/]")`.
    """

    BRAND = f"bold {PALETTE.brand}"
    ACCENT = f"bold {PALETTE.accent}"
    SUCCESS = PALETTE.success
    WARNING = PALETTE.warning
    ERROR = f"bold {PALETTE.error}"
    INFO = PALETTE.info
    TEXT = PALETTE.text
    MUTED = f"dim {PALETTE.muted}"
    SUBTLE = PALETTE.subtle

    PANEL_BORDER = PALETTE.subtle
    PANEL_BORDER_ACCENT = PALETTE.brand

    TABLE_HEADER = f"bold {PALETTE.brand}"
    TABLE_ROW_ALT = PALETTE.surface_alt


RICH_STYLES = RichStyles()


def build_prompt_toolkit_style() -> PTStyle:
    """Construye el `Style` de prompt_toolkit para el prompt y la toolbar.

    Las claves usadas aquí deben coincidir con las clases de estilo
    referenciadas en `ui/prompt.py` y `ui/toolbar.py` (p.ej. "prompt",
    "bottom-toolbar", etc.).
    """
    p = PALETTE
    return PTStyle.from_dict(
        {
            "": p.text,
            "prompt.brand": f"bold {p.brand}",
            "prompt.arrow": f"bold {p.accent}",
            "prompt.text": p.text,
            "bottom-toolbar": f"bg:{p.surface} {p.muted}",
            "bottom-toolbar.key": f"bg:{p.surface} bold {p.brand}",
            "bottom-toolbar.sep": f"bg:{p.surface} {p.subtle}",
            "completion-menu.completion": f"bg:{p.surface} {p.text}",
            "completion-menu.completion.current": f"bg:{p.brand} #11111b bold",
            "completion-menu.meta.completion": f"bg:{p.surface} {p.muted}",
            "completion-menu.meta.completion.current": f"bg:{p.brand} #11111b",
            "scrollbar.background": f"bg:{p.surface}",
            "scrollbar.button": f"bg:{p.subtle}",
        }
    )


PROMPT_TOOLKIT_STYLE = build_prompt_toolkit_style()