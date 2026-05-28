"""Create a job run for an existing AIDP job."""

from __future__ import annotations

import os

from ffs_aidp import AIDPClient


def main() -> None:
    endpoint = os.environ["AIDP_ENDPOINT"]
    ai_data_platform_id = os.environ["AIDP_ID"]
    workspace_key = os.environ["AIDP_WORKSPACE_KEY"]
    job_key = os.environ["AIDP_JOB_KEY"]

    with AIDPClient.from_oci_config(
        endpoint=endpoint,
        ai_data_platform_id=ai_data_platform_id,
        profile=os.environ.get("OCI_PROFILE", "DEFAULT"),
    ) as client:
        run = client.workflows.create_job_run(
            workspace_key=workspace_key,
            details={"jobKey": job_key},
        )
        print(run)


if __name__ == "__main__":
    main()
