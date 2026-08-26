from brain.graph.models.edge import (
    Edge,
)

from brain.graph.models.node import (
    Node,
)

from brain.graph.storage.graph_store import (
    GraphStore,
)

from brain.ui.models.screen_understanding import (
    ScreenUnderstanding,
)


class UIGraphBuilder:
    """
    Converts screen understanding into graph knowledge.
    """

    def build(
        self,
        understanding: ScreenUnderstanding,
    ) -> GraphStore:

        graph = GraphStore()

        screen_id = "screen"

        graph.add_node(
            Node(
                id=screen_id,
                name="Screen",
                type="screen",
                metadata={
                    "width": understanding.screen.width,
                    "height": understanding.screen.height,
                    "image_path": (
                        understanding.screen.image_path
                    ),
                },
            )
        )

        if understanding.application is not None:

            application_id = (
                f"application:"
                f"{understanding.application}"
            )

            graph.add_node(
                Node(
                    id=application_id,
                    name=understanding.application,
                    type="application",
                )
            )

            graph.add_edge(
                Edge(
                    id="screen-application",
                    source=screen_id,
                    target=application_id,
                    relation="displays",
                )
            )

        if understanding.window_title is not None:

            window_id = (
                f"window:"
                f"{understanding.window_title}"
            )

            graph.add_node(
                Node(
                    id=window_id,
                    name=understanding.window_title,
                    type="window",
                )
            )

            graph.add_edge(
                Edge(
                    id="screen-window",
                    source=screen_id,
                    target=window_id,
                    relation="contains",
                )
            )

        for index, element in enumerate(
            sorted(
                understanding.elements,
                key=lambda item: (
                    item.y,
                    item.x,
                    item.name,
                ),
            )
        ):

            element_id = (
                f"ui-element:{index}"
            )

            graph.add_node(
                Node(
                    id=element_id,
                    name=element.name,
                    type=element.element_type,
                    metadata={
                        "x": element.x,
                        "y": element.y,
                        "width": element.width,
                        "height": element.height,
                        "text": element.text,
                        "confidence": (
                            element.confidence
                        ),
                    },
                )
            )

            graph.add_edge(
                Edge(
                    id=(
                        f"screen-contains-"
                        f"{index}"
                    ),
                    source=screen_id,
                    target=element_id,
                    relation="contains",
                )
            )

        return graph