from brain.graph.extraction.relationship_extractor import (
    RelationshipExtractor,
)
from brain.graph.storage.graph_store import GraphStore
from brain.models.document import Document


class RelationshipPipeline:
    """
    Builds relationships between knowledge entities.
    """

    def __init__(
        self,
        extractor: RelationshipExtractor,
        store: GraphStore,
    ):
        self._extractor = extractor
        self._store = store

    def process(
        self,
        document: Document,
    ) -> None:

        nodes = list(
            self._store.graph.nodes.values()
        )

        edges = self._extractor.extract(
            document.content,
            nodes,
        )

        for edge in edges:
            self._store.add_edge(edge)