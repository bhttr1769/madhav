from datetime import datetime
from pathlib import Path

import pytest

from brain.browser.integrations.browser_document_adapter import (
    BrowserDocumentAdapter,
)
from brain.models.document import Document


def test_converts_browser_content_to_document():
    adapter = BrowserDocumentAdapter()

    acquired_at = datetime(
        2026,
        9,
        27,
        12,
        30,
    )

    document = adapter.to_document(
        url="https://example.com/docs/page",
        content="Hello Madhav",
        acquired_at=acquired_at,
    )

    assert isinstance(document, Document)
    assert document.name == "page.html"
    assert document.path == Path(
        "browser://https://example.com/docs/page"
    )
    assert document.extension == ".html"
    assert document.content == "Hello Madhav"
    assert document.size == len(
        "Hello Madhav".encode("utf-8")
    )
    assert document.created_at == acquired_at
    assert document.modified_at == acquired_at
    assert document.language == "unknown"
    assert document.source == "browser"
    assert document.chunks == []
    assert document.metadata["source_url"] == (
        "https://example.com/docs/page"
    )


def test_root_url_uses_host_as_document_name():
    adapter = BrowserDocumentAdapter()

    document = adapter.to_document(
        url="https://example.com/",
        content="Example",
        acquired_at=datetime(2026, 9, 27),
    )

    assert document.name == "example.com"


def test_nested_url_without_extension_gets_html_extension():
    adapter = BrowserDocumentAdapter()

    document = adapter.to_document(
        url="https://example.com/articles/madhav",
        content="Article",
        acquired_at=datetime(2026, 9, 27),
    )

    assert document.name == "madhav.html"
    assert document.extension == ".html"


def test_preserves_explicit_file_extension():
    adapter = BrowserDocumentAdapter()

    document = adapter.to_document(
        url="https://example.com/docs/reference.html",
        content="Reference",
        acquired_at=datetime(2026, 9, 27),
    )

    assert document.name == "reference.html"
    assert document.extension == ".html"


def test_unicode_content_uses_utf8_byte_size():
    adapter = BrowserDocumentAdapter()

    content = "Madhav — ज्ञान"

    document = adapter.to_document(
        url="https://example.com",
        content=content,
        acquired_at=datetime(2026, 9, 27),
    )

    assert document.size == len(content.encode("utf-8"))


def test_rejects_non_string_url():
    adapter = BrowserDocumentAdapter()

    with pytest.raises(TypeError):
        adapter.to_document(
            url=123,
            content="content",
        )


def test_rejects_empty_url():
    adapter = BrowserDocumentAdapter()

    with pytest.raises(ValueError):
        adapter.to_document(
            url="   ",
            content="content",
        )


def test_rejects_invalid_url():
    adapter = BrowserDocumentAdapter()

    with pytest.raises(ValueError):
        adapter.to_document(
            url="not-a-valid-url",
            content="content",
        )


def test_rejects_non_string_content():
    adapter = BrowserDocumentAdapter()

    with pytest.raises(TypeError):
        adapter.to_document(
            url="https://example.com",
            content=123,
        )


def test_rejects_invalid_timestamp():
    adapter = BrowserDocumentAdapter()

    with pytest.raises(TypeError):
        adapter.to_document(
            url="https://example.com",
            content="content",
            acquired_at="2026-09-27",
        )