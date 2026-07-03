"""Lexer de la línea de comandos de AegisCode CLI.

Colorea la entrada del usuario mientras escribe: comando raíz,
subcomando, flags (`--foo`), strings entre comillas y argumentos
sueltos. No depende de Pygments: es un tokenizador ligero a medida,
suficiente para la gramática simple de esta CLI (`/comando sub arg`).
"""

from __future__ import annotations

import re
from collections.abc import Callable

from prompt_toolkit.document import Document
from prompt_toolkit.lexers import Lexer

from cli.spec import all_root_names
from cli.ui.style import PALETTE

_TOKEN_PATTERN = re.compile(
    r"""
    (?P<string>"[^"]*"|'[^']*')   |
    (?P<flag>--?[A-Za-z][\w-]*)   |
    (?P<word>[^\s]+)
    """,
    re.VERBOSE,
)


class CommandLexer(Lexer):
    """Lexer consciente de la gramática `/comando subcomando args...`.

    Recibe un `command_names` callback para saber qué primera palabra
    cuenta como "comando" (y así distinguirla de un subcomando o un
    argumento libre) sin acoplarse a un árbol de comandos concreto.
    """

    def __init__(self, known_commands: Callable[[], set[str]] = all_root_names) -> None:
        self._known_commands = known_commands

    def lex_document(self, document: Document) -> Callable[[int], list[tuple[str, str]]]:
        lines = document.lines

        def get_line(line_number: int) -> list[tuple[str, str]]:
            if line_number >= len(lines):
                return []
            return self._tokenize_line(lines[line_number])

        return get_line

    def _tokenize_line(self, line: str) -> list[tuple[str, str]]:
        tokens: list[tuple[str, str]] = []
        commands = self._known_commands()
        word_index = 0
        pos = 0

        for match in _TOKEN_PATTERN.finditer(line):
            start, end = match.span()
            if start > pos:
                tokens.append(("", line[pos:start]))

            text = match.group()
            kind = match.lastgroup

            if kind == "string":
                tokens.append((f"fg:{PALETTE.syntax_string}", text))
            elif kind == "flag":
                tokens.append((f"fg:{PALETTE.syntax_flag}", text))
            elif kind == "word":
                if word_index == 0 and text in commands:
                    tokens.append((f"fg:{PALETTE.syntax_command} bold", text))
                elif word_index == 1:
                    tokens.append((f"fg:{PALETTE.syntax_subcommand}", text))
                else:
                    tokens.append((f"fg:{PALETTE.syntax_argument}", text))
                word_index += 1
            else:  # pragma: no cover - defensivo
                tokens.append(("", text))

            pos = end

        if pos < len(line):
            tokens.append(("", line[pos:]))

        return tokens or [("", line)]