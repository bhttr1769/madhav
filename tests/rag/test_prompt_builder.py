from brain.rag.prompt_builder import PromptBuilder
from brain.search.models.search_result import SearchResult
from brain.vector.models.vector import Vector
from brain.vector.models.vector_record import VectorRecord


def test_prompt_builder():

    builder = PromptBuilder()

    results = [
        SearchResult(
            record=VectorRecord(
                id="1",
                vector=Vector([0.1]),
                document_id="doc",
                chunk_id=0,
                text="Spring Boot is built using Java.",
            ),
            score=0.9,
        ),
        SearchResult(
            record=VectorRecord(
                id="2",
                vector=Vector([0.2]),
                document_id="doc",
                chunk_id=1,
                text="Maven manages dependencies.",
            ),
            score=0.8,
        ),
    ]

    prompt = builder.build(
        "What is Spring Boot built with?",
        results,
    )

    assert "Spring Boot is built using Java." in prompt
    assert "Maven manages dependencies." in prompt
    assert "What is Spring Boot built with?" in prompt