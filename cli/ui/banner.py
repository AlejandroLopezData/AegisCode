"""Banner de bienvenida de AegisCode CLI.

Cabecera compacta: escudo simple a la izquierda + "AEGIS CODE" y versión
a la derecha, con el modelo/proveedor activos y el workspace debajo.
Todo construido como un único Text para que el Panel se ajuste al
contenido real (expand=False) en vez de ocupar todo el ancho de la
terminal.
"""

from __future__ import annotations

import os

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from config.active_store import get_active_model_id
from config.models_store import load_models
from config.providers_store import load_providers
from cli.ui.style import PALETTE

# TODO: mover a un origen único de versión (ej. cli/spec.py) cuando exista.
VERSION = "0.1.0"


_SHIELD = [
    "▄▄▄▄▄▄",
    "█▄██▄█",
    "██████",
    "▀▀▀▀▀▀",
]
def _active_summary() -> str:
    """Devuelve 'modelo · proveedor' del modelo activo, o un mensaje si no hay."""
    model_id = get_active_model_id()
    if not model_id:
        return "No active model · No active provider"

    models_cfg = load_models()
    model = next((m for m in models_cfg.models if m.id == model_id), None)
    if not model:
        return f"{model_id} · Unknown provider"

    return f"{model.id} · {model.provider}"


def build_banner() -> Panel:
    """Construye el panel de bienvenida con estado real del sistema."""
    active = _active_summary()
    workspace = os.getcwd()

    body = Text()
    for i, row in enumerate(_SHIELD):
        for ch in row:
            if ch == " ":
                body.append(" ")
            elif ch in "▄▀":
                body.append(ch, style=f"bold bright_{PALETTE.brand}")
            else:
                body.append(ch, style=f"bold {PALETTE.brand}")
        body.append("  ")

        if i == 0:
            body.append("AEGIS CODE", style=f"bold {PALETTE.text}")
            body.append(f"  v{VERSION}", style=f"dim {PALETTE.muted}")
        elif i == 1:
            body.append("─" * 24, style=f"dim {PALETTE.subtle}")
        elif i == 2:
            body.append(active, style=f"bold {PALETTE.text}")
        elif i == 3:
            body.append("Workspace  ", style=f"dim {PALETTE.muted}")
            body.append(workspace, style=f"dim {PALETTE.muted}")

        if i < len(_SHIELD) - 1:
            body.append("\n")

    return Panel(
        body,
        border_style=PALETTE.subtle,
        padding=(1, 2),
        expand=False,
    )


def print_banner(console: Console) -> None:
    """Imprime el banner seguido de la línea de ayuda rápida."""
    console.print(build_banner())
    console.print()
    hint = Text()
    hint.append("/", style=f"bold {PALETTE.brand}")
    hint.append(" show commands   ", style=f"dim {PALETTE.muted}")
    console.print(hint)