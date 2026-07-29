from dataclasses import dataclass

from brain.config.base_config import BaseConfig


@dataclass(frozen=True)
class ChunkingConfig(BaseConfig):
    """
    Configuration for chunking.
    """

    chunk_size: int = 500