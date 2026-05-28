from __future__ import annotations

from typing import Any

import requests

from ffs_aidp import AIDPClient
from test_transport import FakeSession, make_response


def test_workspaces_list_uses_versioned_platform_path() -> None:
    session = FakeSession([make_response(200, {"items": []})])
    client = AIDPClient.from_signer(
        endpoint="https://aidp.us-ashburn-1.oci.oraclecloud.com",
        ai_data_platform_id="ocid1.aidataplatform.oc1..example",
        signer=lambda request: request,
        session=session,  # type: ignore[arg-type]
        max_retries=0,
    )

    assert client.workspaces.list() == {"items": []}
    assert session.calls[0]["method"] == "GET"
    assert session.calls[0]["url"].endswith(
        "/20260430/aiDataPlatforms/ocid1.aidataplatform.oc1..example/workspaces"
    )


def test_cluster_action_path() -> None:
    session = FakeSession([make_response(202, {"state": "STARTING"})])
    client = AIDPClient.from_signer(
        endpoint="https://aidp.us-ashburn-1.oci.oraclecloud.com",
        ai_data_platform_id="ocid1.aidataplatform.oc1..example",
        signer=lambda request: request,
        session=session,  # type: ignore[arg-type]
        max_retries=0,
    )

    result = client.clusters.start("workspaceKey", "clusterKey")

    assert result == {"state": "STARTING"}
    assert session.calls[0]["method"] == "POST"
    assert session.calls[0]["url"].endswith(
        "/workspaces/workspaceKey/clusters/clusterKey/actions/start"
    )


def test_list_iter_uses_opc_next_page() -> None:
    responses: list[requests.Response] = [
        make_response(200, {"items": [{"key": "one"}]}, headers={"opc-next-page": "page-2"}),
        make_response(200, {"items": [{"key": "two"}]}),
    ]
    session = FakeSession(responses)
    client = AIDPClient.from_signer(
        endpoint="https://aidp.us-ashburn-1.oci.oraclecloud.com",
        ai_data_platform_id="ocid1.aidataplatform.oc1..example",
        signer=lambda request: request,
        session=session,  # type: ignore[arg-type]
        max_retries=0,
    )

    assert list(client.workspaces.list_iter()) == [{"key": "one"}, {"key": "two"}]
    assert session.calls[0]["params"] is None
    assert session.calls[1]["params"] == {"page": "page-2"}


def test_raw_request_can_skip_base_path() -> None:
    session = FakeSession([make_response(200, {"ok": True})])
    client = AIDPClient.from_signer(
        endpoint="https://aidp.us-ashburn-1.oci.oraclecloud.com",
        ai_data_platform_id="ocid1.aidataplatform.oc1..example",
        signer=lambda request: request,
        session=session,  # type: ignore[arg-type]
        max_retries=0,
    )

    assert client.raw_request("GET", "/health", include_base_path=False) == {"ok": True}
    assert session.calls[0]["url"] == "https://aidp.us-ashburn-1.oci.oraclecloud.com/health"


def test_wait_until_returns_target_state() -> None:
    states: list[dict[str, Any]] = [{"lifecycleState": "CREATING"}, {"lifecycleState": "ACTIVE"}]
    client = AIDPClient.from_signer(
        endpoint="https://aidp.us-ashburn-1.oci.oraclecloud.com",
        ai_data_platform_id="ocid1.aidataplatform.oc1..example",
        signer=lambda request: request,
        session=FakeSession([]),  # type: ignore[arg-type]
        max_retries=0,
    )

    result = client.wait_until(
        getter=lambda: states.pop(0),
        target_states={"ACTIVE"},
        interval_seconds=0,
        max_wait_seconds=1,
    )

    assert result == {"lifecycleState": "ACTIVE"}
