"""Notebook resource client."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .base import AIDPData, BaseResource, path_param


class NotebooksResource(BaseResource):
    """Client for notebook contents and sessions."""

    def get_content(
        self,
        workspace_key: str,
        content_path: str = "",
        params: Mapping[str, Any] | None = None,
        **query: Any,
    ) -> AIDPData:
        return self._get(
            self._content_path(workspace_key, content_path),
            params=params,
            **query,
        )

    def create_content(
        self,
        workspace_key: str,
        content_path: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._create(self._content_path(workspace_key, content_path), details)

    def update_content(
        self,
        workspace_key: str,
        content_path: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._update(self._content_path(workspace_key, content_path), details)

    def patch_content(
        self,
        workspace_key: str,
        content_path: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._update(
            self._content_path(workspace_key, content_path),
            details,
            method="PATCH",
        )

    def delete_content(
        self,
        workspace_key: str,
        content_path: str,
    ) -> AIDPData:
        return self._delete(self._content_path(workspace_key, content_path))

    def export_content(
        self,
        workspace_key: str,
        content_path: str,
        details: Mapping[str, Any] | None = None,
    ) -> AIDPData:
        return self._action(
            "/workspaces/"
            f"{path_param(workspace_key)}/notebook/api/actions/export/contents/"
            f"{path_param(content_path, allow_slash=True)}",
            details,
        )

    def list_sessions(
        self,
        workspace_key: str,
        params: Mapping[str, Any] | None = None,
        **query: Any,
    ) -> AIDPData:
        return self._list(self._sessions_path(workspace_key), params=params, **query)

    def create_session(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._create(self._sessions_path(workspace_key), details)

    def get_session(
        self,
        workspace_key: str,
        session_id: str,
    ) -> AIDPData:
        return self._get(f"{self._sessions_path(workspace_key)}/{path_param(session_id)}")

    def patch_session(
        self,
        workspace_key: str,
        session_id: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._update(
            f"{self._sessions_path(workspace_key)}/{path_param(session_id)}",
            details,
            method="PATCH",
        )

    def delete_session(
        self,
        workspace_key: str,
        session_id: str,
    ) -> AIDPData:
        return self._delete(f"{self._sessions_path(workspace_key)}/{path_param(session_id)}")

    @staticmethod
    def _content_path(workspace_key: str, content_path: str) -> str:
        return (
            f"/workspaces/{path_param(workspace_key)}/notebook/api/contents/"
            f"{path_param(content_path, allow_slash=True)}"
        )

    @staticmethod
    def _sessions_path(workspace_key: str) -> str:
        return f"/workspaces/{path_param(workspace_key)}/notebook/api/sessions"
