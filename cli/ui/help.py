"""Panel de ayuda de AegisCode CLI.

Se genera dinámicamente a partir de `cli.spec.COMMAND_TREE`: añadir
un comando nuevo en `spec.py` lo hace aparecer aquí automáticamente,
sin tocar este archivo.
"""

from __future__ import annotations

from rich.console import Console, Group
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from cli.spec import COMMAND_TREE, CommandNode
from cli.ui.icons import ICONS
from cli.ui.style import PALETTE


def _icon_for(node: CommandNode) -> str:
    return getattr(ICONS, node.icon, "") if node.icon else ""


def _command_table(root: CommandNode) -> Table:
    table = Table(
        show_header=False,
        box=None,
        padding=(0, 1, 0, 0),
        collapse_padding=True,
    )
    table.add_column("cmd", style=f"bold {PALETTE.brand}", no_wrap=True, min_width=22)
    table.add_column("desc", style=PALETTE.text)

    icon = _icon_for(root)
    root_label = f"{icon} {root.name}".strip()
    table.add_row(root_label, root.description)

    for child in root.children.values():
        child_label = f"    {root.name} {child.name}"
        desc = child.description
        if child.aliases:
            desc = f"{desc}  [dim]({', '.join(child.aliases)})[/dim]"
        table.add_row(child_label, desc)

    return table


def build_help_panel() -> Panel:
    """Construye el panel de ayuda completo, agrupado por comando raíz."""
    sections: list[Text | Table] = []

    for root in COMMAND_TREE.values():
        if root.children:
            heading = Text(root.name.lstrip("/").capitalize(), style=f"bold {PALETTE.accent}")
            sections.append(heading)
            sections.append(_command_table(root))
            sections.append(Text(""))

    standalone = Table(show_header=False, box=None, padding=(0, 1, 0, 0))
    standalone.add_column("cmd", style=f"bold {PALETTE.brand}", no_wrap=True, min_width=22)
    standalone.add_column("desc", style=PALETTE.text)
    for root in COMMAND_TREE.values():
        if not root.children:
            icon = _icon_for(root)
            label = f"{icon} {root.name}".strip()
            standalone.add_row(label, root.description)

    sections.append(Text("General", style=f"bold {PALETTE.accent}"))
    sections.append(standalone)

    body = Padding(Group(*sections), (0, 1))
    return Panel(
        body,
        title="Comandos disponibles",
        title_align="left",
        border_style=PALETTE.subtle,
        padding=(1, 2),
    )


def print_help(console: Console) -> None:
    console.print()
    console.print(build_help_panel())
    console.print()