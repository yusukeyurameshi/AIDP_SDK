"""Delta Share resource client."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from .base import AIDPData, BaseResource, path_param


class DeltaShareResource(BaseResource):
    """Client for Delta Share shares, recipients and access management."""

    def list_shares(
        self,
        params: Mapping[str, Any] | None = None,
        **query: Any,
    ) -> AIDPData:
        return self._list("/shares", params=params, **query)

    def list_shares_iter(
        self,
        params: Mapping[str, Any] | None = None,
        *,
        item_key: str = "items",
        **query: Any,
    ) -> Iterable[Any]:
        return self._list_iter("/shares", params=params, item_key=item_key, **query)

    def create_share(self, details: Mapping[str, Any]) -> AIDPData:
        return self._create("/shares", details)

    def get_share(self, share_key: str) -> AIDPData:
        return self._get(f"/shares/{path_param(share_key)}")

    def update_share(
        self,
        share_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._update(f"/shares/{path_param(share_key)}", details)

    def delete_share(self, share_key: str) -> AIDPData:
        return self._delete(f"/shares/{path_param(share_key)}")

    def share_permissions(self, share_key: str) -> AIDPData:
        return self._get(f"/shares/{path_param(share_key)}/permissions")

    def manage_share_permissions(
        self,
        share_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._action(f"/shares/{path_param(share_key)}/actions/managePermission", details)

    def manage_share_access(
        self,
        share_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._action(f"/shares/{path_param(share_key)}/actions/manageAccess", details)

    def manage_share_data_assets(
        self,
        share_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._action(f"/shares/{path_param(share_key)}/actions/manageDataAsset", details)

    def list_share_data_assets(
        self,
        share_key: str,
        params: Mapping[str, Any] | None = None,
        **query: Any,
    ) -> AIDPData:
        return self._list(f"/shares/{path_param(share_key)}/dataAssets", params=params, **query)

    def list_share_recipients(
        self,
        share_key: str,
        params: Mapping[str, Any] | None = None,
        **query: Any,
    ) -> AIDPData:
        return self._list(f"/shares/{path_param(share_key)}/recipients", params=params, **query)

    def list_recipients(
        self,
        params: Mapping[str, Any] | None = None,
        **query: Any,
    ) -> AIDPData:
        return self._list("/recipients", params=params, **query)

    def list_recipients_iter(
        self,
        params: Mapping[str, Any] | None = None,
        *,
        item_key: str = "items",
        **query: Any,
    ) -> Iterable[Any]:
        return self._list_iter("/recipients", params=params, item_key=item_key, **query)

    def create_recipient(
        self,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._create("/recipients", details)

    def get_recipient(self, recipient_key: str) -> AIDPData:
        return self._get(f"/recipients/{path_param(recipient_key)}")

    def update_recipient(
        self,
        recipient_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._update(f"/recipients/{path_param(recipient_key)}", details)

    def delete_recipient(self, recipient_key: str) -> AIDPData:
        return self._delete(f"/recipients/{path_param(recipient_key)}")

    def recipient_permissions(
        self,
        recipient_key: str,
    ) -> AIDPData:
        return self._get(f"/recipients/{path_param(recipient_key)}/permissions")

    def manage_recipient_permissions(
        self,
        recipient_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._action(
            f"/recipients/{path_param(recipient_key)}/actions/managePermission",
            details,
        )

    def list_recipient_shares(
        self,
        recipient_key: str,
        params: Mapping[str, Any] | None = None,
        **query: Any,
    ) -> AIDPData:
        return self._list(
            f"/recipients/{path_param(recipient_key)}/shares",
            params=params,
            **query,
        )
