from brain.rag.prompt_builder import PromptBuilder
from brain.search.models.search_query import SearchQuery
from brain.search.services.semantic_searcher import SemanticSearcher


class RagService:
    """
    Retrieval-Augmented Generation service.
    """

    def __init__(
        self,
        searcher: SemanticSearcher,
        prompt_builder: PromptBuilder,
        chat_service,
    ):
        self._searcher = searcher
        self._prompt_builder = prompt_builder
        self._chat = chat_service

    def ask(
        self,
        question: str,
    ) -> str:

        results = self._searcher.search(
            SearchQuery(question)
        )

        prompt = self._prompt_builder.build(
            question,
            results,
        )

        return self._chat.chat(prompt)