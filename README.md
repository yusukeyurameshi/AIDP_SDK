# ffs-aidp-sdk

`ffs-aidp-sdk` is a Python SDK for Oracle AI Data Platform Workbench REST APIs.
It provides a typed, extensible client around the documented `/20260430`
endpoints while still exposing `raw_request()` for new API operations.

- PyPI distribution name: `ffs-aidp-sdk`
- Python import name: `ffs_aidp`
- Minimum Python: 3.10
- License: UPL-1.0

This package does not include credentials, OCIDs, tokens, private keys or sample
data tied to a real tenancy.

## Installation

```bash
python -m pip install ffs-aidp-sdk
```

For local development:

```bash
python -m pip install -e ".[dev]"
```

Do not publish this package without explicit confirmation. Before any future
publish, confirm again that `ffs-aidp-sdk` is still available on PyPI.

## HTTP stack choice

The SDK uses `requests` instead of `httpx` because the OCI Python SDK signer is
designed to plug directly into the `requests` authentication flow, and because
`requests` plus `urllib3` gives a stable synchronous retry/timeout stack with no
async policy decisions for callers. The transport is isolated in
`ffs_aidp.transport`, so an `httpx` transport can be added later without changing
resource clients.

## Authentication

The default path uses the OCI config file and profile:

```python
from ffs_aidp import AIDPClient

client = AIDPClient.from_oci_config(
    endpoint="https://aidp.<region>.oci.oraclecloud.com",
    ai_data_platform_id="ocid1.aidataplatform.oc1..example",
    profile="DEFAULT",
)
```

Session-token, instance-principal, resource-principal and custom-signer flows
are also supported:

```python
client = AIDPClient.from_resource_principal(
    endpoint="https://aidp.<region>.oci.oraclecloud.com",
    ai_data_platform_id="ocid1.aidataplatform.oc1..example",
)
```

```python
client = AIDPClient.from_signer(
    endpoint="https://aidp.<region>.oci.oraclecloud.com",
    ai_data_platform_id="ocid1.aidataplatform.oc1..example",
    signer=my_requests_compatible_signer,
)
```

## Quick start

```python
from ffs_aidp import AIDPClient

client = AIDPClient.from_oci_config(
    endpoint="https://aidp.<region>.oci.oraclecloud.com",
    ai_data_platform_id="ocid1.aidataplatform.oc1..example",
    profile="DEFAULT",
)

workspaces = client.workspaces.list()
workspace = client.workspaces.get("workspaceKey")
```

The API version defaults to `20260430` and can be overridden:

```python
client = AIDPClient.from_oci_config(
    endpoint="https://aidp.<region>.oci.oraclecloud.com",
    ai_data_platform_id="ocid1.aidataplatform.oc1..example",
    api_version="20260430",
)
```

## Examples

List workspaces:

```python
for workspace in client.workspaces.list_iter():
    print(workspace.get("displayName"), workspace.get("key"))
```

Start a cluster:

```python
client.clusters.start(
    workspace_key="workspaceKey",
    cluster_key="clusterKey",
)
```

Create and run a job:

```python
job = client.workflows.create_job(
    workspace_key="workspaceKey",
    details={
        "displayName": "daily-refresh",
        "description": "Example job definition",
    },
)

run = client.workflows.create_job_run(
    workspace_key="workspaceKey",
    details={"jobKey": job["key"]},
)
```

Catalogs, schemas, tables and views:

```python
catalogs = client.catalogs.list()
schemas = client.schemas.list_schemas(catalog_key="catalogKey")
tables = client.schemas.list_tables(schema_key="schemaKey")
views = client.schemas.list_views(schema_key="schemaKey")
```

Volumes:

```python
files = client.volumes.list_files("volumeKey", path="/")
upload_target = client.volumes.upload_file_meta(
    "volumeKey",
    {"path": "/tmp/example.csv"},
)
```

Delta Share:

```python
shares = client.delta_share.list_shares()
recipients = client.delta_share.list_recipients()
```

MLOps APIs are exposed under `client.mlops` and are marked preview because the
Oracle documentation labels the MLOps category as preview:

```python
experiments = client.mlops.search_experiments(
    workspace_key="workspaceKey",
    details={"max_results": 25},
)
```

## Pagination

List methods return one response page. Methods ending in `_iter()` iterate over
all pages using `opc-next-page`, `opcNextPage`, `nextPage` or `next_page` when
present.

```python
for job in client.workflows.list_jobs_iter("workspaceKey"):
    print(job)
```

## Waiters

The SDK includes a generic waiter for asynchronous operations:

```python
workspace = client.wait_until(
    getter=lambda: client.workspaces.get("workspaceKey"),
    target_states={"ACTIVE"},
    failure_states={"FAILED", "DELETED"},
)
```

## Development

```bash
python -m pip install -e ".[dev]"
python -m ruff check .
python -m pytest
python -m build
python -m twine check dist/*
```

No command above publishes to PyPI.
