"""Árbol de comandos único de AegisCode CLI.

Esta es la ÚNICA fuente de verdad sobre qué comandos existen, sus
alias, descripciones y de dónde sacan sus opciones dinámicas
(p.ej. `/providers remove <tab>` listando proveedores reales).

`ui/completer.py`, `ui/lexer.py`, `ui/help.py` y `commands/registry.py`
leen todos de aquí. Añadir un comando nuevo solo requiere editar
`COMMAND_TREE` en este archivo.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from cli.adapters.models import model_names
from cli.adapters.providers import catalog_names, provider_names


@dataclass(frozen=True, slots=True)
class CommandNode:
    """Un nodo del árbol de comandos: comando, subcomando o acción hoja."""

    name: str
    description: str
    icon: str = ""
    aliases: tuple[str, ...] = field(default_factory=tuple)
    children: dict[str, "CommandNode"] = field(default_factory=dict)
    # Callback que produce opciones dinámicas (p.ej. proveedores enlazados)
    # para autocompletar el argumento de este nodo. None si no aplica.
    dynamic_options: Callable[[], list[str]] | None = None

    def all_names(self) -> tuple[str, ...]:
        """Nombre canónico + alias, útil para matching y lexer."""
        return (self.name, *self.aliases)


def _leaf(name: str, description: str, icon: str = "", aliases: tuple[str, ...] = ()) -> CommandNode:
    return CommandNode(name=name, description=description, icon=icon, aliases=aliases)


COMMAND_TREE: dict[str, CommandNode] = {
    "/providers": CommandNode(
        name="/providers",
        description="Ver catálogo y enlazar un proveedor nuevo",
        icon="provider",
        aliases=("/p",),
        children={
            "list": _leaf("list", "Ver proveedores ya enlazados", aliases=("ls",)),
            "remove": CommandNode(
                name="remove",
                description="Eliminar un proveedor enlazado",
                aliases=("rm", "del"),
                dynamic_options=provider_names,
            ),
            "add": CommandNode(
                name="add",
                description="Enlazar un proveedor del catálogo",
                aliases=("link",),
                dynamic_options=catalog_names,
            ),
        },
    ),
    "/models": CommandNode(
        name="/models",
        description="Ver todos los modelos añadidos",
        icon="model",
        aliases=("/m",),
        children={
            "list": _leaf("list", "Ver todos los modelos añadidos", aliases=("ls",)),
            "add": CommandNode(
                name="add",
                description="Añadir un modelo a un proveedor enlazado",
                dynamic_options=provider_names,
            ),
            "remove": CommandNode(
                name="remove",
                description="Eliminar un modelo",
                aliases=("rm", "del"),
                dynamic_options=model_names,
            ),
        },
    ),
    "/help": _leaf("/help", "Mostrar la ayuda", icon="help", aliases=("/?", "?")),
    "exit": _leaf("exit", "Salir de la CLI", aliases=("quit", "salir", "q")),
}


def all_root_names() -> set[str]:
    """Todos los nombres/alias de comandos raíz — usado por el lexer."""
    names: set[str] = set()
    for node in COMMAND_TREE.values():
        names.update(node.all_names())
    return names


def resolve_root(token: str) -> CommandNode | None:
    """Resuelve un token (comando o alias) al CommandNode raíz correspondiente."""
    for node in COMMAND_TREE.values():
        if token in node.all_names():
            return node
    return None


def resolve_child(node: CommandNode, token: str) -> CommandNode | None:
    """Resuelve un token (subcomando o alias) a un hijo de `node`."""
    for child in node.children.values():
        if token in child.all_names():
            return child
    return None