from ffs_aidp.config import AIDPConfig, endpoint_for_region


def test_config_normalizes_endpoint_and_base_path() -> None:
    config = AIDPConfig(
        endpoint="https://aidp.us-ashburn-1.oci.oraclecloud.com/",
        ai_data_platform_id="ocid1.aidataplatform.oc1..example",
    )

    assert config.endpoint == "https://aidp.us-ashburn-1.oci.oraclecloud.com"
    assert (
        config.api_base_path
        == "/20260430/aiDataPlatforms/ocid1.aidataplatform.oc1..example"
    )


def test_endpoint_for_region() -> None:
    assert endpoint_for_region("us-phoenix-1") == "https://aidp.us-phoenix-1.oci.oraclecloud.com"
