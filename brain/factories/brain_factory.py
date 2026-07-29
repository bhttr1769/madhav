from brain.config.brain_config import BrainConfig
from brain.manager import BrainManager
from brain.registry.chunker_registry import ChunkerRegistry
from brain.registry.parser_registry import ParserRegistry
from brain.registry.reader_registry import ReaderRegistry


class BrainFactory:
    """
    Responsible for creating fully configured BrainManager instances.
    """

    @staticmethod
    def create() -> BrainManager:
        config = BrainConfig(
            reader_registry=ReaderRegistry(),
            parser_registry=ParserRegistry(),
            chunker_registry=ChunkerRegistry(),
        )

        return BrainManager(config)