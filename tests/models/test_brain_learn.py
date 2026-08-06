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


class FakeEntityPipeline:
    def process(self, document):
        pass

class FakeRelationshipPipeline:

    def __init__(self):
        self.called = False

    def process(self, document):
        self.called = True

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
    relationship_pipeline = FakeRelationshipPipeline()

    config = BrainConfig(
        reader_registry=ReaderRegistry(),
        parser_registry=ParserRegistry(),
        chunker_registry=ChunkerRegistry(),
        embedding_pipeline=FakeEmbeddingPipeline(),
        memory_pipeline=memory,
        semantic_searcher=FakeSearcher(),
        entity_pipeline=FakeEntityPipeline(),
        relationship_pipeline=relationship_pipeline,
    )

    brain = FakeBrain(config)

    brain.learn("sample.txt")

    assert memory.ingested

    assert relationship_pipeline.called