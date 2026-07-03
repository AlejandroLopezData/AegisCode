"""Paneles y tablas reutilizables de AegisCode CLI.

Agrupa toda la renderización "de dominio" (tablas de proveedores y
modelos) y los mensajes de estado genéricos (éxito/error/warning/info)
usados por los comandos. Los comandos nunca llaman a `console.print`
con strings sueltos: siempre pasan por aquí para mantener consistencia
visual.
"""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from cli.adapters.models import ModelInfo
from cli.adapters.providers import CatalogEntry, ProviderInfo
from cli.ui.icons import ICONS
from cli.ui.style import PALETTE, RICH_STYLES


def _empty_panel(message: str) -> Panel:
    return Panel(
        Text(message, style=f"dim {PALETTE.muted}"),
        border_style=PALETTE.subtle,
        padding=(1, 2),
    )


def providers_table(providers: list[ProviderInfo]) -> Table | Panel:
    """Tabla de proveedores ya enlazados."""
    if not providers:
        return _empty_panel(
            "No hay proveedores enlazados todavía. Usa /providers add para enlazar uno."
        )

    table = Table(
        title=f"{ICONS.provider} Proveedores enlazados",
        title_style=RICH_STYLES.TABLE_HEADER,
        header_style=RICH_STYLES.TABLE_HEADER,
        border_style=PALETTE.subtle,
        row_styles=["", f"on {PALETTE.surface_alt}"],
    )
    table.add_column("ID", style=PALETTE.text, no_wrap=True)
    table.add_column("Nombre", style=PALETTE.text)
    table.add_column("Estado", justify="center")
    table.add_column("Modelos", justify="right", style=PALETTE.muted)

    for provider in providers:
        status_style = RICH_STYLES.SUCCESS if provider.status == "linked" else RICH_STYLES.WARNING
        status_icon = ICONS.success if provider.status == "linked" else ICONS.warning
        table.add_row(
            provider.id,
            provider.name,
            Text(f"{status_icon} {provider.status}", style=status_style),
            str(provider.models_count),
        )

    return table


def catalog_table(entries: list[CatalogEntry]) -> Table | Panel:
    """Tabla del catálogo completo de proveedores disponibles."""
    if not entries:
        return _empty_panel("El catálogo de proveedores está vacío.")

    table = Table(
        title=f"{ICONS.provider} Catálogo de proveedores",
        title_style=RICH_STYLES.TABLE_HEADER,
        header_style=RICH_STYLES.TABLE_HEADER,
        border_style=PALETTE.subtle,
        row_styles=["", f"on {PALETTE.surface_alt}"],
    )
    table.add_column("ID", style=PALETTE.text, no_wrap=True)
    table.add_column("Nombre", style=PALETTE.text)
    table.add_column("Descripción", style=PALETTE.muted)

    for entry in entries:
        table.add_row(entry.id, entry.name, entry.description)

    return table


def models_table(models: list[ModelInfo]) -> Table | Panel:
    """Tabla de modelos añadidos."""
    if not models:
        return _empty_panel(
            "No hay modelos añadidos todavía. Usa /models add para añadir uno."
        )

    table = Table(
        title=f"{ICONS.model} Modelos",
        title_style=RICH_STYLES.TABLE_HEADER,
        header_style=RICH_STYLES.TABLE_HEADER,
        border_style=PALETTE.subtle,
        row_styles=["", f"on {PALETTE.surface_alt}"],
    )
    table.add_column("ID", style=PALETTE.text, no_wrap=True)
    table.add_column("Nombre", style=PALETTE.text)
    table.add_column("Proveedor", style=PALETTE.muted)
    table.add_column("Estado", justify="center")

    for model in models:
        status_style = RICH_STYLES.SUCCESS if model.status == "ready" else RICH_STYLES.WARNING
        status_icon = ICONS.success if model.status == "ready" else ICONS.warning
        table.add_row(
            model.id,
            model.name,
            model.provider_id or "-",
            Text(f"{status_icon} {model.status}", style=status_style),
        )

    return table


def print_success(console: Console, message: str) -> None:
    console.print(f"[{RICH_STYLES.SUCCESS}]{ICONS.success}[/{RICH_STYLES.SUCCESS}] {message}")


def print_error(console: Console, message: str) -> None:
    console.print(f"[{RICH_STYLES.ERROR}]{ICONS.error}[/{RICH_STYLES.ERROR}] {message}")


def print_warning(console: Console, message: str) -> None:
    console.print(f"[{RICH_STYLES.WARNING}]{ICONS.warning}[/{RICH_STYLES.WARNING}] {message}")


def print_info(console: Console, message: str) -> None:
    console.print(f"[{RICH_STYLES.INFO}]{ICONS.info}[/{RICH_STYLES.INFO}] {message}")