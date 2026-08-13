from brain.config.brain_config import BrainConfig
from brain.manager import BrainManager
from brain.registry.chunker_registry import ChunkerRegistry
from brain.registry.parser_registry import ParserRegistry
from brain.registry.reader_registry import ReaderRegistry
from brain.graph.persistence.graph_manager import (
    GraphManager,
)


class FakeEmbeddingPipeline:

    def process(self, document):
        return document


class FakeMemoryPipeline:

    def process(self, document):
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

    def process(self, document):
        pass


class FakeRelationshipPipeline:

    def process(self, document):
        pass


class FakeRagService:
    def __init__(self):
        self.question = None
    def ask(self, question):
        self.question = question
        return "Answer"


def test_brain_ask():

    rag = FakeRagService()

    config = BrainConfig(
        reader_registry=ReaderRegistry(),
        parser_registry=ParserRegistry(),
        chunker_registry=ChunkerRegistry(),
        embedding_pipeline=FakeEmbeddingPipeline(),
        memory_pipeline=FakeMemoryPipeline(),
        memory_runtime=FakeMemoryRuntime(),
        semantic_searcher=FakeSearcher(),
        entity_pipeline=FakeEntityPipeline(),
        relationship_pipeline=FakeRelationshipPipeline(),
        graph_manager=GraphManager("tests/data/graph.json",),
        rag_service=rag,
    )

    brain = BrainManager(config)

    answer = brain.ask("Hello")

    assert answer == "Answer"
    assert rag.question == "Hello"