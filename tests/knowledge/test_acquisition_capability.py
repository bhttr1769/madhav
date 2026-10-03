from unittest.mock import MagicMock

import pytest

from brain.browser.integrations.browser_knowledge_integrator import (
    BrowserKnowledgeIntegrator,
)
from brain.knowledge.acquisition_capability import (
    AcquisitionCapability,
)
from brain.manager import BrainManager
from brain.models.document import Document


def create_document(
    name: str = "example.html",
) -> Document:
    from datetime import datetime
    from pathlib import Path

    timestamp = datetime.now()

    return Document(
        name=name,
        path=Path("test"),
        extension=".html",
        content="test content",
        size=12,
        created_at=timestamp,
        modified_at=timestamp,
        language="unknown",
        source="test",
    )


def create_capability():
    browser_integrator = MagicMock(
        spec=BrowserKnowledgeIntegrator
    )

    brain_manager = MagicMock(
        spec=BrainManager
    )

    capability = AcquisitionCapability(
        browser_integrator=browser_integrator,
        brain_manager=brain_manager,
    )

    return (
        capability,
        browser_integrator,
        brain_manager,
    )


def test_descriptor_has_expected_id():
    capability, _, _ = create_capability()

    descriptor = capability.capability_descriptor()

    assert descriptor.id == "knowledge.acquisition"


def test_descriptor_has_expected_entry_point():
    capability, _, _ = create_capability()

    descriptor = capability.capability_descriptor()

    assert (
        descriptor.entry_point
        == (
            "brain.knowledge.acquisition_capability."
            "AcquisitionCapability"
        )
    )


def test_browser_acquisition_delegates_exact_url():
    (
        capability,
        browser_integrator,
        _,
    ) = create_capability()

    document = create_document()

    browser_integrator.learn.return_value = document

    result = capability.execute(
        {
            "source": "browser",
            "url": "https://example.com",
        }
    )

    browser_integrator.learn.assert_called_once_with(
        "https://example.com"
    )

    assert result is document


def test_browser_acquisition_returns_integrator_document():
    (
        capability,
        browser_integrator,
        _,
    ) = create_capability()

    document = create_document()

    browser_integrator.learn.return_value = document

    result = capability.execute(
        {
            "source": "browser",
            "url": "https://example.com",
        }
    )

    assert result is document


def test_file_acquisition_reads_file():
    (
        capability,
        _,
        brain_manager,
    ) = create_capability()

    document = create_document(
        name="example.txt"
    )

    brain_manager.read.return_value = document
    brain_manager.learn_document.return_value = document

    capability.execute(
        {
            "source": "file",
            "path": "example.txt",
        }
    )

    brain_manager.read.assert_called_once_with(
        "example.txt"
    )


def test_file_acquisition_passes_read_document_to_learning():
    (
        capability,
        _,
        brain_manager,
    ) = create_capability()

    document = create_document(
        name="example.txt"
    )

    brain_manager.read.return_value = document
    brain_manager.learn_document.return_value = document

    capability.execute(
        {
            "source": "file",
            "path": "example.txt",
        }
    )

    brain_manager.learn_document.assert_called_once_with(
        document
    )


def test_file_acquisition_returns_learned_document():
    (
        capability,
        _,
        brain_manager,
    ) = create_capability()

    document = create_document(
        name="example.txt"
    )

    brain_manager.read.return_value = document
    brain_manager.learn_document.return_value = document

    result = capability.execute(
        {
            "source": "file",
            "path": "example.txt",
        }
    )

    assert result is document


def test_unsupported_source_is_rejected():
    capability, _, _ = create_capability()

    with pytest.raises(
        ValueError,
        match="unsupported acquisition source",
    ):
        capability.execute(
            {
                "source": "unknown",
            }
        )


def test_missing_source_is_rejected():
    capability, _, _ = create_capability()

    with pytest.raises(
        TypeError,
        match="source must be a string",
    ):
        capability.execute({})


def test_empty_source_is_rejected():
    capability, _, _ = create_capability()

    with pytest.raises(
        ValueError,
        match="source must not be empty",
    ):
        capability.execute(
            {
                "source": "   ",
            }
        )


def test_non_dict_input_is_rejected():
    capability, _, _ = create_capability()

    with pytest.raises(
        TypeError,
        match="input_data must be a dict",
    ):
        capability.execute("browser")


def test_browser_requires_url():
    capability, _, _ = create_capability()

    with pytest.raises(
        TypeError,
        match="browser acquisition requires",
    ):
        capability.execute(
            {
                "source": "browser",
            }
        )


def test_file_requires_path():
    capability, _, _ = create_capability()

    with pytest.raises(
        TypeError,
        match="file acquisition requires",
    ):
        capability.execute(
            {
                "source": "file",
            }
        )


def test_invalid_browser_integrator_is_rejected():
    brain_manager = MagicMock(
        spec=BrainManager
    )

    with pytest.raises(
        TypeError,
        match="browser_integrator",
    ):
        AcquisitionCapability(
            browser_integrator=object(),
            brain_manager=brain_manager,
        )


def test_invalid_brain_manager_is_rejected():
    browser_integrator = MagicMock(
        spec=BrowserKnowledgeIntegrator
    )

    with pytest.raises(
        TypeError,
        match="brain_manager",
    ):
        AcquisitionCapability(
            browser_integrator=browser_integrator,
            brain_manager=object(),
        )


def test_browser_failure_is_propagated():
    (
        capability,
        browser_integrator,
        _,
    ) = create_capability()

    error = RuntimeError(
        "browser acquisition failed"
    )

    browser_integrator.learn.side_effect = error

    with pytest.raises(
        RuntimeError,
        match="browser acquisition failed",
    ):
        capability.execute(
            {
                "source": "browser",
                "url": "https://example.com",
            }
        )


def test_file_read_failure_is_propagated():
    (
        capability,
        _,
        brain_manager,
    ) = create_capability()

    brain_manager.read.side_effect = RuntimeError(
        "file read failed"
    )

    with pytest.raises(
        RuntimeError,
        match="file read failed",
    ):
        capability.execute(
            {
                "source": "file",
                "path": "example.txt",
            }
        )


def test_file_learning_failure_is_propagated():
    (
        capability,
        _,
        brain_manager,
    ) = create_capability()

    document = create_document(
        name="example.txt"
    )

    brain_manager.read.return_value = document

    brain_manager.learn_document.side_effect = (
        RuntimeError("learning failed")
    )

    with pytest.raises(
        RuntimeError,
        match="learning failed",
    ):
        capability.execute(
            {
                "source": "file",
                "path": "example.txt",
            }
        )


def test_file_acquisition_preserves_call_order():
    (
        capability,
        _,
        brain_manager,
    ) = create_capability()

    document = create_document(
        name="example.txt"
    )

    brain_manager.read.return_value = document
    brain_manager.learn_document.return_value = document

    capability.execute(
        {
            "source": "file",
            "path": "example.txt",
        }
    )

    assert brain_manager.method_calls == [
        ("read", ("example.txt",), {}),
        ("learn_document", (document,), {}),
    ]