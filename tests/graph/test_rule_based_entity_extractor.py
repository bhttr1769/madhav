from brain.graph.extraction.rule_based_entity_extractor import (
    RuleBasedEntityExtractor,
)


def test_rule_based_entity_extractor():

    extractor = RuleBasedEntityExtractor()

    nodes = extractor.extract(
        "Java is used with Spring Boot."
    )

    assert len(nodes) == 2

    assert nodes[0].name == "Java"

    assert nodes[1].name == "Spring Boot"