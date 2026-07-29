from brain.chunking.base_chunker import BaseChunker
from brain.models.chunk import Chunk
from brain.models.document import Document
from brain.config.chunking_config import ChunkingConfig


class FixedChunker(BaseChunker):
    """
    Splits documents into fixed-size character chunks.
    """

    def __init__(self, config: ChunkingConfig):
        self._config = config

    def chunk(self, document: Document) -> list[Chunk]:

        chunks: list[Chunk] = []

        text = document.content

        chunk_id = 0

        for start in range(0, len(text), self._config.chunk_size):

            end = min(start + self._config.chunk_size, len(text))

            chunk_text = text[start:end]

            chunks.append(
                Chunk(
                    id=chunk_id,
                    text=chunk_text,
                    start_char=start,
                    end_char=end,
                    token_count=len(chunk_text.split()),
                )
            )

            chunk_id += 1

        return chunks