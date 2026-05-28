"""Configuration primitives for the AIDP SDK."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias
from urllib.parse import quote

from .exceptions import AIDPConfigError

DEFAULT_API_VERSION = "20260430"
DEFAULT_PROFILE = "DEFAULT"
DEFAULT_TIMEOUT: tuple[float, float] = (10.0, 60.0)
Timeout: TypeAlias = float | tuple[float, float]


@dataclass(frozen=True, slots=True)
class AIDPConfig:
    """Runtime configuration used by :class:`ffs_aidp.client.AIDPClient`."""

    endpoint: str
    ai_data_platform_id: str
    api_version: str = DEFAULT_API_VERSION
    region: str | None = None
    profile: str = DEFAULT_PROFILE
    tenancy: str | None = None
    config_file: str | None = None
    timeout: Timeout = DEFAULT_TIMEOUT

    def __post_init__(self) -> None:
        endpoint = self.endpoint.strip().rstrip("/")
        api_version = self.api_version.strip().strip("/")
        ai_data_platform_id = self.ai_data_platform_id.strip()

        if not endpoint:
            raise AIDPConfigError("endpoint is required")
        if not ai_data_platform_id:
            raise AIDPConfigError("ai_data_platform_id is required")
        if not api_version:
            raise AIDPConfigError("api_version is required")

        object.__setattr__(self, "endpoint", endpoint)
        object.__setattr__(self, "api_version", api_version)
        object.__setattr__(self, "ai_data_platform_id", ai_data_platform_id)

    @property
    def api_base_path(self) -> str:
        platform_id = quote(self.ai_data_platform_id, safe="")
        return f"/{self.api_version}/aiDataPlatforms/{platform_id}"


def endpoint_for_region(region: str) -> str:
    """Return the standard AIDP endpoint for an OCI region identifier."""

    normalized = region.strip()
    if not normalized:
        raise AIDPConfigError("region is required to build an endpoint")
    return f"https://aidp.{normalized}.oci.oraclecloud.com"
