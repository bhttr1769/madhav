from pathlib import Path
from unittest.mock import MagicMock

from brain.browser.integrations.browser_document_adapter import (
    BrowserDocumentAdapter,
)
from brain.browser.integrations.browser_knowledge_integrator import (
    BrowserKnowledgeIntegrator,
)
from brain.browser.pipelines.browser_learning_pipeline import (
    BrowserLearningPipeline,
)
from brain.manager import BrainManager
from brain.models.document import Document


def create_document() -> Document:
    return Document(
        name="example.com",
        path=Path("example.com.html"),
        extension=".html",
        content="Example content",
        size=15,
        created_at=MagicMock(),
        modified_at=MagicMock(),
    )


class TestBrowserKnowledgeIntegrator:

    def test_learn_acquires_content_from_browser_pipeline(self):
        browser_pipeline = MagicMock(spec=BrowserLearningPipeline)
        adapter = MagicMock(spec=BrowserDocumentAdapter)
        brain_manager = MagicMock(spec=BrainManager)

        content = "cleaned browser content"
        document = create_document()

        browser_pipeline.learn.return_value = content
        adapter.to_document.return_value = document
        brain_manager.learn_document.return_value = document

        integrator = BrowserKnowledgeIntegrator(
            browser_pipeline=browser_pipeline,
            document_adapter=adapter,
            brain_manager=brain_manager,
        )

        url = "https://example.com"

        integrator.learn(url)

        browser_pipeline.learn.assert_called_once_with(url)

    def test_learn_passes_browser_content_to_document_adapter(self):
        browser_pipeline = MagicMock(spec=BrowserLearningPipeline)
        adapter = MagicMock(spec=BrowserDocumentAdapter)
        brain_manager = MagicMock(spec=BrainManager)

        content = "cleaned browser content"
        document = create_document()

        browser_pipeline.learn.return_value = content
        adapter.to_document.return_value = document
        brain_manager.learn_document.return_value = document

        integrator = BrowserKnowledgeIntegrator(
            browser_pipeline=browser_pipeline,
            document_adapter=adapter,
            brain_manager=brain_manager,
        )

        url = "https://example.com"

        integrator.learn(url)

        adapter.to_document.assert_called_once_with(
            url=url,
            content=content,
        )

    def test_learn_passes_document_to_brain_manager(self):
        browser_pipeline = MagicMock(spec=BrowserLearningPipeline)
        adapter = MagicMock(spec=BrowserDocumentAdapter)
        brain_manager = MagicMock(spec=BrainManager)

        content = "cleaned browser content"
        document = create_document()

        browser_pipeline.learn.return_value = content
        adapter.to_document.return_value = document
        brain_manager.learn_document.return_value = document

        integrator = BrowserKnowledgeIntegrator(
            browser_pipeline=browser_pipeline,
            document_adapter=adapter,
            brain_manager=brain_manager,
        )

        integrator.learn("https://example.com")

        brain_manager.learn_document.assert_called_once_with(
            document
        )

    def test_learn_returns_learned_document(self):
        browser_pipeline = MagicMock(spec=BrowserLearningPipeline)
        adapter = MagicMock(spec=BrowserDocumentAdapter)
        brain_manager = MagicMock(spec=BrainManager)

        content = "cleaned browser content"
        document = create_document()

        browser_pipeline.learn.return_value = content
        adapter.to_document.return_value = document
        brain_manager.learn_document.return_value = document

        integrator = BrowserKnowledgeIntegrator(
            browser_pipeline=browser_pipeline,
            document_adapter=adapter,
            brain_manager=brain_manager,
        )

        result = integrator.learn("https://example.com")

        assert result is document

    def test_learn_preserves_pipeline_order(self):
        browser_pipeline = MagicMock(spec=BrowserLearningPipeline)
        adapter = MagicMock(spec=BrowserDocumentAdapter)
        brain_manager = MagicMock(spec=BrainManager)

        content = "cleaned browser content"
        document = create_document()

        browser_pipeline.learn.return_value = content
        adapter.to_document.return_value = document
        brain_manager.learn_document.return_value = document

        integrator = BrowserKnowledgeIntegrator(
            browser_pipeline=browser_pipeline,
            document_adapter=adapter,
            brain_manager=brain_manager,
        )

        integrator.learn("https://example.com")

        assert (
            browser_pipeline.learn.call_count == 1
            and adapter.to_document.call_count == 1
            and brain_manager.learn_document.call_count == 1
        )

        browser_call = browser_pipeline.learn.call_args
        adapter_call = adapter.to_document.call_args
        manager_call = brain_manager.learn_document.call_args

        assert browser_call is not None
        assert adapter_call is not None
        assert manager_call is not None

    def test_browser_failure_stops_integration(self):
        browser_pipeline = MagicMock(spec=BrowserLearningPipeline)
        adapter = MagicMock(spec=BrowserDocumentAdapter)
        brain_manager = MagicMock(spec=BrainManager)

        error = RuntimeError("browser acquisition failed")
        browser_pipeline.learn.side_effect = error

        integrator = BrowserKnowledgeIntegrator(
            browser_pipeline=browser_pipeline,
            document_adapter=adapter,
            brain_manager=brain_manager,
        )

        try:
            integrator.learn("https://example.com")
            assert False
        except RuntimeError as exc:
            assert exc is error

        adapter.to_document.assert_not_called()
        brain_manager.learn_document.assert_not_called()

    def test_adapter_failure_stops_integration(self):
        browser_pipeline = MagicMock(spec=BrowserLearningPipeline)
        adapter = MagicMock(spec=BrowserDocumentAdapter)
        brain_manager = MagicMock(spec=BrainManager)

        content = "cleaned browser content"
        error = RuntimeError("document adaptation failed")

        browser_pipeline.learn.return_value = content
        adapter.to_document.side_effect = error

        integrator = BrowserKnowledgeIntegrator(
            browser_pipeline=browser_pipeline,
            document_adapter=adapter,
            brain_manager=brain_manager,
        )

        try:
            integrator.learn("https://example.com")
            assert False
        except RuntimeError as exc:
            assert exc is error

        brain_manager.learn_document.assert_not_called()

    def test_brain_manager_failure_propagates(self):
        browser_pipeline = MagicMock(spec=BrowserLearningPipeline)
        adapter = MagicMock(spec=BrowserDocumentAdapter)
        brain_manager = MagicMock(spec=BrainManager)

        content = "cleaned browser content"
        document = create_document()
        error = RuntimeError("knowledge integration failed")

        browser_pipeline.learn.return_value = content
        adapter.to_document.return_value = document
        brain_manager.learn_document.side_effect = error

        integrator = BrowserKnowledgeIntegrator(
            browser_pipeline=browser_pipeline,
            document_adapter=adapter,
            brain_manager=brain_manager,
        )

        try:
            integrator.learn("https://example.com")
            assert False
        except RuntimeError as exc:
            assert exc is error