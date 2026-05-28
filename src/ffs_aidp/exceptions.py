"""SDK-specific exceptions."""

from __future__ import annotations

from typing import Any


class AIDPError(Exception):
    """Base class for all SDK exceptions."""


class AIDPConfigError(AIDPError, ValueError):
    """Raised when the SDK configuration is invalid."""


class AIDPAuthenticationError(AIDPError):
    """Raised when an OCI signer cannot be created or used."""


class AIDPTransportError(AIDPError):
    """Raised when the HTTP transport fails before a service response is available."""


class AIDPServiceError(AIDPError):
    """Raised for non-success responses returned by the AIDP service."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        code: str | None = None,
        opc_request_id: str | None = None,
        response_body: Any = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code
        self.opc_request_id = opc_request_id
        self.response_body = response_body

    @classmethod
    def from_response(cls, response: Any, parsed_body: Any) -> AIDPServiceError:
        """Build an exception from a requests response and decoded response body."""

        code: str | None = None
        message: str | None = None

        if isinstance(parsed_body, dict):
            raw_code = parsed_body.get("code") or parsed_body.get("errorCode")
            raw_message = parsed_body.get("message") or parsed_body.get("detail")
            code = str(raw_code) if raw_code is not None else None
            message = str(raw_message) if raw_message is not None else None
        elif parsed_body:
            message = str(parsed_body)

        if not message:
            reason = getattr(response, "reason", "")
            message = f"AIDP service returned HTTP {response.status_code}"
            if reason:
                message = f"{message}: {reason}"

        return cls(
            message,
            status_code=response.status_code,
            code=code,
            opc_request_id=response.headers.get("opc-request-id"),
            response_body=parsed_body,
        )

    def __str__(self) -> str:
        parts = [self.message, f"status_code={self.status_code}"]
        if self.code:
            parts.append(f"code={self.code}")
        if self.opc_request_id:
            parts.append(f"opc_request_id={self.opc_request_id}")
        return " | ".join(parts)


class AIDPWaiterError(AIDPError):
    """Raised when a waiter reaches a terminal failure state."""


class AIDPWaiterTimeoutError(AIDPWaiterError, TimeoutError):
    """Raised when a waiter exceeds its maximum wait time."""
