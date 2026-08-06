from brain.graph.extraction.entity_extractor import EntityExtractor
from brain.graph.models.node import Node


class RuleBasedEntityExtractor(EntityExtractor):
    """
    Simple rule-based entity extractor.
    """

    KNOWN_ENTITIES = {
        "Java": "language",
        "Spring Boot": "framework",
        "Maven": "tool",
        "Docker": "tool",
        "PostgreSQL": "database",
    }

    def extract(
        self,
        text: str,
    ) -> list[Node]:

        nodes = []

        for name, entity_type in self.KNOWN_ENTITIES.items():

            if name in text:

                node = Node(
                    id=name.lower().replace(" ", "_"),
                    name=name,
                    type=entity_type,
                )

                nodes.append(node)

        return nodes