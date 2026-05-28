from __future__ import annotations

from typing import Any

from ffs_aidp import auth


class FakeOCIConfig:
    def __init__(self) -> None:
        self.from_file_calls: list[dict[str, str]] = []
        self.validated_configs: list[dict[str, str | None]] = []

    def from_file(self, **kwargs: str) -> dict[str, str | None]:
        self.from_file_calls.append(kwargs)
        return {
            "tenancy": "tenancy",
            "user": "user",
            "fingerprint": "fingerprint",
            "pass_phrase": None,
            "key_file": "/tmp/key.pem",
        }

    def validate_config(self, config: dict[str, str | None]) -> None:
        self.validated_configs.append(config)


class FakeSignerNamespace:
    def __init__(self) -> None:
        self.signer_kwargs: dict[str, Any] | None = None

    def Signer(self, **kwargs: Any) -> object:
        self.signer_kwargs = kwargs
        return object()


class FakeOCI:
    def __init__(self) -> None:
        self.config = FakeOCIConfig()
        self.signer = FakeSignerNamespace()


def test_config_file_signer_omits_none_file_location(monkeypatch: Any) -> None:
    fake_oci = FakeOCI()
    monkeypatch.setattr(auth, "_import_oci", lambda: fake_oci)

    auth.create_config_file_signer(profile="DEFAULT")

    assert fake_oci.config.from_file_calls == [{"profile_name": "DEFAULT"}]
    assert fake_oci.config.validated_configs
    assert fake_oci.signer.signer_kwargs is not None
    assert fake_oci.signer.signer_kwargs["private_key_file_location"] == "/tmp/key.pem"


def test_config_file_signer_passes_explicit_file_location(monkeypatch: Any) -> None:
    fake_oci = FakeOCI()
    monkeypatch.setattr(auth, "_import_oci", lambda: fake_oci)

    auth.create_config_file_signer(config_file="/tmp/oci-config", profile="ADMIN")

    assert fake_oci.config.from_file_calls == [
        {"profile_name": "ADMIN", "file_location": "/tmp/oci-config"}
    ]
