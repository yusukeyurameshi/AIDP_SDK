"""Workflow, job, job run and task run resource client."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from .base import AIDPData, BaseResource, path_param


class WorkflowsResource(BaseResource):
    """Client for workflow/job APIs."""

    def list_jobs(
        self,
        workspace_key: str,
        params: Mapping[str, Any] | None = None,
        **query: Any,
    ) -> AIDPData:
        return self._list(self._jobs_path(workspace_key), params=params, **query)

    def list_jobs_iter(
        self,
        workspace_key: str,
        params: Mapping[str, Any] | None = None,
        *,
        item_key: str = "items",
        **query: Any,
    ) -> Iterable[Any]:
        return self._list_iter(
            self._jobs_path(workspace_key),
            params=params,
            item_key=item_key,
            **query,
        )

    def create_job(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._create(self._jobs_path(workspace_key), details)

    def get_job(self, workspace_key: str, job_key: str) -> AIDPData:
        return self._get(self._job_path(workspace_key, job_key))

    def update_job(
        self,
        workspace_key: str,
        job_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._update(self._job_path(workspace_key, job_key), details)

    def delete_job(
        self,
        workspace_key: str,
        job_key: str,
    ) -> AIDPData:
        return self._delete(self._job_path(workspace_key, job_key))

    def job_permissions(
        self,
        workspace_key: str,
        job_key: str,
    ) -> AIDPData:
        return self._get(f"{self._job_path(workspace_key, job_key)}/permissions")

    def manage_job_permissions(
        self,
        workspace_key: str,
        job_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._action(
            f"{self._job_path(workspace_key, job_key)}/actions/managePermission",
            details,
        )

    def cancel_job_runs(
        self,
        workspace_key: str,
        job_key: str,
        details: Mapping[str, Any] | None = None,
    ) -> AIDPData:
        return self._action(
            f"{self._job_path(workspace_key, job_key)}/actions/cancelJobRuns",
            details,
        )

    def list_job_runs(
        self,
        workspace_key: str,
        params: Mapping[str, Any] | None = None,
        **query: Any,
    ) -> AIDPData:
        return self._list(self._job_runs_path(workspace_key), params=params, **query)

    def list_job_runs_iter(
        self,
        workspace_key: str,
        params: Mapping[str, Any] | None = None,
        *,
        item_key: str = "items",
        **query: Any,
    ) -> Iterable[Any]:
        return self._list_iter(
            self._job_runs_path(workspace_key),
            params=params,
            item_key=item_key,
            **query,
        )

    def recent_job_runs(
        self,
        workspace_key: str,
        params: Mapping[str, Any] | None = None,
        **query: Any,
    ) -> AIDPData:
        return self._list(
            f"/workspaces/{path_param(workspace_key)}/recentJobRuns",
            params=params,
            **query,
        )

    def create_job_run(
        self,
        workspace_key: str,
        details: Mapping[str, Any],
    ) -> AIDPData:
        return self._create(self._job_runs_path(workspace_key), details)

    def get_job_run(
        self,
        workspace_key: str,
        job_run_key: str,
    ) -> AIDPData:
        return self._get(self._job_run_path(workspace_key, job_run_key))

    def delete_job_run(
        self,
        workspace_key: str,
        job_run_key: str,
    ) -> AIDPData:
        return self._delete(self._job_run_path(workspace_key, job_run_key))

    def cancel_job_run(
        self,
        workspace_key: str,
        job_run_key: str,
        details: Mapping[str, Any] | None = None,
    ) -> AIDPData:
        return self._action(
            f"{self._job_run_path(workspace_key, job_run_key)}/actions/cancel",
            details,
        )

    def repair_job_run(
        self,
        workspace_key: str,
        job_run_key: str,
        details: Mapping[str, Any] | None = None,
    ) -> AIDPData:
        return self._action(
            f"{self._job_run_path(workspace_key, job_run_key)}/actions/repair",
            details,
        )

    def list_task_runs(
        self,
        workspace_key: str,
        params: Mapping[str, Any] | None = None,
        **query: Any,
    ) -> AIDPData:
        return self._list(self._task_runs_path(workspace_key), params=params, **query)

    def get_task_run(
        self,
        workspace_key: str,
        task_run_key: str,
    ) -> AIDPData:
        return self._get(f"{self._task_runs_path(workspace_key)}/{path_param(task_run_key)}")

    def fetch_task_run_output(
        self,
        workspace_key: str,
        task_run_key: str,
        details: Mapping[str, Any] | None = None,
    ) -> AIDPData:
        return self._action(
            f"{self._task_runs_path(workspace_key)}/{path_param(task_run_key)}/actions/fetchOutput",
            details,
        )

    def export_task_run_output(
        self,
        workspace_key: str,
        task_run_key: str,
        task_run_output_key: str,
        details: Mapping[str, Any] | None = None,
    ) -> AIDPData:
        return self._action(
            f"{self._task_runs_path(workspace_key)}/{path_param(task_run_key)}"
            f"/outputs/{path_param(task_run_output_key)}/actions/export",
            details,
        )

    @staticmethod
    def _jobs_path(workspace_key: str) -> str:
        return f"/workspaces/{path_param(workspace_key)}/jobs"

    @classmethod
    def _job_path(cls, workspace_key: str, job_key: str) -> str:
        return f"{cls._jobs_path(workspace_key)}/{path_param(job_key)}"

    @staticmethod
    def _job_runs_path(workspace_key: str) -> str:
        return f"/workspaces/{path_param(workspace_key)}/jobRuns"

    @classmethod
    def _job_run_path(cls, workspace_key: str, job_run_key: str) -> str:
        return f"{cls._job_runs_path(workspace_key)}/{path_param(job_run_key)}"

    @staticmethod
    def _task_runs_path(workspace_key: str) -> str:
        return f"/workspaces/{path_param(workspace_key)}/taskRuns"
