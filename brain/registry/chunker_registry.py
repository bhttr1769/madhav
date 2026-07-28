from brain.chunking.base_chunker import BaseChunker
from brain.chunking.fixed_chunker import FixedChunker


class ChunkerRegistry:
    """
    Stores and provides the active chunking strategy.
    """

    def __init__(self) -> None:
        self._chunker: BaseChunker = FixedChunker()

    def get_chunker(self) -> BaseChunker:
        return self._chunker

    def set_chunker(self, chunker: BaseChunker) -> None:
        self._chunker = chunker