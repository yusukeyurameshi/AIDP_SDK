"""Pagination helpers for Oracle-style page tokens."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from typing import Any

from .transport import AIDPResponse

PageFetcher = Callable[[str | None], AIDPResponse | Mapping[str, Any] | list[Any]]


def extract_items(payload: Any, *, item_key: str = "items") -> list[Any]:
    """Extract list items from a list response payload."""

    if payload is None:
        return []
    if isinstance(payload, list):
        return payload
    if not isinstance(payload, Mapping):
        return []

    items = payload.get(item_key)
    if items is None and item_key != "items":
        items = payload.get("items")
    if items is None:
        return []
    if isinstance(items, list):
        return items
    return list(items)


def next_page_token(payload: Any, headers: Mapping[str, str] | None = None) -> str | None:
    """Return the next page token from headers or common response body fields."""

    if headers:
        for key, value in headers.items():
            if key.lower() == "opc-next-page" and value:
                return value

    if isinstance(payload, Mapping):
        for key in ("opcNextPage", "nextPage", "next_page"):
            body_value = payload.get(key)
            if body_value:
                return str(body_value)
    return None


def iter_pages(fetch_page: PageFetcher) -> Iterable[AIDPResponse | Mapping[str, Any] | list[Any]]:
    """Iterate over pages returned by a callable accepting a page token."""

    page: str | None = None
    while True:
        response = fetch_page(page)
        yield response

        if isinstance(response, AIDPResponse):
            page = next_page_token(response.data, response.headers)
        else:
            page = next_page_token(response)

        if not page:
            break


def iter_items(fetch_page: PageFetcher, *, item_key: str = "items") -> Iterable[Any]:
    """Iterate over items across every page returned by ``fetch_page``."""

    for page in iter_pages(fetch_page):
        payload = page.data if isinstance(page, AIDPResponse) else page
        yield from extract_items(payload, item_key=item_key)
