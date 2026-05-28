from __future__ import annotations

import json
from typing import Any

import pytest
import requests

from ffs_aidp.exceptions import AIDPServiceError
from ffs_aidp.transport import AIDPTransport


class FakeSession:
    def __init__(self, responses: list[requests.Response]) -> None:
        self.responses = responses
        self.calls: list[dict[str, Any]] = []
        self.auth: Any = None
        self.closed = False

    def mount(self, *_args: Any, **_kwargs: Any) -> None:
        return None

    def request(self, **kwargs: Any) -> requests.Response:
        self.calls.append(kwargs)
        return self.responses.pop(0)

    def close(self) -> None:
        self.closed = True


def make_response(
    status_code: int,
    payload: Any = None,
    *,
    headers: dict[str, str] | None = None,
) -> requests.Response:
    response = requests.Response()
    response.status_code = status_code
    response.reason = "OK" if status_code < 400 else "Error"
    response.headers.update(headers or {})
    if payload is None:
        response._content = b""
    else:
        response.headers.setdefault("Content-Type", "application/json")
        response._content = json.dumps(payload).encode("utf-8")
    return response


def test_transport_decodes_json_and_sets_defaults() -> None:
    session = FakeSession([make_response(200, {"ok": True})])

    def signer(request: Any) -> Any:
        return request

    transport = AIDPTransport(
        endpoint="https://example.com",
        signer=signer,
        session=session,  # type: ignore[arg-type]
        max_retries=0,
    )

    result = transport.request("GET", "/v1/things", params={"a": 1, "b": None})

    assert result == {"ok": True}
    assert session.auth is signer
    assert session.calls[0]["url"] == "https://example.com/v1/things"
    assert session.calls[0]["params"] == {"a": 1}
    assert session.calls[0]["headers"]["Accept"] == "application/json"


def test_transport_raises_service_error() -> None:
    session = FakeSession(
        [
            make_response(
                404,
                {"code": "NotFound", "message": "missing"},
                headers={"opc-request-id": "req-1"},
            )
        ]
    )
    transport = AIDPTransport(
        endpoint="https://example.com",
        session=session,  # type: ignore[arg-type]
        max_retries=0,
    )

    with pytest.raises(AIDPServiceError) as exc_info:
        transport.request("GET", "/missing")

    assert exc_info.value.status_code == 404
    assert exc_info.value.code == "NotFound"
    assert exc_info.value.opc_request_id == "req-1"
