import json
from pathlib import Path

from brain.graph.models.edge import Edge
from brain.graph.models.node import Node
from brain.graph.models.knowledge_graph import (
    KnowledgeGraph,
)


class GraphSerializer:
    """
    Saves and loads knowledge graphs.
    """

    @staticmethod
    def save(
        graph: KnowledgeGraph,
        path: str,
    ) -> None:

        data = {
            "nodes": [],
            "edges": [],
        }

        for node in graph.nodes.values():

            data["nodes"].append(
                {
                    "id": node.id,
                    "name": node.name,
                    "type": node.type,
                    "metadata": node.metadata,
                }
            )

        for edge in graph.edges.values():

            data["edges"].append(
                {
                    "id": edge.id,
                    "source": edge.source,
                    "target": edge.target,
                    "relation": edge.relation,
                    "metadata": edge.metadata,
                }
            )

        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
            )

    @staticmethod
    def load(
        path: str,
    ) -> KnowledgeGraph:

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        graph = KnowledgeGraph()

        for item in data["nodes"]:

            graph.nodes[item["id"]] = Node(
                id=item["id"],
                name=item["name"],
                type=item["type"],
                metadata=item["metadata"],
            )

        for item in data["edges"]:

            graph.edges[item["id"]] = Edge(
                id=item["id"],
                source=item["source"],
                target=item["target"],
                relation=item["relation"],
                metadata=item["metadata"],
            )

        return graph