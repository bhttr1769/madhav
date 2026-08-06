from brain.rag.prompt_builder import PromptBuilder
from brain.rag.rag_service import RagService
from brain.search.models.search_result import SearchResult
from brain.vector.models.vector import Vector
from brain.vector.models.vector_record import VectorRecord


class FakeSearcher:

    def search(self, query):

        return [
            SearchResult(
                record=VectorRecord(
                    id="1",
                    vector=Vector([1.0]),
                    document_id="doc",
                    chunk_id=0,
                    text="Spring Boot uses Java.",
                ),
                score=0.95,
            )
        ]


class FakeChat:

    def __init__(self):
        self.prompt = None

    def chat(self, prompt):

        self.prompt = prompt

        return "Answer"


def test_rag_service():

    chat = FakeChat()

    rag = RagService(
        searcher=FakeSearcher(),
        prompt_builder=PromptBuilder(),
        chat_service=chat,
    )

    answer = rag.ask(
        "What does Spring Boot use?"
    )

    assert answer == "Answer"

    assert "Spring Boot uses Java." in chat.prompt

    assert "What does Spring Boot use?" in chat.prompt