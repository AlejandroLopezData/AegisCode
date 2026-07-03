#!/usr/bin/env python3
"""Entrypoint de AegisCode CLI.

Toda la lógica vive en `cli.app.AegisApp`. Este archivo solo prepara
el `sys.path` (para que `config/`, `runtime/`, etc. sean importables
como paquetes de nivel superior) y arranca la aplicación.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli.app import AegisApp


def main() -> None:
    AegisApp().run()


if __name__ == "__main__":
    main()