"""Schema, table and view resource client."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from .base import AIDPData, BaseResource, path_param


class SchemasResource(BaseResource):
    """Client for schemas, tables and views."""

    def list(
        self,
        params: Mapping[str, Any] | None = None,
        **query: Any,
    ) -> AIDPData:
        return self.list_schemas(params=params, **query)

    def list_iter(
        self,
        params: Mapping[str, Any] | None = None,
        *,
        item_key: str = "items",
        **query: Any,
    ) -> Iterable[Any]:
        return self.list_schemas_iter(params=params, item_key=item_key, **query)

    def create(self, details: Mapping[str, Any]) -> AIDPData:
        return self.create_schema(details)

    def get(self, schema_key: str) -> AIDPData:
        return self.get_schema(schema_key)

    def update(
        self,
        schema_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.update_schema(schema_key, details)

    def delete(self, schema_key: str) -> AIDPData:
        return self.delete_schema(schema_key)

    def list_schemas(
        self,
        params: Mapping[str, Any] | None = None,
        **query: Any,
    ) -> AIDPData:
        return self._list("/schemas", params=params, **query)

    def list_schemas_iter(
        self,
        params: Mapping[str, Any] | None = None,
        *,
        item_key: str = "items",
        **query: Any,
    ) -> Iterable[Any]:
        return self._list_iter("/schemas", params=params, item_key=item_key, **query)

    def create_schema(self, details: Mapping[str, Any]) -> AIDPData:
        return self._create("/schemas", details)

    def get_schema(self, schema_key: str) -> AIDPData:
        return self._get(f"/schemas/{path_param(schema_key)}")

    def update_schema(
        self,
        schema_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._update(f"/schemas/{path_param(schema_key)}", details)

    def delete_schema(self, schema_key: str) -> AIDPData:
        return self._delete(f"/schemas/{path_param(schema_key)}")

    def schema_permissions(self, schema_key: str) -> AIDPData:
        return self._get(f"/schemas/{path_param(schema_key)}/permissions")

    def manage_schema_permissions(
        self,
        schema_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._action(f"/schemas/{path_param(schema_key)}/actions/managePermission", details)

    def refresh_schema(
        self,
        schema_key: str,
        details: Mapping[str, Any] | None = None,
    ) -> AIDPData:
        return self._action(f"/schemas/{path_param(schema_key)}/actions/refresh", details)

    def infer_schema(
        self,
        schema_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._action(f"/schemas/{path_param(schema_key)}/actions/inferSchema", details)

    def infer_schema_with_preview(
        self,
        schema_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._action(
            f"/schemas/{path_param(schema_key)}/actions/inferSchemaWithPreview",
            details,
        )

    def generate_temp_file_upload_target(
        self,
        schema_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._action(
            f"/schemas/{path_param(schema_key)}/actions/generateTempFileUploadTarget",
            details,
        )

    def list_tables(
        self,
        params: Mapping[str, Any] | None = None,
        **query: Any,
    ) -> AIDPData:
        return self._list("/tables", params=params, **query)

    def list_tables_iter(
        self,
        params: Mapping[str, Any] | None = None,
        *,
        item_key: str = "items",
        **query: Any,
    ) -> Iterable[Any]:
        return self._list_iter("/tables", params=params, item_key=item_key, **query)

    def create_table(self, details: Mapping[str, Any]) -> AIDPData:
        return self._create("/tables", details)

    def create_managed_table_from_sample_file(
        self,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._create("/dataTables", details)

    def get_table(self, table_key: str) -> AIDPData:
        return self._get(f"/tables/{path_param(table_key)}")

    def update_table(
        self,
        table_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._update(f"/tables/{path_param(table_key)}", details)

    def delete_table(self, table_key: str) -> AIDPData:
        return self._delete(f"/tables/{path_param(table_key)}")

    def table_permissions(self, table_key: str) -> AIDPData:
        return self._get(f"/tables/{path_param(table_key)}/permissions")

    def manage_table_permissions(
        self,
        table_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._action(f"/tables/{path_param(table_key)}/actions/managePermission", details)

    def refresh_table(
        self,
        table_key: str,
        details: Mapping[str, Any] | None = None,
    ) -> AIDPData:
        return self._action(f"/tables/{path_param(table_key)}/actions/refresh", details)

    def get_table_par(
        self,
        table_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._action(f"/tables/{path_param(table_key)}/actions/getPar", details)

    def list_views(
        self,
        params: Mapping[str, Any] | None = None,
        **query: Any,
    ) -> AIDPData:
        return self._list("/views", params=params, **query)

    def list_views_iter(
        self,
        params: Mapping[str, Any] | None = None,
        *,
        item_key: str = "items",
        **query: Any,
    ) -> Iterable[Any]:
        return self._list_iter("/views", params=params, item_key=item_key, **query)

    def create_view(self, details: Mapping[str, Any]) -> AIDPData:
        return self._create("/views", details)

    def get_view(self, view_key: str) -> AIDPData:
        return self._get(f"/views/{path_param(view_key)}")

    def update_view(
        self,
        view_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._update(f"/views/{path_param(view_key)}", details)

    def delete_view(self, view_key: str) -> AIDPData:
        return self._delete(f"/views/{path_param(view_key)}")

    def view_permissions(self, view_key: str) -> AIDPData:
        return self._get(f"/views/{path_param(view_key)}/permissions")

    def manage_view_permissions(
        self,
        view_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._action(f"/views/{path_param(view_key)}/actions/managePermission", details)
