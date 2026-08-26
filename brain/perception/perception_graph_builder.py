from brain.graph.models.edge import (
    Edge,
)

from brain.graph.models.node import (
    Node,
)

from brain.graph.storage.graph_store import (
    GraphStore,
)

from brain.perception.models.cross_modal_context import (
    CrossModalContext,
)


class PerceptionGraphBuilder:
    """
    Converts cross-modal perception context
    into knowledge graph structures.
    """

    def build(
        self,
        context: CrossModalContext,
    ) -> GraphStore:

        graph = GraphStore()

        for observation in context.observations:

            node_id = self._observation_id(
                observation,
            )

            graph.add_node(
                Node(
                    id=node_id,
                    name=observation.value,
                    type=(
                        observation.category
                    ),
                    metadata={
                        "source": observation.source,
                        "category": observation.category,
                        "subject": observation.subject,
                        "confidence": (
                            observation.confidence
                        ),
                    },
                )
            )

        for (
            source_id,
            relation,
            target_id,
        ) in context.relationships:

            graph.add_edge(
                Edge(
                    id=(
                        f"{source_id}-"
                        f"{relation}-"
                        f"{target_id}"
                    ),
                    source=source_id,
                    target=target_id,
                    relation=relation,
                )
            )

        return graph

    def _observation_id(
        self,
        observation,
    ) -> str:

        return (
            f"{observation.source}:"
            f"{observation.category}:"
            f"{observation.subject}:"
            f"{observation.value}"
        )