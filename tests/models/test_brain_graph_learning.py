from brain.config.brain_config import BrainConfig
from brain.manager import BrainManager
from brain.registry.chunker_registry import ChunkerRegistry
from brain.registry.parser_registry import ParserRegistry
from brain.registry.reader_registry import ReaderRegistry
from tests.utils.fake_rag_service import FakeRagService
from brain.graph.persistence.graph_manager import (
    GraphManager,
)
from brain.graph.storage.graph_store import (
    GraphStore,
)



class FakeEmbeddingPipeline:
    def process(self, document):
        return document


class FakeMemoryPipeline:
    def ingest(self, document):
        pass
    
class FakeMemoryManager:

    def save(self, store):
        pass


class FakeStore(GraphStore):

    def has_document(
        self,
        document_id,
    ):

        return False

    def remove_document(
        self,
        document_id,
    ):

        pass


class FakeMemoryRuntime:

    def __init__(self):

        self.store = FakeStore()

        self.manager = FakeMemoryManager()   


class FakeSearcher:
    def search(self, query):
        return []


class FakeEntityPipeline:

    def __init__(self):

        self.called = False

        self._store = FakeStore()

    def process(
        self,
        document,
    ):

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
        graph_manager=GraphManager("tests/data/graph.json",),
        rag_service=FakeRagService(),
    )

    brain = BrainManager(config)

    brain.learn(
        "tests/models/sample.txt"
    )

    assert entity_pipeline.called
    assert relationship_pipeline.called