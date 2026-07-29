from brain.chunking.fixed_chunker import FixedChunker
from brain.config.chunking_config import ChunkingConfig


class ChunkerFactory:
    """
    Factory responsible for creating the default chunker.
    """

    @staticmethod
    def create_default() -> FixedChunker:
        return FixedChunker(
            config=ChunkingConfig()
        )