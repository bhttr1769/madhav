from pathlib import Path

from brain.graph.persistence.graph_serializer import (
    GraphSerializer,
)
from brain.graph.storage.graph_store import GraphStore


class GraphManager:
    """
    Manages graph persistence.
    """

    def __init__(
        self,
        path: str | Path,
    ):

        self._path = Path(path)

    def save(
        self,
        store: GraphStore,
    ) -> None:

        GraphSerializer.save(
            store.graph,
            self._path,
        )

    def load(
        self,
    ) -> GraphStore:

        store = GraphStore()

        if not self._path.exists():

            return store

        store._graph = GraphSerializer.load(
            self._path,
        )

        return store