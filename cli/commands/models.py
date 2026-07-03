"""Comando `/models` de AegisCode CLI.

Subcomandos soportados (ya resueltos de alias por `CommandRegistry`):

- (ninguno) / "list" -> muestra todos los modelos añadidos.
- "add"               -> añade un modelo a un proveedor enlazado.
- "remove"            -> elimina un modelo.
"""

from __future__ import annotations

from rich.console import Console

from cli.adapters.models import ModelsAdapterError, add_model, list_models, remove_model
from cli.commands.base import Command
from cli.ui.panels import models_table, print_error, print_success, print_warning


class ModelsCommand(Command):
    """Implementación de `/models` y sus subcomandos."""

    def execute(self, subcommand: str | None, args: list[str], console: Console) -> None:
        # `/models` sin subcomando se comporta igual que `/models list`,
        # igual que en la CLI original.
        effective = subcommand or "list"

        try:
            if effective == "list":
                self._show_list(console)
            elif effective == "add":
                self._add(args, console)
            elif effective == "remove":
                self._remove(args, console)
            else:  # pragma: no cover - defensivo, registry ya valida
                print_warning(console, f"Subcomando desconocido: {effective}")
        except ModelsAdapterError as exc:
            print_error(console, str(exc))

    def _show_list(self, console: Console) -> None:
        console.print(models_table(list_models()))

    def _add(self, args: list[str], console: Console) -> None:
        if len(args) < 2:
            print_warning(console, "Uso: /models add <provider_id> <model_name>")
            return

        provider_id, model_name = args[0], " ".join(args[1:])
        model = add_model(provider_id, model_name)
        print_success(console, f"Modelo '{model.name}' añadido a '{provider_id}'.")

    def _remove(self, args: list[str], console: Console) -> None:
        if not args:
            print_warning(console, "Uso: /models remove <id>")
            return

        model_id = args[0]
        if remove_model(model_id):
            print_success(console, f"Modelo '{model_id}' eliminado.")
        else:
            print_error(console, f"No se pudo eliminar el modelo '{model_id}'.")