from brain.graph.models.node import (
    Node,
)


class BrowserGraphLearner:

    def __init__(
        self,
        browser_engine,
        graph_store,
    ):

        self._browser_engine = (
            browser_engine
        )

        self._graph_store = (
            graph_store
        )

    def learn(
        self,
        url,
    ):

        content = (
            self._browser_engine.learn(
                url,
            )
        )

        node = Node(
            id=url,
            name=url,
            type="document",
            metadata={
                "content": content.text,
            },
        )

        self._graph_store.add_node(
            node,
        )

        return node