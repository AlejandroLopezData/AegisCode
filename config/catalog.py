"""
config/catalog.py

Lee el catálogo de tipos de proveedor soportados (config/providers_catalog.yaml).
Esto NO es config del usuario: es información fija que define qué tipos de
proveedor existen y qué campos hay que pedir para cada uno. Añadir un tipo
nuevo (ej. "azure_openai") es editar este YAML, no tocar código.
"""

from pathlib import Path

import yaml

CATALOG_PATH = Path(__file__).parent / "providers_catalog.yaml"


def load_catalog() -> list[dict]:
    with open(CATALOG_PATH) as f:
        raw = yaml.safe_load(f) or {}
    return raw.get("providers", [])


def find_catalog_entry(provider_type: str) -> dict | None:
    return next((p for p in load_catalog() if p["type"] == provider_type), None)