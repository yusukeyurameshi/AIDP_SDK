"""Main Oracle AI Data Platform Workbench SDK client."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any

import requests

from .auth import (
    Signer,
    create_config_file_signer,
    create_instance_principal_signer,
    create_resource_principal_signer,
    create_session_token_signer,
)
from .config import (
    DEFAULT_API_VERSION,
    DEFAULT_PROFILE,
    DEFAULT_TIMEOUT,
    AIDPConfig,
    Timeout,
    endpoint_for_region,
)
from .resources import (
    CatalogsResource,
    ClustersResource,
    DeltaShareResource,
    MLOpsResource,
    NotebooksResource,
    SchemasResource,
    VolumesResource,
    WorkflowsResource,
    WorkspacesResource,
)
from .transport import AIDPTransport, Json
from .waiters import default_state_getter, wait_until


@dataclass(slots=True)
class AIDPClient:
    """Client for Oracle AI Data Platform Workbench REST APIs."""

    config: AIDPConfig
    transport: AIDPTransport
    workspaces: WorkspacesResource = field(init=False)
    clusters: ClustersResource = field(init=False)
    notebooks: NotebooksResource = field(init=False)
    workflows: WorkflowsResource = field(init=False)
    catalogs: CatalogsResource = field(init=False)
    schemas: SchemasResource = field(init=False)
    volumes: VolumesResource = field(init=False)
    delta_share: DeltaShareResource = field(init=False)
    mlops: MLOpsResource = field(init=False)

    def __post_init__(self) -> None:
        self.workspaces = WorkspacesResource(config=self.config, transport=self.transport)
        self.clusters = ClustersResource(config=self.config, transport=self.transport)
        self.notebooks = NotebooksResource(config=self.config, transport=self.transport)
        self.workflows = WorkflowsResource(config=self.config, transport=self.transport)
        self.catalogs = CatalogsResource(config=self.config, transport=self.transport)
        self.schemas = SchemasResource(config=self.config, transport=self.transport)
        self.volumes = VolumesResource(config=self.config, transport=self.transport)
        self.delta_share = DeltaShareResource(config=self.config, transport=self.transport)
        self.mlops = MLOpsResource(config=self.config, transport=self.transport)

    @classmethod
    def from_oci_config(
        cls,
        *,
        endpoint: str | None = None,
        region: str | None = None,
        ai_data_platform_id: str,
        profile: str = DEFAULT_PROFILE,
        config_file: str | None = None,
        api_version: str = DEFAULT_API_VERSION,
        tenancy: str | None = None,
        timeout: Timeout | None = None,
        max_retries: int = 3,
        retry_backoff: float = 0.5,
        user_agent: str | None = None,
        session: requests.Session | None = None,
    ) -> AIDPClient:
        """Create a client using a signer from an OCI config file profile."""

        signer = create_config_file_signer(config_file=config_file, profile=profile)
        return cls.from_signer(
            endpoint=endpoint,
            region=region,
            ai_data_platform_id=ai_data_platform_id,
            signer=signer,
            api_version=api_version,
            profile=profile,
            config_file=config_file,
            tenancy=tenancy,
            timeout=timeout,
            max_retries=max_retries,
            retry_backoff=retry_backoff,
            user_agent=user_agent,
            session=session,
        )

    @classmethod
    def from_session_token(
        cls,
        *,
        endpoint: str | None = None,
        region: str | None = None,
        ai_data_platform_id: str,
        profile: str = DEFAULT_PROFILE,
        config_file: str | None = None,
        security_token_file: str | None = None,
        api_version: str = DEFAULT_API_VERSION,
        timeout: Timeout | None = None,
        max_retries: int = 3,
        retry_backoff: float = 0.5,
        user_agent: str | None = None,
        session: requests.Session | None = None,
    ) -> AIDPClient:
        """Create a client using OCI session-token authentication."""

        signer = create_session_token_signer(
            config_file=config_file,
            profile=profile,
            security_token_file=security_token_file,
        )
        return cls.from_signer(
            endpoint=endpoint,
            region=region,
            ai_data_platform_id=ai_data_platform_id,
            signer=signer,
            api_version=api_version,
            profile=profile,
            config_file=config_file,
            timeout=timeout,
            max_retries=max_retries,
            retry_backoff=retry_backoff,
            user_agent=user_agent,
            session=session,
        )

    @classmethod
    def from_resource_principal(
        cls,
        *,
        endpoint: str | None = None,
        region: str | None = None,
        ai_data_platform_id: str,
        api_version: str = DEFAULT_API_VERSION,
        timeout: Timeout | None = None,
        max_retries: int = 3,
        retry_backoff: float = 0.5,
        user_agent: str | None = None,
        session: requests.Session | None = None,
    ) -> AIDPClient:
        """Create a client using OCI resource-principal authentication."""

        return cls.from_signer(
            endpoint=endpoint,
            region=region,
            ai_data_platform_id=ai_data_platform_id,
            signer=create_resource_principal_signer(),
            api_version=api_version,
            timeout=timeout,
            max_retries=max_retries,
            retry_backoff=retry_backoff,
            user_agent=user_agent,
            session=session,
        )

    @classmethod
    def from_instance_principal(
        cls,
        *,
        endpoint: str | None = None,
        region: str | None = None,
        ai_data_platform_id: str,
        api_version: str = DEFAULT_API_VERSION,
        timeout: Timeout | None = None,
        max_retries: int = 3,
        retry_backoff: float = 0.5,
        user_agent: str | None = None,
        session: requests.Session | None = None,
    ) -> AIDPClient:
        """Create a client using OCI instance-principal authentication."""

        return cls.from_signer(
            endpoint=endpoint,
            region=region,
            ai_data_platform_id=ai_data_platform_id,
            signer=create_instance_principal_signer(),
            api_version=api_version,
            timeout=timeout,
            max_retries=max_retries,
            retry_backoff=retry_backoff,
            user_agent=user_agent,
            session=session,
        )

    @classmethod
    def from_signer(
        cls,
        *,
        endpoint: str | None = None,
        region: str | None = None,
        ai_data_platform_id: str,
        signer: Signer | None,
        api_version: str = DEFAULT_API_VERSION,
        profile: str = DEFAULT_PROFILE,
        tenancy: str | None = None,
        config_file: str | None = None,
        timeout: Timeout | None = None,
        max_retries: int = 3,
        retry_backoff: float = 0.5,
        user_agent: str | None = None,
        session: requests.Session | None = None,
    ) -> AIDPClient:
        """Create a client from a custom requests-compatible OCI signer."""

        resolved_endpoint = endpoint or endpoint_for_region(region or "")
        config = AIDPConfig(
            endpoint=resolved_endpoint,
            ai_data_platform_id=ai_data_platform_id,
            api_version=api_version,
            region=region,
            profile=profile,
            tenancy=tenancy,
            config_file=config_file,
            timeout=timeout or DEFAULT_TIMEOUT,
        )
        transport_kwargs: dict[str, Any] = {
            "endpoint": config.endpoint,
            "signer": signer,
            "timeout": config.timeout,
            "max_retries": max_retries,
            "retry_backoff": retry_backoff,
            "session": session,
        }
        if user_agent:
            transport_kwargs["user_agent"] = user_agent
        return cls(config=config, transport=AIDPTransport(**transport_kwargs))

    def raw_request(
        self,
        method: str,
        path: str,
        *,
        include_base_path: bool = True,
        params: Mapping[str, Any] | None = None,
        json_body: Json = None,
        data: Any = None,
        files: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        expected_status: int | Iterable[int] | None = None,
    ) -> Any:
        """Call an endpoint that is not yet wrapped by a resource method."""

        request_path = self._resolve_raw_path(path, include_base_path=include_base_path)
        return self.transport.request(
            method,
            request_path,
            params=params,
            json_body=json_body,
            data=data,
            files=files,
            headers=headers,
            expected_status=expected_status,
        )

    def wait_until(
        self,
        *,
        getter: Callable[[], Any],
        target_states: Iterable[str],
        failure_states: Iterable[str] = (),
        state_getter: Callable[[Any], str | None] = default_state_getter,
        interval_seconds: float = 5.0,
        max_wait_seconds: float = 600.0,
    ) -> Any:
        """Poll a callable until it reaches a target state."""

        return wait_until(
            getter=getter,
            target_states=target_states,
            failure_states=failure_states,
            state_getter=state_getter,
            interval_seconds=interval_seconds,
            max_wait_seconds=max_wait_seconds,
        )

    def close(self) -> None:
        self.transport.close()

    def __enter__(self) -> AIDPClient:
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()

    def _resolve_raw_path(self, path: str, *, include_base_path: bool) -> str:
        if path.startswith(("http://", "https://")):
            return path

        normalized = path if path.startswith("/") else f"/{path}"
        version_prefix = f"/{self.config.api_version}/"
        if not include_base_path or normalized.startswith(version_prefix):
            return normalized
        return f"{self.config.api_base_path}{normalized}"
