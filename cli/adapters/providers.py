"""Adapter sobre `config.providers_store` y `config.catalog`.

Este módulo es la ÚNICA frontera entre la CLI y la capa de
configuración real del proyecto. El resto de `cli/` nunca importa
`config.*` directamente: solo conoce `ProviderInfo`, `CatalogEntry` y
las funciones de este archivo.

Si las firmas reales de `config.providers_store` / `config.catalog`
difieren de lo asumido aquí (marcado con `# ASSUMPTION`), basta con
editar el cuerpo de las funciones de abajo — el resto de la CLI no
se ve afectado.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProviderInfo:
    """Representación normalizada de un proveedor ya enlazado."""

    id: str
    name: str
    status: str = "linked"
    models_count: int = 0


@dataclass(frozen=True, slots=True)
class CatalogEntry:
    """Representación normalizada de una entrada del catálogo de proveedores."""

    id: str
    name: str
    description: str = ""


class ProvidersAdapterError(RuntimeError):
    """Error al comunicarse con la capa de configuración de proveedores."""


def list_linked_providers() -> list[ProviderInfo]:
    """Devuelve los proveedores ya enlazados por el usuario."""
    try:
        from config.providers_store import list_providers  # ASSUMPTION
    except ImportError as exc:  # pragma: no cover - guía de integración
        raise ProvidersAdapterError(
            "No se pudo importar `list_providers` desde "
            "`config.providers_store`. Ajusta `adapters/providers.py` "
            "con el nombre real de la función."
        ) from exc

    raw = list_providers()
    return [
        ProviderInfo(
            id=str(item.get("id", item.get("name", ""))),
            name=str(item.get("name", item.get("id", "desconocido"))),
            status=str(item.get("status", "linked")),
            models_count=int(item.get("models_count", 0)),
        )
        for item in raw
    ]


def list_catalog() -> list[CatalogEntry]:
    """Devuelve el catálogo completo de proveedores disponibles para enlazar."""
    try:
        from config.catalog import list_catalog as _list_catalog  # ASSUMPTION
    except ImportError as exc:  # pragma: no cover - guía de integración
        raise ProvidersAdapterError(
            "No se pudo importar `list_catalog` desde `config.catalog`. "
            "Ajusta `adapters/providers.py` con el nombre real de la función."
        ) from exc

    raw = _list_catalog()
    return [
        CatalogEntry(
            id=str(item.get("id", item.get("name", ""))),
            name=str(item.get("name", item.get("id", "desconocido"))),
            description=str(item.get("description", "")),
        )
        for item in raw
    ]


def remove_provider(provider_id: str) -> bool:
    """Elimina un proveedor enlazado. Devuelve True si se eliminó."""
    try:
        from config.providers_store import remove_provider as _remove  # ASSUMPTION
    except ImportError as exc:  # pragma: no cover - guía de integración
        raise ProvidersAdapterError(
            "No se pudo importar `remove_provider` desde "
            "`config.providers_store`. Ajusta `adapters/providers.py` "
            "con el nombre real de la función."
        ) from exc

    return bool(_remove(provider_id))


def link_provider(catalog_id: str) -> ProviderInfo:
    """Enlaza un proveedor del catálogo. Devuelve el ProviderInfo resultante."""
    try:
        from config.providers_store import link_provider as _link  # ASSUMPTION
    except ImportError as exc:  # pragma: no cover - guía de integración
        raise ProvidersAdapterError(
            "No se pudo importar `link_provider` desde "
            "`config.providers_store`. Ajusta `adapters/providers.py` "
            "con el nombre real de la función."
        ) from exc

    result = _link(catalog_id)
    return ProviderInfo(
        id=str(result.get("id", catalog_id)),
        name=str(result.get("name", catalog_id)),
        status=str(result.get("status", "linked")),
        models_count=int(result.get("models_count", 0)),
    )


def provider_names() -> list[str]:
    """Nombres/IDs de proveedores enlazados, usados por el completer dinámico."""
    return [p.id for p in list_linked_providers()]


def catalog_names() -> list[str]:
    """Nombres/IDs del catálogo, usados por el completer dinámico."""
    return [c.id for c in list_catalog()]