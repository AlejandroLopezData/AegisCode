"""Aplicación principal de AegisCode CLI.

`AegisApp` es la única clase que orquesta: `PromptSession`, el
`CommandRegistry`, el banner de bienvenida y el loop de lectura de
entrada. `main.py` solo instancia y llama a `run()`.
"""

from __future__ import annotations

from rich.console import Console

from cli.commands.models import ModelsCommand
from cli.commands.provider import ProvidersCommand
from cli.commands.registry import CommandRegistry
from cli.ui.banner import print_banner
from cli.ui.prompt import build_session


class AegisApp:
    """Aplicación de línea de comandos de AegisCode."""

    def __init__(self) -> None:
        self.console = Console()
        self.session = build_session()
        self.registry = CommandRegistry()
        self._register_commands()

    def _register_commands(self) -> None:
        self.registry.register("/providers", ProvidersCommand())
        self.registry.register("/models", ModelsCommand())

    def run(self) -> None:
        """Punto de entrada del loop principal de la aplicación."""
        print_banner(self.console)

        while True:
            try:
                raw_input_text = self.session.prompt()
            except KeyboardInterrupt:
                continue
            except EOFError:
                self._print_goodbye()
                break

            should_continue = self.registry.dispatch(raw_input_text, self.console)
            if not should_continue:
                self._print_goodbye()
                break

    def _print_goodbye(self) -> None:
        self.console.print("\n[dim]bye.[/dim]")