"""Construcción del `PromptSession` de AegisCode CLI.

Centraliza el ensamblado de: prompt visual (`Aegis ❯`), historial
persistente en `~/.aegis/history`, completer propio, lexer propio,
estilo y toolbar inferior. `app.py` solo llama a `build_session()`.
"""

from __future__ import annotations

from pathlib import Path

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import ThreadedCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.lexers import Lexer as PTLexer

from cli.ui.completer import AegisCompleter
from cli.ui.icons import ICONS
from cli.ui.lexer import CommandLexer
from cli.ui.style import PROMPT_TOOLKIT_STYLE

HISTORY_DIR = Path.home() / ".aegis"
HISTORY_FILE = HISTORY_DIR / "history"

PROMPT_MESSAGE = [
    ("class:prompt.brand", "Aegis"),
    ("", " "),
    ("class:prompt.arrow", ICONS.arrow),
    ("", " "),
]


def _ensure_history_file() -> FileHistory:
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    HISTORY_FILE.touch(exist_ok=True)
    return FileHistory(str(HISTORY_FILE))


def build_session() -> PromptSession:
    """Construye el `PromptSession` completamente configurado."""
    lexer: PTLexer = CommandLexer()

    return PromptSession(
        message=PROMPT_MESSAGE,
        completer=ThreadedCompleter(AegisCompleter()),
        complete_while_typing=True,
        lexer=lexer,
        style=PROMPT_TOOLKIT_STYLE,
        history=_ensure_history_file(),
    )