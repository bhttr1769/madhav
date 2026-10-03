from brain.browser.integrations.browser_document_adapter import (
    BrowserDocumentAdapter,
)
from brain.browser.pipelines.browser_learning_pipeline import (
    BrowserLearningPipeline,
)
from brain.manager import BrainManager
from brain.models.document import Document


class BrowserKnowledgeIntegrator:
    """
    Integrates browser-acquired content with the existing
    Brain knowledge pipeline.
    """

    def __init__(
        self,
        browser_pipeline: BrowserLearningPipeline,
        document_adapter: BrowserDocumentAdapter,
        brain_manager: BrainManager,
    ):
        self._browser_pipeline = browser_pipeline
        self._document_adapter = document_adapter
        self._brain_manager = brain_manager

    def learn(
        self,
        url: str,
    ) -> Document:
        content = self._browser_pipeline.learn(url)

        document = self._document_adapter.to_document(
            url=url,
            content=content,
        )

        return self._brain_manager.learn_document(
            document
        )