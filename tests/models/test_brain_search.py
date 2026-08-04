from brain.config.brain_config import BrainConfig
from brain.manager import BrainManager
from brain.registry.chunker_registry import ChunkerRegistry
from brain.registry.parser_registry import ParserRegistry
from brain.registry.reader_registry import ReaderRegistry


class FakeEmbeddingPipeline:
    def process(self, document):
        return document


class FakeSearcher:
    def search(self, query):
        return ["result"]
    
class FakeMemoryPipeline:
    def ingest(self, document):
        pass


def test_brain_search():

    config = BrainConfig(
        reader_registry=ReaderRegistry(),
        parser_registry=ParserRegistry(),
        chunker_registry=ChunkerRegistry(),
        embedding_pipeline=FakeEmbeddingPipeline(),
        memory_pipeline=FakeMemoryPipeline(),
        semantic_searcher=FakeSearcher(),
    )

    brain = BrainManager(config)

    results = brain.search("Hello")

    assert results == ["result"]