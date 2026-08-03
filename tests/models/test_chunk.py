from brain.models.chunk import Chunk


def test_chunk_creation():

    chunk = Chunk(
        id=1,
        text="Hello Madhav!",
        start_char=0,
        end_char=13,
        token_count=2,
    )

    assert chunk.id == 1
    assert chunk.text == "Hello Madhav!"
    assert chunk.start_char == 0
    assert chunk.end_char == 13
    assert chunk.token_count == 2
    assert chunk.embedding is None
    assert chunk.metadata == {}