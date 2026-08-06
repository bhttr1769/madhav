from datetime import datetime
from pathlib import Path

from brain.graph.extraction.rule_based_entity_extractor import (
    RuleBasedEntityExtractor,
)
from brain.graph.extraction.rule_based_relationship_extractor import (
    RuleBasedRelationshipExtractor,
)
from brain.graph.pipeline.entity_pipeline import EntityPipeline
from brain.graph.pipeline.relationship_pipeline import (
    RelationshipPipeline,
)
from brain.graph.storage.graph_store import GraphStore
from brain.models.document import Document


def test_relationship_pipeline():

    store = GraphStore()

    document = Document(
        name="sample.txt",
        path=Path("sample.txt"),
        extension=".txt",
        content="Java uses Spring Boot.",
        size=0,
        created_at=datetime.now(),
        modified_at=datetime.now(),
    )

    EntityPipeline(
        RuleBasedEntityExtractor(),
        store,
    ).process(document)

    RelationshipPipeline(
        RuleBasedRelationshipExtractor(),
        store,
    ).process(document)

    assert len(store.graph.edges) == 1

    edge = next(iter(store.graph.edges.values()))

    assert edge.source == "java"

    assert edge.target == "spring_boot"

    assert edge.relation == "USES"