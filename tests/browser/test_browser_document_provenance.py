from pathlib import Path
from unittest.mock import MagicMock

from brain.browser.integrations.browser_document_adapter import (
    BrowserDocumentAdapter,
)
from brain.models.document import Document


def test_browser_document_source_is_browser():
    adapter = BrowserDocumentAdapter()

    document = adapter.to_document(
        url="https://example.com",
        content="Example content",
    )

    assert isinstance(document, Document)
    assert document.source == "browser"


def test_browser_document_preserves_url_as_provenance():
    adapter = BrowserDocumentAdapter()

    url = "https://example.com/docs/page"

    document = adapter.to_document(
        url=url,
        content="Example content",
    )

    assert document.metadata["source_url"] == url


def test_browser_document_provenance_is_distinct_from_local():
    adapter = BrowserDocumentAdapter()

    document = adapter.to_document(
        url="https://example.com",
        content="Example content",
    )

    assert document.source != "local"
    assert document.source == "browser"


def test_local_document_defaults_to_local_source():
    document = Document(
        name="test.txt",
        path=Path("test.txt"),
        extension=".txt",
        content="test content",
        size=12,
        created_at=MagicMock(),
        modified_at=MagicMock(),
    )

    assert document.source == "local"


def test_browser_provenance_survives_knowledge_integration():
    adapter = BrowserDocumentAdapter()

    document = adapter.to_document(
        url="https://example.com",
        content="Example content",
    )

    assert document.source == "browser"
    assert document.metadata["source_url"] == "https://example.com"