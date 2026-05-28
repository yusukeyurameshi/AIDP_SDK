"""Cluster resource client."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from .base import AIDPData, BaseResource, path_param


class ClustersResource(BaseResource):
    """Client for cluster operations inside workspaces."""

    def list(
        self,
        workspace_key: str,
        params: Mapping[str, Any] | None = None,
        **query: Any,
    ) -> AIDPData:
        return self._list(self._collection_path(workspace_key), params=params, **query)

    def list_iter(
        self,
        workspace_key: str,
        params: Mapping[str, Any] | None = None,
        *,
        item_key: str = "items",
        **query: Any,
    ) -> Iterable[Any]:
        return self._list_iter(
            self._collection_path(workspace_key),
            params=params,
            item_key=item_key,
            **query,
        )

    def get_default(self) -> AIDPData:
        return self._get("/defaultCluster")

    def create(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._create(self._collection_path(workspace_key), details)

    def get(
        self,
        workspace_key: str,
        cluster_key: str,
    ) -> AIDPData:
        return self._get(self._item_path(workspace_key, cluster_key))

    def update(
        self,
        workspace_key: str,
        cluster_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._update(self._item_path(workspace_key, cluster_key), details)

    def delete(
        self,
        workspace_key: str,
        cluster_key: str,
    ) -> AIDPData:
        return self._delete(self._item_path(workspace_key, cluster_key))

    def start(
        self,
        workspace_key: str,
        cluster_key: str,
        details: Mapping[str, Any] | None = None,
    ) -> AIDPData:
        return self._action(f"{self._item_path(workspace_key, cluster_key)}/actions/start", details)

    def stop(
        self,
        workspace_key: str,
        cluster_key: str,
        details: Mapping[str, Any] | None = None,
    ) -> AIDPData:
        return self._action(f"{self._item_path(workspace_key, cluster_key)}/actions/stop", details)

    def restart(
        self,
        workspace_key: str,
        cluster_key: str,
        details: Mapping[str, Any] | None = None,
    ) -> AIDPData:
        return self._action(
            f"{self._item_path(workspace_key, cluster_key)}/actions/restart",
            details,
        )

    def libraries(
        self,
        workspace_key: str,
        cluster_key: str,
    ) -> AIDPData:
        return self._get(f"{self._item_path(workspace_key, cluster_key)}/libraries")

    def patch_libraries(
        self,
        workspace_key: str,
        cluster_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._update(
            f"{self._item_path(workspace_key, cluster_key)}/libraries",
            details,
            method="PATCH",
        )

    def permissions(
        self,
        workspace_key: str,
        cluster_key: str,
    ) -> AIDPData:
        return self._get(f"{self._item_path(workspace_key, cluster_key)}/permissions")

    def manage_permissions(
        self,
        workspace_key: str,
        cluster_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._action(
            f"{self._item_path(workspace_key, cluster_key)}/actions/managePermission",
            details,
        )

    def download_logs(
        self,
        workspace_key: str,
        cluster_key: str,
        details: Mapping[str, Any] | None = None,
    ) -> AIDPData:
        return self._action(
            f"{self._item_path(workspace_key, cluster_key)}/actions/downloadLogs",
            details,
        )

    def search_logs(
        self,
        workspace_key: str,
        cluster_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._action(
            f"{self._item_path(workspace_key, cluster_key)}/actions/searchLogs",
            details,
        )

    def summarize_metrics_data(
        self,
        workspace_key: str,
        cluster_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._action(
            f"{self._item_path(workspace_key, cluster_key)}/actions/summarizeMetricsData",
            details,
        )

    @staticmethod
    def _collection_path(workspace_key: str) -> str:
        return f"/workspaces/{path_param(workspace_key)}/clusters"

    @classmethod
    def _item_path(cls, workspace_key: str, cluster_key: str) -> str:
        return f"{cls._collection_path(workspace_key)}/{path_param(cluster_key)}"
