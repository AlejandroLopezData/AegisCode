"""Interfaz base de los comandos de AegisCode CLI.

Cada comando raíz (`/providers`, `/models`, ...) implementa `Command`.
El `CommandRegistry` ya resolvió alias y subcomando canónico antes de
llamar a `execute`, así que un `Command` nunca necesita saber sobre
`ls`/`rm`/`del`: solo ve el nombre canónico (`"list"`, `"remove"`, ...).
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from rich.console import Console


class Command(ABC):
    """Contrato que implementa cada comando raíz de la CLI."""

    @abstractmethod
    def execute(
        self,
        subcommand: str | None,
        args: list[str],
        console: Console,
    ) -> None:
        """Ejecuta el comando.

        Args:
            subcommand: nombre canónico del subcomando (ya resuelto de
                alias), o None si se invocó el comando raíz sin args.
            args: argumentos restantes tras el subcommand.
            console: consola Rich donde renderizar la salida.
        """
        raise NotImplementedError