"""Volume resource client."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from .base import AIDPData, BaseResource, path_param


class VolumesResource(BaseResource):
    """Client for volume and volume file operations."""

    def list(
        self,
        params: Mapping[str, Any] | None = None,
        **query: Any,
    ) -> AIDPData:
        return self._list("/volumes", params=params, **query)

    def list_iter(
        self,
        params: Mapping[str, Any] | None = None,
        *,
        item_key: str = "items",
        **query: Any,
    ) -> Iterable[Any]:
        return self._list_iter("/volumes", params=params, item_key=item_key, **query)

    def create(self, details: Mapping[str, Any]) -> AIDPData:
        return self._create("/volumes", details)

    def get(self, volume_key: str) -> AIDPData:
        return self._get(f"/volumes/{path_param(volume_key)}")

    def update(
        self,
        volume_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._update(f"/volumes/{path_param(volume_key)}", details)

    def delete(self, volume_key: str) -> AIDPData:
        return self._delete(f"/volumes/{path_param(volume_key)}")

    def permissions(self, volume_key: str) -> AIDPData:
        return self._get(f"/volumes/{path_param(volume_key)}/permissions")

    def manage_permissions(
        self,
        volume_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._action(
            f"/volumes/{path_param(volume_key)}/actions/managePermission",
            details,
            method="PUT",
        )

    def list_files(
        self,
        volume_key: str,
        params: Mapping[str, Any] | None = None,
        **query: Any,
    ) -> AIDPData:
        return self._list(f"/volumes/{path_param(volume_key)}/files", params=params, **query)

    def mkdir(
        self,
        volume_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._action(f"/volumes/{path_param(volume_key)}/actions/mkdir", details)

    def update_dir(
        self,
        volume_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._action(
            f"/volumes/{path_param(volume_key)}/actions/updateDir",
            details,
            method="PUT",
        )

    def delete_dir(
        self,
        volume_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._delete(f"/volumes/{path_param(volume_key)}/actions/deleteDir", details=details)

    def delete_file(
        self,
        volume_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._delete(
            f"/volumes/{path_param(volume_key)}/actions/deleteFile",
            details=details,
        )

    def upload_file(
        self,
        volume_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._action(f"/volumes/{path_param(volume_key)}/actions/uploadFile", details)

    def upload_file_meta(
        self,
        volume_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._action(f"/volumes/{path_param(volume_key)}/actions/uploadFileMeta", details)

    def download_file(
        self,
        volume_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._action(f"/volumes/{path_param(volume_key)}/actions/downloadFile", details)

    def download_file_meta(
        self,
        volume_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._action(f"/volumes/{path_param(volume_key)}/actions/downloadFileMeta", details)
