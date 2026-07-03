"""Toolbar inferior de AegisCode CLI.

`PromptSession(bottom_toolbar=...)` acepta un callable que devuelve
`FormattedText`. Aquí se construye esa barra con los atajos
disponibles, reutilizando las clases de estilo definidas en
`ui/style.py` (`bottom-toolbar`, `bottom-toolbar.key`, etc.).
"""

from __future__ import annotations

from prompt_toolkit.formatted_text import FormattedText

from cli.ui.icons import ICONS

_SHORTCUTS: tuple[tuple[str, str], ...] = (
    ("TAB", "Completar"),
    ("↑ ↓", "Historial"),
    ("Ctrl+C", "Cancelar"),
    ("/", "Ayuda"),
)


def build_toolbar() -> FormattedText:
    """Construye el contenido de la toolbar inferior."""
    fragments: list[tuple[str, str]] = [("class:bottom-toolbar", "  ")]

    for index, (key, label) in enumerate(_SHORTCUTS):
        if index > 0:
            fragments.append(("class:bottom-toolbar.sep", f"  {ICONS.separator}  "))
        fragments.append(("class:bottom-toolbar.key", key))
        fragments.append(("class:bottom-toolbar", f" {label}"))

    fragments.append(("class:bottom-toolbar", "  "))
    return FormattedText(fragments)