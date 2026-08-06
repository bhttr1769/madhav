from brain.graph.extraction.entity_extractor import EntityExtractor
from brain.graph.storage.graph_store import GraphStore
from brain.models.document import Document


class EntityPipeline:
    """
    Builds a knowledge graph from documents.
    """

    def __init__(
        self,
        extractor: EntityExtractor,
        store: GraphStore,
    ):
        self._extractor = extractor
        self._store = store

    def process(
        self,
        document: Document,
    ) -> None:
        """
        Extract entities from a document
        and store them in the graph.
        """

        nodes = self._extractor.extract(
            document.content
        )

        for node in nodes:
            self._store.add_node(node)