"""Catalog resource client."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from .base import AIDPData, BaseResource, path_param


class CatalogsResource(BaseResource):
    """Client for catalog operations."""

    def list(
        self,
        params: Mapping[str, Any] | None = None,
        **query: Any,
    ) -> AIDPData:
        return self._list("/catalogs", params=params, **query)

    def list_iter(
        self,
        params: Mapping[str, Any] | None = None,
        *,
        item_key: str = "items",
        **query: Any,
    ) -> Iterable[Any]:
        return self._list_iter("/catalogs", params=params, item_key=item_key, **query)

    def create(self, details: Mapping[str, Any]) -> AIDPData:
        return self._create("/catalogs", details)

    def get(self, catalog_key: str) -> AIDPData:
        return self._get(f"/catalogs/{path_param(catalog_key)}")

    def update(
        self,
        catalog_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._update(f"/catalogs/{path_param(catalog_key)}", details)

    def delete(self, catalog_key: str) -> AIDPData:
        return self._delete(f"/catalogs/{path_param(catalog_key)}")

    def permissions(self, catalog_key: str) -> AIDPData:
        return self._get(f"/catalogs/{path_param(catalog_key)}/permissions")

    def manage_permissions(
        self,
        catalog_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._action(
            f"/catalogs/{path_param(catalog_key)}/actions/managePermission",
            details,
        )

    def refresh(
        self,
        catalog_key: str,
        details: Mapping[str, Any] | None = None,
    ) -> AIDPData:
        return self._action(f"/catalogs/{path_param(catalog_key)}/actions/refresh", details)

    def test_connection(
        self,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._action("/actions/testConnection", details)
