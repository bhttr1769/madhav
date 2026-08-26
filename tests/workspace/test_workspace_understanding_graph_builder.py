from brain.workspace.models.workspace_context import (
    WorkspaceContext,
)

from brain.workspace.models.workspace_understanding import (
    WorkspaceUnderstanding,
)

from brain.workspace.workspace_understanding_graph_builder import (
    WorkspaceUnderstandingGraphBuilder,
)


def create_understanding():

    return WorkspaceUnderstanding(
        name="Madhav",
        root="C:/Madhav",
        files=100,
        directories=10,
        technologies=frozenset({
            "Python",
        }),
        dependencies=frozenset({
            "pytest",
        }),
        architectures=frozenset({
            "layered",
        }),
    )


def create_context():

    return WorkspaceContext(
        workspace_type="software_project",
        scale="medium",
        primary_technology="Python",
        primary_architecture="layered",
        confidence=1.0,
    )


def test_builder_creates_workspace_node():

    graph = (
        WorkspaceUnderstandingGraphBuilder()
        .build(
            create_understanding(),
            create_context(),
        )
    )

    node = graph.graph.nodes[
        "workspace"
    ]

    assert node.name == "Madhav"
    assert node.type == "workspace"

    assert node.metadata["root"] == "C:/Madhav"
    assert node.metadata["files"] == 100
    assert node.metadata["directories"] == 10


def test_builder_creates_context_node():

    graph = (
        WorkspaceUnderstandingGraphBuilder()
        .build(
            create_understanding(),
            create_context(),
        )
    )

    node = graph.graph.nodes[
        "workspace-context"
    ]

    assert node.type == "workspace_context"

    assert (
        node.metadata["workspace_type"]
        == "software_project"
    )

    assert node.metadata["scale"] == "medium"

    assert (
        node.metadata["primary_technology"]
        == "Python"
    )

    assert (
        node.metadata["primary_architecture"]
        == "layered"
    )

    assert node.metadata["confidence"] == 1.0


def test_builder_connects_context():

    graph = (
        WorkspaceUnderstandingGraphBuilder()
        .build(
            create_understanding(),
            create_context(),
        )
    )

    edge = graph.graph.edges[
        "workspace-context"
    ]

    assert edge.source == "workspace"
    assert edge.target == "workspace-context"
    assert edge.relation == "has_context"


def test_builder_creates_technology_relationship():

    graph = (
        WorkspaceUnderstandingGraphBuilder()
        .build(
            create_understanding(),
            create_context(),
        )
    )

    node = graph.graph.nodes[
        "technology:Python"
    ]

    assert node.name == "Python"
    assert node.type == "technology"

    edge = graph.graph.edges[
        "workspace-uses-Python"
    ]

    assert edge.source == "workspace"
    assert edge.target == "technology:Python"
    assert edge.relation == "uses"


def test_builder_creates_dependency_relationship():

    graph = (
        WorkspaceUnderstandingGraphBuilder()
        .build(
            create_understanding(),
            create_context(),
        )
    )

    node = graph.graph.nodes[
        "dependency:pytest"
    ]

    assert node.name == "pytest"
    assert node.type == "dependency"

    edge = graph.graph.edges[
        "workspace-depends-pytest"
    ]

    assert edge.source == "workspace"
    assert edge.target == "dependency:pytest"
    assert edge.relation == "depends_on"


def test_builder_creates_architecture_relationship():

    graph = (
        WorkspaceUnderstandingGraphBuilder()
        .build(
            create_understanding(),
            create_context(),
        )
    )

    node = graph.graph.nodes[
        "architecture:layered"
    ]

    assert node.name == "layered"
    assert node.type == "architecture"

    edge = graph.graph.edges[
        "workspace-follows-layered"
    ]

    assert edge.source == "workspace"
    assert edge.target == "architecture:layered"
    assert edge.relation == "follows"