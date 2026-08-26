from brain.graph.models.edge import (
    Edge,
)

from brain.graph.models.node import (
    Node,
)

from brain.graph.storage.graph_store import (
    GraphStore,
)

from brain.reasoning.models.decision import (
    Decision,
)


class DecisionGraphBuilder:
    """
    Converts reasoning decisions into graph knowledge.
    """

    def build(
        self,
        decision: Decision,
    ) -> GraphStore:

        graph = GraphStore()

        decision_id = "decision"

        graph.add_node(
            Node(
                id=decision_id,
                name=decision.action,
                type="decision",
                metadata={
                    "rationale": decision.rationale,
                    "confidence": decision.confidence,
                },
            )
        )

        for index, alternative in enumerate(
            sorted(
                decision.alternatives,
            )
        ):

            alternative_id = (
                f"alternative:{index}"
            )

            graph.add_node(
                Node(
                    id=alternative_id,
                    name=alternative,
                    type="alternative",
                )
            )

            graph.add_edge(
                Edge(
                    id=(
                        f"decision-alternative-"
                        f"{index}"
                    ),
                    source=decision_id,
                    target=alternative_id,
                    relation="alternative_to",
                )
            )

        return graph