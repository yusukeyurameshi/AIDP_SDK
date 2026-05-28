"""Generic waiters for polling asynchronous AIDP operations."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from time import monotonic
from time import sleep as default_sleep
from typing import Any

from .exceptions import AIDPWaiterError, AIDPWaiterTimeoutError

DEFAULT_STATE_KEYS = ("lifecycleState", "lifecycle_state", "state", "status", "runState")


def default_state_getter(resource: Any) -> str | None:
    """Extract a lifecycle/status value from a common response shape."""

    if isinstance(resource, Mapping):
        for key in DEFAULT_STATE_KEYS:
            value = resource.get(key)
            if value is not None:
                return str(value)
    return None


def wait_until(
    *,
    getter: Callable[[], Any],
    target_states: Iterable[str],
    failure_states: Iterable[str] = (),
    state_getter: Callable[[Any], str | None] = default_state_getter,
    interval_seconds: float = 5.0,
    max_wait_seconds: float = 600.0,
    sleep: Callable[[float], None] = default_sleep,
) -> Any:
    """Poll ``getter`` until its state reaches a target or failure state."""

    normalized_targets = {state.upper() for state in target_states}
    normalized_failures = {state.upper() for state in failure_states}
    deadline = monotonic() + max_wait_seconds
    last_resource: Any = None
    last_state: str | None = None

    while monotonic() <= deadline:
        last_resource = getter()
        last_state = state_getter(last_resource)
        normalized_state = last_state.upper() if last_state is not None else None

        if normalized_state in normalized_targets:
            return last_resource
        if normalized_state in normalized_failures:
            raise AIDPWaiterError(f"AIDP resource reached failure state {last_state!r}")

        remaining = deadline - monotonic()
        if remaining <= 0:
            break
        sleep(min(interval_seconds, remaining))

    raise AIDPWaiterTimeoutError(
        f"Timed out after {max_wait_seconds} seconds waiting for states "
        f"{sorted(normalized_targets)}; last_state={last_state!r}, "
        f"last_resource={last_resource!r}"
    )
