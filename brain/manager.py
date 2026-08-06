from pathlib import Path

from brain.models.document import Document
from brain.config.brain_config import BrainConfig
from brain.search.models.search_query import SearchQuery


class BrainManager:
    """
    Central entry point for reading and parsing documents.
    """

    def __init__(self, config: BrainConfig) -> None:
        self._config = config

    def read(self, file_path: Path | str) -> Document:
        file_path = Path(file_path)

        reader = self._config.reader_registry.get_reader(file_path)

        document = reader.read(file_path)

        parser = self._config.parser_registry.get_parser(file_path)

        document = parser.parse(document)

        chunker = self._config.chunker_registry.get_chunker()

        document.chunks = chunker.chunk(document)

        document = self._config.embedding_pipeline.process(document)

        return document
    
    def learn(
        self,
        file_path: Path | str,
        ) -> Document:
        """
        Learn a document by reading, processing,
        and storing it in semantic memory.
        """

        document = self.read(file_path)

        self._config.memory_pipeline.ingest(document)
        
        self._config.entity_pipeline.process(document)
        
        self._config.relationship_pipeline.process(document)

        return document
    
    def search(
        self,
        text: str,
        ):

        query = SearchQuery(text)

        return self._config.semantic_searcher.search(
            query
        )
        
    def ask(
        self,
        question: str,
    ) -> str:

        return self._config.rag_service.ask(
            question
        )