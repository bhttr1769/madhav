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
                    text="Java is object-oriented.",
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


def test_rag_integration():

    chat = FakeChat()

    rag = RagService(
        searcher=FakeSearcher(),
        prompt_builder=PromptBuilder(),
        chat_service=chat,
    )

    answer = rag.ask(
        "What is Java?"
    )

    assert answer == "Answer"

    assert "Java is object-oriented." in chat.prompt

    assert "What is Java?" in chat.prompt