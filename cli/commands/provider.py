"""Comando `/providers` de AegisCode CLI.

Subcomandos soportados (ya resueltos de alias por `CommandRegistry`):

- (ninguno)  -> muestra el catálogo de proveedores disponibles.
- "list"     -> muestra los proveedores ya enlazados.
- "add"      -> enlaza un proveedor del catálogo.
- "remove"   -> elimina un proveedor enlazado.
"""

from __future__ import annotations

from rich.console import Console

from cli.adapters.providers import (
    ProvidersAdapterError,
    link_provider,
    list_catalog,
    list_linked_providers,
    remove_provider,
)
from cli.commands.base import Command
from cli.ui.panels import (
    catalog_table,
    print_error,
    print_success,
    print_warning,
    providers_table,
)


class ProvidersCommand(Command):
    """Implementación de `/providers` y sus subcomandos."""

    def execute(self, subcommand: str | None, args: list[str], console: Console) -> None:
        try:
            if subcommand is None:
                self._show_catalog(console)
            elif subcommand == "list":
                self._show_linked(console)
            elif subcommand == "add":
                self._add(args, console)
            elif subcommand == "remove":
                self._remove(args, console)
            else:  # pragma: no cover - defensivo, registry ya valida
                print_warning(console, f"Subcomando desconocido: {subcommand}")
        except ProvidersAdapterError as exc:
            print_error(console, str(exc))

    def _show_catalog(self, console: Console) -> None:
        console.print(catalog_table(list_catalog()))

    def _show_linked(self, console: Console) -> None:
        console.print(providers_table(list_linked_providers()))

    def _add(self, args: list[str], console: Console) -> None:
        if not args:
            print_warning(console, "Uso: /providers add <id-del-catalogo>")
            return

        catalog_id = args[0]
        provider = link_provider(catalog_id)
        print_success(console, f"Proveedor '{provider.name}' enlazado correctamente.")

    def _remove(self, args: list[str], console: Console) -> None:
        if not args:
            print_warning(console, "Uso: /providers remove <id>")
            return

        provider_id = args[0]
        if remove_provider(provider_id):
            print_success(console, f"Proveedor '{provider_id}' eliminado.")
        else:
            print_error(console, f"No se pudo eliminar el proveedor '{provider_id}'.")