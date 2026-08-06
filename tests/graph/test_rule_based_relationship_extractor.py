from brain.graph.extraction.rule_based_relationship_extractor import (
    RuleBasedRelationshipExtractor,
)
from brain.graph.models.node import Node


def test_rule_based_relationship_extractor():

    extractor = RuleBasedRelationshipExtractor()

    nodes = [
        Node(
            id="java",
            name="Java",
            type="language",
        ),
        Node(
            id="spring_boot",
            name="Spring Boot",
            type="framework",
        ),
    ]

    edges = extractor.extract(
        "Java uses Spring Boot.",
        nodes,
    )

    assert len(edges) == 1

    assert edges[0].source == "java"

    assert edges[0].target == "spring_boot"

    assert edges[0].relation == "USES"