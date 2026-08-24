import pytest

from brain.knowledge.builders.graph_builder import (
    GraphBuilder,
)

from brain.knowledge.models.edge_type import (
    EdgeType,
)

from brain.knowledge.models.node_type import (
    NodeType,
)

from brain.knowledge.stores.graph_store import (
    GraphStore,
)


def create_builder():

    store = GraphStore()

    builder = GraphBuilder(
        store,
    )

    return builder, store


def test_add_node():

    builder, store = (
        create_builder()
    )

    node = builder.add_node(
        node_type=NodeType.FILE,
        name="main.py",
        properties={
            "language": "python",
        },
        metadata={
            "source": "workspace",
        },
        node_id="file-1",
    )

    assert (
        node.id
        == "file-1"
    )

    assert (
        node.type
        == NodeType.FILE
    )

    assert (
        node.name
        == "main.py"
    )

    assert (
        node.properties[
            "language"
        ]
        == "python"
    )

    assert (
        store.get_node(
            "file-1",
        )
        == node
    )


def test_add_node_generates_id():

    builder, store = (
        create_builder()
    )

    node = builder.add_node(
        node_type=NodeType.PROJECT,
        name="Madhav",
    )

    assert node.id

    assert (
        store.get_node(
            node.id,
        )
        == node
    )


def test_add_node_copies_properties():

    builder, _ = (
        create_builder()
    )

    properties = {
        "language": "python",
    }

    node = builder.add_node(
        node_type=NodeType.FILE,
        name="main.py",
        properties=properties,
    )

    properties[
        "language"
    ] = "java"

    assert (
        node.properties[
            "language"
        ]
        == "python"
    )


def test_add_edge():

    builder, store = (
        create_builder()
    )

    project = builder.add_node(
        node_type=NodeType.PROJECT,
        name="Madhav",
        node_id="project-1",
    )

    file = builder.add_node(
        node_type=NodeType.FILE,
        name="main.py",
        node_id="file-1",
    )

    edge = builder.add_edge(
        source_id=project.id,
        target_id=file.id,
        edge_type=EdgeType.CONTAINS,
        edge_id="edge-1",
    )

    assert (
        edge.id
        == "edge-1"
    )

    assert (
        edge.source_id
        == "project-1"
    )

    assert (
        edge.target_id
        == "file-1"
    )

    assert (
        edge.type
        == EdgeType.CONTAINS
    )

    assert (
        store.get_edge(
            "edge-1",
        )
        == edge
    )


def test_add_edge_generates_id():

    builder, store = (
        create_builder()
    )

    source = builder.add_node(
        node_type=NodeType.FILE,
        name="main.py",
    )

    target = builder.add_node(
        node_type=NodeType.MODULE,
        name="utils",
    )

    edge = builder.add_edge(
        source_id=source.id,
        target_id=target.id,
        edge_type=EdgeType.IMPORTS,
    )

    assert edge.id

    assert (
        store.get_edge(
            edge.id,
        )
        == edge
    )


def test_add_edge_requires_source_node():

    builder, _ = (
        create_builder()
    )

    target = builder.add_node(
        node_type=NodeType.FILE,
        name="main.py",
    )

    with pytest.raises(
        ValueError,
        match="Source node does not exist",
    ):

        builder.add_edge(
            source_id="missing",
            target_id=target.id,
            edge_type=EdgeType.IMPORTS,
        )


def test_add_edge_requires_target_node():

    builder, _ = (
        create_builder()
    )

    source = builder.add_node(
        node_type=NodeType.FILE,
        name="main.py",
    )

    with pytest.raises(
        ValueError,
        match="Target node does not exist",
    ):

        builder.add_edge(
            source_id=source.id,
            target_id="missing",
            edge_type=EdgeType.IMPORTS,
        )


def test_builder_creates_complete_relationship():

    builder, store = (
        create_builder()
    )

    project = builder.add_node(
        node_type=NodeType.PROJECT,
        name="Madhav",
        node_id="project-1",
    )

    package = builder.add_node(
        node_type=NodeType.PACKAGE,
        name="pytest",
        node_id="package-1",
    )

    edge = builder.add_edge(
        source_id=project.id,
        target_id=package.id,
        edge_type=EdgeType.USES,
        properties={
            "reason": "dependency",
        },
        metadata={
            "source": "package_manager",
        },
    )

    assert (
        store.node_count()
        == 2
    )

    assert (
        store.edge_count()
        == 1
    )

    assert (
        edge.properties[
            "reason"
        ]
        == "dependency"
    )

    assert (
        edge.metadata[
            "source"
        ]
        == "package_manager"
    )