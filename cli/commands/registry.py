"""Registro y dispatcher de comandos de AegisCode CLI.

`CommandRegistry` es la única pieza que conoce cómo pasar de texto
crudo escrito por el usuario a una llamada a `Command.execute`. Usa
`cli.spec` para resolver comando raíz y subcomando (incluyendo alias),
así que ningún `Command` concreto necesita lógica de parsing.
"""

from __future__ import annotations

from rich.console import Console

from cli.commands.base import Command
from cli.spec import resolve_child, resolve_root
from cli.ui.help import print_help
from cli.ui.panels import print_warning


class CommandRegistry:
    """Registra comandos raíz y despacha la entrada del usuario hacia ellos."""

    def __init__(self) -> None:
        self._commands: dict[str, Command] = {}

    def register(self, root_name: str, command: Command) -> None:
        """Asocia un comando raíz (p.ej. "/providers") a su implementación."""
        self._commands[root_name] = command

    def dispatch(self, raw_input: str, console: Console) -> bool:
        """Procesa una línea de entrada del usuario.

        Devuelve False si el loop principal de la aplicación debe
        terminar (comando `exit`), True en cualquier otro caso.
        """
        text = raw_input.strip()
        if not text:
            return True

        parts = text.split()
        first_token = parts[0]

        if text == "/":
            print_help(console)
            return True

        root_node = resolve_root(first_token)
        if root_node is None:
            print_warning(
                console,
                f"Comando desconocido: {first_token}. "
                "Usa /help para ver los comandos disponibles.",
            )
            return True

        if root_node.name == "exit":
            return False

        if root_node.name == "/help":
            print_help(console)
            return True

        command = self._commands.get(root_node.name)
        if command is None:
            print_warning(console, f"El comando {root_node.name} no está registrado todavía.")
            return True

        args = parts[1:]
        subcommand: str | None = None
        rest: list[str] = args

        if args and root_node.children:
            child_node = resolve_child(root_node, args[0])
            if child_node is not None:
                subcommand = child_node.name
                rest = args[1:]
            else:
                print_warning(
                    console,
                    f"Subcomando desconocido: {args[0]}. "
                    f"Usa /help para ver las opciones de {root_node.name}.",
                )
                return True

        command.execute(subcommand, rest, console)
        return True