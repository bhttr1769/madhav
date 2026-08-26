from brain.ui.models.screen import (
    Screen,
)

from brain.ui.models.screen_understanding import (
    ScreenUnderstanding,
)

from brain.ui.models.ui_element import (
    UIElement,
)

from brain.ui.ui_graph_builder import (
    UIGraphBuilder,
)


def test_ui_graph_builder_creates_screen():

    understanding = ScreenUnderstanding(
        screen=Screen(
            width=1920,
            height=1080,
            image_path="screen.png",
        ),
        elements=frozenset(),
        application=None,
        window_title=None,
    )

    graph = UIGraphBuilder().build(
        understanding,
    )

    node = graph.graph.nodes[
        "screen"
    ]

    assert node.name == "Screen"
    assert node.type == "screen"
    assert node.metadata["width"] == 1920
    assert node.metadata["height"] == 1080
    assert node.metadata["image_path"] == (
        "screen.png"
    )


def test_ui_graph_builder_creates_elements():

    button = UIElement(
        element_type="button",
        name="Submit",
        x=100,
        y=200,
        width=120,
        height=40,
        text="Submit",
        confidence=0.95,
    )

    understanding = ScreenUnderstanding(
        screen=Screen(
            width=1920,
            height=1080,
        ),
        elements=frozenset({
            button,
        }),
        application=None,
        window_title=None,
    )

    graph = UIGraphBuilder().build(
        understanding,
    )

    node = graph.graph.nodes[
        "ui-element:0"
    ]

    assert node.name == "Submit"
    assert node.type == "button"
    assert node.metadata["x"] == 100
    assert node.metadata["y"] == 200
    assert node.metadata["width"] == 120
    assert node.metadata["height"] == 40
    assert node.metadata["text"] == "Submit"
    assert node.metadata["confidence"] == 0.95


def test_ui_graph_builder_connects_elements():

    element = UIElement(
        element_type="button",
        name="Submit",
        x=100,
        y=200,
        width=120,
        height=40,
    )

    understanding = ScreenUnderstanding(
        screen=Screen(
            width=1920,
            height=1080,
        ),
        elements=frozenset({
            element,
        }),
        application=None,
        window_title=None,
    )

    graph = UIGraphBuilder().build(
        understanding,
    )

    edge = graph.graph.edges[
        "screen-contains-0"
    ]

    assert edge.source == "screen"
    assert edge.target == "ui-element:0"
    assert edge.relation == "contains"


def test_ui_graph_builder_creates_application():

    understanding = ScreenUnderstanding(
        screen=Screen(
            width=1920,
            height=1080,
        ),
        elements=frozenset(),
        application="Chrome",
        window_title=None,
    )

    graph = UIGraphBuilder().build(
        understanding,
    )

    node = graph.graph.nodes[
        "application:Chrome"
    ]

    assert node.name == "Chrome"
    assert node.type == "application"

    edge = graph.graph.edges[
        "screen-application"
    ]

    assert edge.source == "screen"
    assert edge.target == "application:Chrome"
    assert edge.relation == "displays"


def test_ui_graph_builder_creates_window():

    understanding = ScreenUnderstanding(
        screen=Screen(
            width=1920,
            height=1080,
        ),
        elements=frozenset(),
        application=None,
        window_title="Madhav",
    )

    graph = UIGraphBuilder().build(
        understanding,
    )

    node = graph.graph.nodes[
        "window:Madhav"
    ]

    assert node.name == "Madhav"
    assert node.type == "window"

    edge = graph.graph.edges[
        "screen-window"
    ]

    assert edge.source == "screen"
    assert edge.target == "window:Madhav"
    assert edge.relation == "contains"