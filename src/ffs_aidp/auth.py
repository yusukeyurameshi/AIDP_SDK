"""OCI signer factories used by the SDK."""

from __future__ import annotations

from collections.abc import Callable
from importlib import import_module
from pathlib import Path
from typing import Any, Protocol, cast

from .exceptions import AIDPAuthenticationError


class Signer(Protocol):
    """Protocol for requests-compatible OCI signers."""

    def __call__(self, request: Any) -> Any:
        """Sign a prepared requests object."""


SignerFactory = Callable[[], Signer]


def _import_oci() -> Any:
    try:
        return import_module("oci")
    except ImportError as exc:
        raise AIDPAuthenticationError(
            "The 'oci' package is required for OCI authentication. "
            "Install ffs-aidp-sdk with its runtime dependencies."
        ) from exc


def create_config_file_signer(
    *,
    config_file: str | None = None,
    profile: str = "DEFAULT",
) -> Signer:
    """Create a signer from an OCI config file profile."""

    oci = _import_oci()
    config = _load_config_from_file(oci, config_file=config_file, profile=profile)
    oci.config.validate_config(config)

    signer_kwargs: dict[str, Any] = {
        "tenancy": config["tenancy"],
        "user": config["user"],
        "fingerprint": config["fingerprint"],
        "pass_phrase": config.get("pass_phrase"),
    }
    if config.get("key_file"):
        signer_kwargs["private_key_file_location"] = config["key_file"]
    if config.get("key_content"):
        signer_kwargs["private_key_content"] = config["key_content"]

    return cast(Signer, oci.signer.Signer(**signer_kwargs))


def create_session_token_signer(
    *,
    config_file: str | None = None,
    profile: str = "DEFAULT",
    security_token_file: str | None = None,
) -> Signer:
    """Create a signer for OCI CLI session-token authentication."""

    oci = _import_oci()
    config = _load_config_from_file(oci, config_file=config_file, profile=profile)
    token_file = security_token_file or config.get("security_token_file")
    key_file = config.get("key_file")

    if not token_file:
        raise AIDPAuthenticationError(
            "security_token_file is required for session-token authentication"
        )
    if not key_file:
        raise AIDPAuthenticationError("key_file is required for session-token authentication")

    token_path = Path(token_file).expanduser()
    token = token_path.read_text(encoding="utf-8").strip()
    private_key = oci.signer.load_private_key_from_file(key_file, config.get("pass_phrase"))
    return cast(Signer, oci.auth.signers.SecurityTokenSigner(token, private_key))


def create_resource_principal_signer() -> Signer:
    """Create a signer from OCI resource-principal environment variables."""

    oci = _import_oci()
    return cast(Signer, oci.auth.signers.get_resource_principals_signer())


def create_instance_principal_signer() -> Signer:
    """Create an instance-principal signer."""

    oci = _import_oci()
    return cast(Signer, oci.auth.signers.InstancePrincipalsSecurityTokenSigner())


def _load_config_from_file(
    oci: Any,
    *,
    config_file: str | None,
    profile: str,
) -> dict[str, Any]:
    kwargs = {"profile_name": profile}
    if config_file is not None:
        kwargs["file_location"] = config_file
    return cast(dict[str, Any], oci.config.from_file(**kwargs))
