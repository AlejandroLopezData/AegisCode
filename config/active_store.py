"""
config/active_store.py

Guarda cuál es el modelo activo ahora mismo (uno solo). Es un archivo
aparte y muy pequeño a propósito: es un puntero, no una lista.

De momento solo expone get/set del ID del modelo. El proveedor
correspondiente se resuelve consultando models_store + providers_store,
no se duplica aquí.
"""

import os
from pathlib import Path

import yaml

CONFIG_DIR = Path(os.path.expanduser("~/.config/aegis"))
ACTIVE_PATH = CONFIG_DIR / "active.yaml"


def _ensure_config_dir():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def get_active_model_id() -> str | None:
    if not ACTIVE_PATH.exists():
        return None
    with open(ACTIVE_PATH) as f:
        raw = yaml.safe_load(f) or {}
    return raw.get("model_id")


def set_active_model_id(model_id: str) -> None:
    _ensure_config_dir()
    with open(ACTIVE_PATH, "w") as f:
        yaml.safe_dump({"model_id": model_id}, f)