"""Synchronous HTTP transport for AIDP REST calls."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from .config import DEFAULT_TIMEOUT, Timeout
from .exceptions import AIDPServiceError, AIDPTransportError

DEFAULT_USER_AGENT = "ffs-aidp-sdk/0.1.0"
Json = dict[str, Any] | list[Any] | str | int | float | bool | None


@dataclass(frozen=True, slots=True)
class AIDPResponse:
    """Decoded HTTP response plus transport metadata."""

    data: Any
    status_code: int
    headers: Mapping[str, str]
    opc_request_id: str | None = None
    text: str | None = None


class AIDPTransport:
    """Small requests-based transport with OCI signer support."""

    def __init__(
        self,
        *,
        endpoint: str,
        signer: Any | None = None,
        timeout: Timeout = DEFAULT_TIMEOUT,
        max_retries: int = 3,
        retry_backoff: float = 0.5,
        user_agent: str = DEFAULT_USER_AGENT,
        session: requests.Session | None = None,
    ) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.timeout = timeout
        self.user_agent = user_agent
        self.session = session or requests.Session()

        if signer is not None:
            self.session.auth = signer

        if max_retries > 0:
            retry = Retry(
                total=max_retries,
                connect=max_retries,
                read=max_retries,
                status=max_retries,
                backoff_factor=retry_backoff,
                status_forcelist=(429, 500, 502, 503, 504),
                allowed_methods=frozenset(
                    {"DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"}
                ),
                raise_on_status=False,
            )
            adapter = HTTPAdapter(max_retries=retry)
            self.session.mount("https://", adapter)
            self.session.mount("http://", adapter)

    def request(
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
        timeout: Timeout | None = None,
    ) -> Any:
        """Execute an HTTP request and return decoded JSON/text data."""

        request_headers = {
            "Accept": "application/json",
            "User-Agent": self.user_agent,
        }
        if json_body is not None:
            request_headers["Content-Type"] = "application/json"
        if headers:
            request_headers.update(headers)

        url = path if path.startswith(("http://", "https://")) else f"{self.endpoint}{path}"

        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                params=_compact_mapping(params),
                json=json_body,
                data=data,
                files=files,
                headers=request_headers,
                timeout=timeout or self.timeout,
            )
        except requests.RequestException as exc:
            raise AIDPTransportError(str(exc)) from exc

        parsed = self._decode_response(response)
        if not self._status_is_expected(response.status_code, expected_status):
            raise AIDPServiceError.from_response(response, parsed)

        result = AIDPResponse(
            data=parsed,
            status_code=response.status_code,
            headers=response.headers,
            opc_request_id=response.headers.get("opc-request-id"),
            text=response.text if isinstance(parsed, str) else None,
        )
        return result if raw_response else result.data

    def close(self) -> None:
        self.session.close()

    @staticmethod
    def _decode_response(response: requests.Response) -> Any:
        if response.status_code == 204 or not response.content:
            return None

        content_type = response.headers.get("Content-Type", "")
        text = response.text
        if "json" in content_type.lower() or text.lstrip().startswith(("{", "[")):
            try:
                return response.json()
            except ValueError:
                return text
        return text

    @staticmethod
    def _status_is_expected(
        status_code: int,
        expected_status: int | Iterable[int] | None,
    ) -> bool:
        if expected_status is None:
            return 200 <= status_code < 300
        if isinstance(expected_status, int):
            return status_code == expected_status
        return status_code in set(expected_status)


def _compact_mapping(mapping: Mapping[str, Any] | None) -> dict[str, Any] | None:
    if mapping is None:
        return None
    compacted = {key: value for key, value in mapping.items() if value is not None}
    return compacted or None
