"""
config/models_store.py

Lee y escribe SOLO la config de modelos (models.yaml). Cada modelo
referencia un proveedor por su nombre, pero este archivo no sabe nada
de cómo conectar a ese proveedor — eso vive en providers.yaml.
"""

import os
from pathlib import Path

import yaml

from core.types import ModelsConfig, Model

CONFIG_DIR = Path(os.path.expanduser("~/.config/aegis"))
MODELS_PATH = CONFIG_DIR / "models.yaml"


def _ensure_config_dir():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_models() -> ModelsConfig:
    if not MODELS_PATH.exists():
        return ModelsConfig(models=[])

    with open(MODELS_PATH) as f:
        raw = yaml.safe_load(f) or {}

    models = [
        Model(id=m["id"], provider=m["provider"])
        for m in raw.get("models", [])
    ]
    return ModelsConfig(models=models)


def save_models(config: ModelsConfig):
    _ensure_config_dir()
    raw = {
        "models": [
            {"id": m.id, "provider": m.provider}
            for m in config.models
        ]
    }
    with open(MODELS_PATH, "w") as f:
        yaml.safe_dump(raw, f, sort_keys=False, allow_unicode=True)


def models_by_provider(config: ModelsConfig, provider_name: str) -> list[Model]:
    return [m for m in config.models if m.provider == provider_name]