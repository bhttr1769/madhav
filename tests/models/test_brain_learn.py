from pathlib import Path

from brain.config.brain_config import BrainConfig
from brain.manager import BrainManager
from brain.models.document import Document
from brain.registry.chunker_registry import ChunkerRegistry
from brain.registry.parser_registry import ParserRegistry
from brain.registry.reader_registry import ReaderRegistry


class FakeEmbeddingPipeline:
    def process(self, document):
        return document


class FakeMemoryPipeline:

    def __init__(self):
        self.ingested = False

    def ingest(self, document):
        self.ingested = True


class FakeSearcher:

    def search(self, query):
        return []


class FakeBrain(BrainManager):

    def read(self, file_path):
        return Document(
            name="sample.txt",
            path=Path("sample.txt"),
            extension=".txt",
            content="Hello",
            size=5,
            created_at=None,
            modified_at=None,
        )


def test_brain_learn():

    memory = FakeMemoryPipeline()

    config = BrainConfig(
        reader_registry=ReaderRegistry(),
        parser_registry=ParserRegistry(),
        chunker_registry=ChunkerRegistry(),
        embedding_pipeline=FakeEmbeddingPipeline(),
        memory_pipeline=memory,
        semantic_searcher=FakeSearcher(),
    )

    brain = FakeBrain(config)

    brain.learn("sample.txt")

    assert memory.ingested