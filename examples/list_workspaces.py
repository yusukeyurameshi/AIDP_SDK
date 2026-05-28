"""List AIDP workspaces using OCI config-file authentication."""

from __future__ import annotations

import os

from ffs_aidp import AIDPClient


def main() -> None:
    endpoint = os.environ["AIDP_ENDPOINT"]
    ai_data_platform_id = os.environ["AIDP_ID"]
    profile = os.environ.get("OCI_PROFILE", "DEFAULT")

    with AIDPClient.from_oci_config(
        endpoint=endpoint,
        ai_data_platform_id=ai_data_platform_id,
        profile=profile,
    ) as client:
        for workspace in client.workspaces.list_iter():
            print(workspace)


if __name__ == "__main__":
    main()
