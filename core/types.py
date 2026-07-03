"""
core/types.py

Tipos de datos compartidos entre módulos. Aquí NO va lógica de negocio.
"""

from dataclasses import dataclass, field


@dataclass
class Provider:
    """
    Un proveedor de inferencia enlazado por el usuario. Solo datos de
    conexión — los modelos NO viven aquí, viven en models.yaml.

    'type' debe existir en el catálogo (config/providers_catalog.yaml).
    'params' guarda los valores que ese tipo pide (host/puerto, url_base,
    api_key_env...), definidos por el catálogo.
    """
    name: str
    type: str
    params: dict[str, str] = field(default_factory=dict)


@dataclass
class ProvidersConfig:
    providers: list[Provider] = field(default_factory=list)


@dataclass
class Model:
    """Un modelo concreto, enlazado a un proveedor por su nombre."""
    id: str            # identificador que usa el proveedor (ej. "qwen2.5-coder:7b")
    provider: str       # nombre del Provider al que pertenece (ej. "ollama_local")


@dataclass
class ModelsConfig:
    models: list[Model] = field(default_factory=list)