"""
config/providers_store.py

Lee y escribe SOLO la config de proveedores enlazados (conexión: host,
puerto, url_base, api_key_env...). No sabe nada de modelos.
"""

import os
from pathlib import Path

import yaml

from core.types import ProvidersConfig, Provider

CONFIG_DIR = Path(os.path.expanduser("~/.config/aegis"))
PROVIDERS_PATH = CONFIG_DIR / "providers.yaml"


def _ensure_config_dir():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_providers() -> ProvidersConfig:
    if not PROVIDERS_PATH.exists():
        return ProvidersConfig(providers=[])

    with open(PROVIDERS_PATH) as f:
        raw = yaml.safe_load(f) or {}

    providers = [
        Provider(name=p["name"], type=p["type"], params=p.get("params", {}))
        for p in raw.get("providers", [])
    ]
    return ProvidersConfig(providers=providers)


def save_providers(config: ProvidersConfig):
    _ensure_config_dir()
    raw = {
        "providers": [
            {"name": p.name, "type": p.type, "params": p.params}
            for p in config.providers
        ]
    }
    with open(PROVIDERS_PATH, "w") as f:
        yaml.safe_dump(raw, f, sort_keys=False, allow_unicode=True)


def find_provider(config: ProvidersConfig, name: str) -> Provider | None:
    return next((p for p in config.providers if p.name == name), None)