"""MLOps preview resource client.

The Oracle AIDP documentation marks the MLOps category as preview. Method names
mirror the MLflow-compatible endpoint names but do not hide that preview status.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast

from .base import AIDPData, BaseResource, path_param

MLFLOW_PREFIX = "mlops/api/2.0/mlflow"


class MLOpsResource(BaseResource):
    """Client for preview MLOps/MLflow-compatible operations."""

    preview = True

    def request(
        self,
        method: str,
        mlflow_path: str,
        *,
        workspace_key: str | None = None,
        params: Mapping[str, Any] | None = None,
        details: Mapping[str, Any] | None = None,
    ) -> AIDPData:
        prefix = self._prefix(workspace_key)
        normalized = mlflow_path.strip("/")
        json_body = dict(details or {}) if method.upper() in {"POST", "PUT", "PATCH"} else None
        return cast(
            AIDPData,
            self._request(
                method,
                f"/{prefix}/{normalized}",
                params=params,
                json_body=json_body,
            ),
        )

    def create_registered_model(
        self,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("POST", "registered-models/create", details=details)

    def get_registered_model(
        self,
        params: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("GET", "registered-models/get", params=params)

    def list_registered_models(
        self,
        params: Mapping[str, Any] | None = None,
    ) -> AIDPData:
        return self.request("GET", "registered-models/search", params=params)

    def update_registered_model(
        self,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("POST", "registered-models/update", details=details)

    def delete_registered_model(
        self,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("POST", "registered-models/delete", details=details)

    def rename_registered_model(
        self,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("POST", "registered-models/rename", details=details)

    def set_registered_model_tag(
        self,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("POST", "registered-models/set-tag", details=details)

    def delete_registered_model_tag(
        self,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("POST", "registered-models/delete-tag", details=details)

    def create_model_version(
        self,
        details: Mapping[str, Any],
        *,
        workspace_key: str | None = None,
    ) -> AIDPData:
        return self.request(
            "POST",
            "model-versions/create",
            workspace_key=workspace_key,
            details=details,
        )

    def get_model_version(
        self,
        params: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("GET", "model-versions/get", params=params)

    def list_model_versions(
        self,
        params: Mapping[str, Any] | None = None,
    ) -> AIDPData:
        return self.request("GET", "model-versions/search", params=params)

    def update_model_version(
        self,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("POST", "model-versions/update", details=details)

    def delete_model_version(
        self,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("POST", "model-versions/delete", details=details)

    def transition_model_version_stage(
        self,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("POST", "model-versions/transition-stage", details=details)

    def set_model_version_tag(
        self,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("POST", "model-versions/set-tag", details=details)

    def delete_model_version_tag(
        self,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("POST", "model-versions/delete-tag", details=details)

    def create_experiment(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request(
            "POST",
            "experiments/create",
            workspace_key=workspace_key,
            details=details,
        )

    def get_experiment(
        self,
        workspace_key: str,
        params: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("GET", "experiments/get", workspace_key=workspace_key, params=params)

    def get_experiment_by_name(
        self,
        workspace_key: str,
        params: Mapping[str, Any],
    ) -> AIDPData:
        return self.request(
            "GET",
            "experiments/get-by-name",
            workspace_key=workspace_key,
            params=params,
        )

    def search_experiments(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request(
            "POST",
            "experiments/search",
            workspace_key=workspace_key,
            details=details,
        )

    def update_experiment(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request(
            "POST",
            "experiments/update",
            workspace_key=workspace_key,
            details=details,
        )

    def delete_experiment(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request(
            "POST",
            "experiments/delete",
            workspace_key=workspace_key,
            details=details,
        )

    def restore_experiment(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request(
            "POST",
            "experiments/restore",
            workspace_key=workspace_key,
            details=details,
        )

    def set_experiment_tag(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request(
            "POST",
            "experiments/set-experiment-tag",
            workspace_key=workspace_key,
            details=details,
        )

    def delete_experiment_tag(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request(
            "POST",
            "experiments/delete-experiment-tag",
            workspace_key=workspace_key,
            details=details,
        )

    def create_run(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("POST", "runs/create", workspace_key=workspace_key, details=details)

    def get_run(
        self,
        workspace_key: str,
        params: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("GET", "runs/get", workspace_key=workspace_key, params=params)

    def search_runs(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("POST", "runs/search", workspace_key=workspace_key, details=details)

    def update_run(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("POST", "runs/update", workspace_key=workspace_key, details=details)

    def delete_run(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("POST", "runs/delete", workspace_key=workspace_key, details=details)

    def restore_run(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("POST", "runs/restore", workspace_key=workspace_key, details=details)

    def log_batch(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("POST", "runs/log-batch", workspace_key=workspace_key, details=details)

    def log_metric(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("POST", "runs/log-metric", workspace_key=workspace_key, details=details)

    def log_parameter(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request(
            "POST",
            "runs/log-parameter",
            workspace_key=workspace_key,
            details=details,
        )

    def log_model(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("POST", "runs/log-model", workspace_key=workspace_key, details=details)

    def log_inputs(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("POST", "runs/log-inputs", workspace_key=workspace_key, details=details)

    def set_run_tag(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("POST", "runs/set-tag", workspace_key=workspace_key, details=details)

    def delete_run_tag(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("POST", "runs/delete-tag", workspace_key=workspace_key, details=details)

    def metric_history(
        self,
        workspace_key: str,
        params: Mapping[str, Any],
    ) -> AIDPData:
        return self.request(
            "GET",
            "metrics/get-history",
            workspace_key=workspace_key,
            params=params,
        )

    def list_artifacts(
        self,
        workspace_key: str,
        params: Mapping[str, Any],
    ) -> AIDPData:
        return self.request("GET", "artifacts/list", workspace_key=workspace_key, params=params)

    def search_logged_models(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self.request(
            "POST",
            "logged-models/search",
            workspace_key=workspace_key,
            details=details,
        )

    @staticmethod
    def _prefix(workspace_key: str | None = None) -> str:
        if workspace_key:
            return f"workspaces/{path_param(workspace_key)}/{MLFLOW_PREFIX}"
        return MLFLOW_PREFIX
