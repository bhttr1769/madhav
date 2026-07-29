from brain.chunking.base_chunker import BaseChunker
from brain.factories.chunker_factory import ChunkerFactory

class ChunkerRegistry:
    """
    Stores and provides the active chunking strategy.
    """

    def __init__(self) -> None:
        self._chunker: BaseChunker = ChunkerFactory.create_default()

    def get_chunker(self) -> BaseChunker:
        return self._chunker

    def set_chunker(self, chunker: BaseChunker) -> None:
        self._chunker = chunker