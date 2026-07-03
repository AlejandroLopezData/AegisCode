"""Adapter sobre `config.models_store`.

Igual que `adapters/providers.py`: es la única frontera entre la CLI
y `config.models_store`. Si las firmas reales difieren de lo asumido
(marcado con `# ASSUMPTION`), solo hay que editar este archivo.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ModelInfo:
    """Representación normalizada de un modelo añadido."""

    id: str
    name: str
    provider_id: str = ""
    status: str = "ready"


class ModelsAdapterError(RuntimeError):
    """Error al comunicarse con la capa de configuración de modelos."""


def list_models() -> list[ModelInfo]:
    """Devuelve todos los modelos añadidos."""
    try:
        from config.models_store import list_models as _list_models  # ASSUMPTION
    except ImportError as exc:  # pragma: no cover - guía de integración
        raise ModelsAdapterError(
            "No se pudo importar `list_models` desde "
            "`config.models_store`. Ajusta `adapters/models.py` "
            "con el nombre real de la función."
        ) from exc

    raw = _list_models()
    return [
        ModelInfo(
            id=str(item.get("id", item.get("name", ""))),
            name=str(item.get("name", item.get("id", "desconocido"))),
            provider_id=str(item.get("provider_id", item.get("provider", ""))),
            status=str(item.get("status", "ready")),
        )
        for item in raw
    ]


def add_model(provider_id: str, model_name: str) -> ModelInfo:
    """Añade un modelo a un proveedor enlazado."""
    try:
        from config.models_store import add_model as _add_model  # ASSUMPTION
    except ImportError as exc:  # pragma: no cover - guía de integración
        raise ModelsAdapterError(
            "No se pudo importar `add_model` desde `config.models_store`. "
            "Ajusta `adapters/models.py` con el nombre real de la función."
        ) from exc

    result = _add_model(provider_id, model_name)
    return ModelInfo(
        id=str(result.get("id", model_name)),
        name=str(result.get("name", model_name)),
        provider_id=str(result.get("provider_id", provider_id)),
        status=str(result.get("status", "ready")),
    )


def remove_model(model_id: str) -> bool:
    """Elimina un modelo. Devuelve True si se eliminó."""
    try:
        from config.models_store import remove_model as _remove  # ASSUMPTION
    except ImportError as exc:  # pragma: no cover - guía de integración
        raise ModelsAdapterError(
            "No se pudo importar `remove_model` desde "
            "`config.models_store`. Ajusta `adapters/models.py` "
            "con el nombre real de la función."
        ) from exc

    return bool(_remove(model_id))


def model_names() -> list[str]:
    """Nombres/IDs de modelos, usados por el completer dinámico."""
    return [m.id for m in list_models()]