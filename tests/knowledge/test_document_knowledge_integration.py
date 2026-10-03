from pathlib import Path
from unittest.mock import MagicMock

from brain.browser.integrations.browser_document_adapter import (
    BrowserDocumentAdapter,
)
from brain.manager import BrainManager
from brain.models.document import Document


def create_config():
    config = MagicMock()

    config.memory_runtime.store.has_document.return_value = False

    config.entity_pipeline._store = MagicMock()

    return config


def create_local_document():
    return Document(
        name="test.txt",
        path=Path("test.txt"),
        extension=".txt",
        content="local content",
        size=14,
        created_at=MagicMock(),
        modified_at=MagicMock(),
        source="local",
    )


def create_browser_document():
    adapter = BrowserDocumentAdapter()

    return adapter.to_document(
        url="https://example.com",
        content="browser content",
    )


def test_local_document_uses_shared_knowledge_pipeline():
    config = create_config()
    manager = BrainManager(config)

    document = create_local_document()

    result = manager.learn_document(document)

    assert result is document

    config.memory_pipeline.ingest.assert_called_once_with(
        document
    )
    config.entity_pipeline.process.assert_called_once_with(
        document
    )
    config.relationship_pipeline.process.assert_called_once_with(
        document
    )


def test_browser_document_uses_shared_knowledge_pipeline():
    config = create_config()
    manager = BrainManager(config)

    document = create_browser_document()

    result = manager.learn_document(document)

    assert result is document

    config.memory_pipeline.ingest.assert_called_once_with(
        document
    )
    config.entity_pipeline.process.assert_called_once_with(
        document
    )
    config.relationship_pipeline.process.assert_called_once_with(
        document
    )


def test_browser_document_provenance_reaches_knowledge_pipeline():
    config = create_config()
    manager = BrainManager(config)

    document = create_browser_document()

    manager.learn_document(document)

    memory_document = (
        config.memory_pipeline.ingest.call_args.args[0]
    )
    entity_document = (
        config.entity_pipeline.process.call_args.args[0]
    )
    relationship_document = (
        config.relationship_pipeline.process.call_args.args[0]
    )

    assert memory_document is document
    assert entity_document is document
    assert relationship_document is document

    assert document.source == "browser"
    assert document.metadata["source_url"] == (
        "https://example.com"
    )


def test_local_and_browser_documents_share_same_knowledge_entry_point():
    config = create_config()
    manager = BrainManager(config)

    local_document = create_local_document()
    browser_document = create_browser_document()

    manager.learn_document(local_document)
    manager.learn_document(browser_document)

    assert config.memory_pipeline.ingest.call_count == 2
    assert config.entity_pipeline.process.call_count == 2
    assert config.relationship_pipeline.process.call_count == 2

    assert (
        config.memory_pipeline.ingest.call_args_list[0].args[0]
        is local_document
    )
    assert (
        config.memory_pipeline.ingest.call_args_list[1].args[0]
        is browser_document
    )


def test_knowledge_integration_does_not_change_document_provenance():
    config = create_config()
    manager = BrainManager(config)

    document = create_browser_document()

    manager.learn_document(document)

    assert document.source == "browser"
    assert document.path == Path(
        "browser://https://example.com"
    )
    assert document.metadata["source_url"] == (
        "https://example.com"
    )