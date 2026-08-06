from brain.search.models.search_result import SearchResult


class PromptBuilder:
    """
    Builds prompts using retrieved context.
    """

    def build(
        self,
        question: str,
        results: list[SearchResult],
    ) -> str:

        context = "\n\n".join(
            result.record.text
            for result in results
        )

        return (
            "Answer the question using the provided context.\n\n"
            f"Context:\n{context}\n\n"
            f"Question:\n{question}"
        )