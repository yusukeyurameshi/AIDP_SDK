"""Workspace resource client."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from .base import AIDPData, BaseResource, path_param


class WorkspacesResource(BaseResource):
    """Client for workspace operations."""

    def list(
        self,
        params: Mapping[str, Any] | None = None,
        **query: Any,
    ) -> AIDPData:
        return self._list("/workspaces", params=params, **query)

    def list_iter(
        self,
        params: Mapping[str, Any] | None = None,
        *,
        item_key: str = "items",
        **query: Any,
    ) -> Iterable[Any]:
        return self._list_iter("/workspaces", params=params, item_key=item_key, **query)

    def create(self, details: Mapping[str, Any]) -> AIDPData:
        return self._create("/workspaces", details)

    def get(self, workspace_key: str) -> AIDPData:
        return self._get(f"/workspaces/{path_param(workspace_key)}")

    def update(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._update(f"/workspaces/{path_param(workspace_key)}", details)

    def delete(self, workspace_key: str) -> AIDPData:
        return self._delete(f"/workspaces/{path_param(workspace_key)}")

    def permissions(self, workspace_key: str) -> AIDPData:
        return self._get(f"/workspaces/{path_param(workspace_key)}/permissions")

    def manage_permissions(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._action(
            f"/workspaces/{path_param(workspace_key)}/actions/managePermission",
            details,
        )

    def list_create_permissions(self) -> AIDPData:
        return self._get("/createWorkspacePermissions")

    def manage_create_workspace_permission(
        self,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._action("/actions/manageCreateWorkspacePermission", details)

    def create_git_folder(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._create(f"/workspaces/{path_param(workspace_key)}/gitFolders", details)

    def update_status(
        self,
        workspace_key: str,
        async_operation_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._update(
            "/workspaces/"
            f"{path_param(workspace_key)}/asyncOperations/"
            f"{path_param(async_operation_key)}/status",
            details,
        )
