from brain.chunking.fixed_chunker import FixedChunker
from brain.models.document import Document


def test_fixed_chunker_creates_chunks():

    document = Document(
        name="sample.txt",
        path="sample.txt",
        extension=".txt",
        content="A" * 1200,
        size=1200,
        created_at=None,
        modified_at=None,
    )

    chunker = FixedChunker(chunk_size=500)

    chunks = chunker.chunk(document)

    assert len(chunks) == 3

    assert chunks[0].start_char == 0
    assert chunks[0].end_char == 500

    assert chunks[1].start_char == 500
    assert chunks[1].end_char == 1000

    assert chunks[2].start_char == 1000
    assert chunks[2].end_char == 1200

    assert chunks[0].id == 0
    assert chunks[1].id == 1
    assert chunks[2].id == 2