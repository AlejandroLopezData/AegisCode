"""Completer propio de AegisCode CLI.

No usa `NestedCompleter`. Recorre `cli/spec.COMMAND_TREE` a mano para
poder soportar tres cosas que `NestedCompleter` no da "gratis":

1. Fuzzy matching (p.ej. "/prov" -> "/providers", "rm" ya es alias).
2. Opciones dinámicas (p.ej. "/providers remove <tab>" listando
   proveedores reales vía `CommandNode.dynamic_options`).
3. Metadata (icono + descripción) en cada sugerencia.

Si `rapidfuzz` está instalado se usa para puntuar coincidencias;
si no, cae a un matching por subsecuencia simple sin dependencias.
"""

from __future__ import annotations

from collections.abc import Iterable

from prompt_toolkit.completion import Completion
from prompt_toolkit.completion import Completer as PTCompleter
from prompt_toolkit.document import Document

from cli.spec import COMMAND_TREE, CommandNode
from cli.ui.icons import ICONS

try:
    from rapidfuzz import fuzz

    _HAS_RAPIDFUZZ = True
except ImportError:  # pragma: no cover - rapidfuzz es opcional
    _HAS_RAPIDFUZZ = False


def _fuzzy_score(query: str, candidate: str) -> float:
    """Puntúa qué tan bien `query` coincide con `candidate` (0-100)."""
    if not query:
        return 100.0
    query_l, candidate_l = query.lower(), candidate.lower()

    if candidate_l.startswith(query_l):
        return 100.0

    if _HAS_RAPIDFUZZ:
        return float(fuzz.partial_ratio(query_l, candidate_l))

    # Fallback sin dependencias: matching por subsecuencia ordenada.
    it = iter(candidate_l)
    if all(ch in it for ch in query_l):
        return 60.0
    return 0.0


def _icon_for(node: CommandNode) -> str:
    icon_name = node.icon
    if not icon_name:
        return ""
    return getattr(ICONS, icon_name, "")


class AegisCompleter(PTCompleter):
    """Completer consciente de la gramática `/comando subcomando arg`."""

    def get_completions(
        self, document: Document, complete_event
    ) -> Iterable[Completion]:
        text_before_cursor = document.text_before_cursor
        words = text_before_cursor.split(" ")

        if len(words) == 1:
            yield from self._complete_root(words[0])
            return

        root_token = words[0]
        root_node = self._resolve_root(root_token)
        if root_node is None:
            return

        if len(words) == 2:
            yield from self._complete_child(root_node, words[1])
            return

        if len(words) == 3:
            child_token = words[1]
            child_node = self._resolve_child(root_node, child_token)
            if child_node is not None and child_node.dynamic_options is not None:
                yield from self._complete_dynamic(child_node, words[2])
            return

    def _resolve_root(self, token: str) -> CommandNode | None:
        for node in COMMAND_TREE.values():
            if token in node.all_names():
                return node
        return None

    def _resolve_child(self, node: CommandNode, token: str) -> CommandNode | None:
        for child in node.children.values():
            if token in child.all_names():
                return child
        return None

    def _complete_root(self, fragment: str) -> Iterable[Completion]:
        scored: list[tuple[float, CommandNode]] = []
        for node in COMMAND_TREE.values():
            best = max(_fuzzy_score(fragment, name) for name in node.all_names())
            if best > 0:
                scored.append((best, node))

        scored.sort(key=lambda pair: pair[0], reverse=True)

        for score, node in scored:
            icon = _icon_for(node)
            display = f"{icon} {node.name}".strip()
            meta = node.description
            if node.aliases:
                meta = f"{meta}  (alias: {', '.join(node.aliases)})"
            yield Completion(
                text=node.name,
                start_position=-len(fragment),
                display=display,
                display_meta=meta,
            )

    def _complete_child(self, root_node: CommandNode, fragment: str) -> Iterable[Completion]:
        if not root_node.children:
            return

        scored: list[tuple[float, CommandNode]] = []
        for child in root_node.children.values():
            best = max(_fuzzy_score(fragment, name) for name in child.all_names())
            if best > 0:
                scored.append((best, child))

        scored.sort(key=lambda pair: pair[0], reverse=True)

        for score, child in scored:
            meta = child.description
            if child.aliases:
                meta = f"{meta}  (alias: {', '.join(child.aliases)})"
            yield Completion(
                text=child.name,
                start_position=-len(fragment),
                display=child.name,
                display_meta=meta,
            )

    def _complete_dynamic(self, child_node: CommandNode, fragment: str) -> Iterable[Completion]:
        if child_node.dynamic_options is None:
            return

        try:
            options = child_node.dynamic_options()
        except Exception:  # noqa: BLE001 - un fallo del adapter no debe romper el completer
            options = []

        scored = [(_fuzzy_score(fragment, opt), opt) for opt in options]
        scored = [pair for pair in scored if pair[0] > 0]
        scored.sort(key=lambda pair: pair[0], reverse=True)

        for _score, option in scored:
            yield Completion(
                text=option,
                start_position=-len(fragment),
                display=option,
            )