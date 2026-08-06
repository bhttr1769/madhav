from datetime import datetime
from pathlib import Path

from brain.graph.extraction.rule_based_entity_extractor import (
    RuleBasedEntityExtractor,
)
from brain.graph.pipeline.entity_pipeline import EntityPipeline
from brain.graph.storage.graph_store import GraphStore
from brain.models.document import Document


def test_entity_pipeline():

    store = GraphStore()

    pipeline = EntityPipeline(
        extractor=RuleBasedEntityExtractor(),
        store=store,
    )

    document = Document(
        name="sample.txt",
        path=Path("sample.txt"),
        extension=".txt",
        content="Java uses Spring Boot.",
        size=0,
        created_at=datetime.now(),
        modified_at=datetime.now(),
    )

    pipeline.process(document)

    assert store.get_node("java") is not None

    assert store.get_node("spring_boot") is not None