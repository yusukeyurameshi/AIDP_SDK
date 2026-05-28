"""Shared resource-client helpers."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any, TypeAlias, cast
from urllib.parse import quote

from ffs_aidp.config import AIDPConfig
from ffs_aidp.pagination import iter_items
from ffs_aidp.transport import AIDPResponse, AIDPTransport, Json

AIDPData: TypeAlias = dict[str, Any] | list[Any] | str | None


class BaseResource:
    """Base class for domain-specific AIDP resources."""

    def __init__(self, *, config: AIDPConfig, transport: AIDPTransport) -> None:
        self._config = config
        self._transport = transport

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json_body: Json = None,
        data: Any = None,
        files: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        expected_status: int | Iterable[int] | None = None,
        raw_response: bool = False,
    ) -> Any:
        return self._transport.request(
            method,
            self._api_path(path),
            params=params,
            json_body=json_body,
            data=data,
            files=files,
            headers=headers,
            expected_status=expected_status,
            raw_response=raw_response,
        )

    def _api_path(self, path: str) -> str:
        normalized = path if path.startswith("/") else f"/{path}"
        return f"{self._config.api_base_path}{normalized}"

    def _list(
        self,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        **query: Any,
    ) -> AIDPData:
        return cast(AIDPData, self._request("GET", path, params=merge_params(params, query)))

    def _list_iter(
        self,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        item_key: str = "items",
        **query: Any,
    ) -> Iterable[Any]:
        base_params = merge_params(params, query)

        def fetch_page(page: str | None) -> AIDPResponse:
            request_params = dict(base_params)
            if page:
                request_params["page"] = page
            return cast(
                AIDPResponse,
                self._request("GET", path, params=request_params, raw_response=True),
            )

        return iter_items(fetch_page, item_key=item_key)

    def _get(
        self,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        **query: Any,
    ) -> AIDPData:
        return cast(AIDPData, self._request("GET", path, params=merge_params(params, query)))

    def _create(
        self,
        path: str,
        details: Mapping[str, Any] | None = None,
        *,
        params: Mapping[str, Any] | None = None,
        **query: Any,
    ) -> AIDPData:
        return cast(
            AIDPData,
            self._request(
                "POST",
                path,
                params=merge_params(params, query),
                json_body=dict(details or {}),
            ),
        )

    def _update(
        self,
        path: str,
        details: Mapping[str, Any] | None = None,
        *,
        method: str = "PUT",
        params: Mapping[str, Any] | None = None,
        **query: Any,
    ) -> AIDPData:
        return cast(
            AIDPData,
            self._request(
                method,
                path,
                params=merge_params(params, query),
                json_body=dict(details or {}),
            ),
        )

    def _delete(
        self,
        path: str,
        *,
        details: Mapping[str, Any] | None = None,
        params: Mapping[str, Any] | None = None,
        **query: Any,
    ) -> AIDPData:
        return cast(
            AIDPData,
            self._request(
                "DELETE",
                path,
                params=merge_params(params, query),
                json_body=dict(details) if details is not None else None,
            ),
        )

    def _action(
        self,
        path: str,
        details: Mapping[str, Any] | None = None,
        *,
        method: str = "POST",
        params: Mapping[str, Any] | None = None,
        **query: Any,
    ) -> AIDPData:
        return cast(
            AIDPData,
            self._request(
                method,
                path,
                params=merge_params(params, query),
                json_body=dict(details or {}),
            ),
        )


def merge_params(
    params: Mapping[str, Any] | None = None,
    query: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    if params:
        merged.update(params)
    if query:
        merged.update(query)
    return {key: value for key, value in merged.items() if value is not None}


def path_param(value: Any, *, allow_slash: bool = False) -> str:
    raw = str(value).strip("/") if allow_slash else str(value)
    return quote(raw, safe="/" if allow_slash else "")
