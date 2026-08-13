from brain.config.brain_config import BrainConfig
from brain.manager import BrainManager
from brain.registry.chunker_registry import ChunkerRegistry
from brain.registry.parser_registry import ParserRegistry
from brain.registry.reader_registry import ReaderRegistry
from tests.utils.fake_rag_service import FakeRagService


class FakeEmbeddingPipeline:
    def process(self, document):
        return document


class FakeMemoryPipeline:
    def ingest(self, document):
        pass
    
class FakeMemoryManager:

    def save(self, store):
        pass


class FakeMemoryRuntime:

    def __init__(self):

        self.store = None

        self.manager = FakeMemoryManager()    


class FakeSearcher:
    def search(self, query):
        return []


class FakeEntityPipeline:
    def __init__(self):
        self.called = False
    def process(self, document):
        self.called = True


class FakeRelationshipPipeline:
    def __init__(self):
        self.called = False
    def process(self, document):
        self.called = True


def test_brain_learn_calls_entity_pipeline():

    entity_pipeline = FakeEntityPipeline()
    relationship_pipeline = FakeRelationshipPipeline()

    config = BrainConfig(
        reader_registry=ReaderRegistry(),
        parser_registry=ParserRegistry(),
        chunker_registry=ChunkerRegistry(),
        embedding_pipeline=FakeEmbeddingPipeline(),
        memory_pipeline=FakeMemoryPipeline(),
        memory_runtime=FakeMemoryRuntime(),
        semantic_searcher=FakeSearcher(),
        entity_pipeline=entity_pipeline,
        relationship_pipeline=relationship_pipeline,
        rag_service=FakeRagService(),
    )

    brain = BrainManager(config)

    brain.learn(
        "tests/models/sample.txt"
    )

    assert entity_pipeline.called
    assert relationship_pipeline.called