from brain.knowledge.models.edge import (
    Edge,
)

from brain.knowledge.models.edge_type import (
    EdgeType,
)


def test_edge_creation():

    edge = Edge(
        id="edge-1",
        source_id="project-1",
        target_id="file-1",
        type=EdgeType.CONTAINS,
        properties={
            "relationship": "project-file",
        },
        metadata={
            "source": "workspace",
        },
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
        edge.properties[
            "relationship"
        ]
        == "project-file"
    )

    assert (
        edge.metadata[
            "source"
        ]
        == "workspace"
    )


def test_edge_is_immutable():

    edge = Edge(
        id="edge-1",
        source_id="project-1",
        target_id="file-1",
        type=EdgeType.CONTAINS,
        properties={},
        metadata={},
    )

    try:

        edge.source_id = "other"

        assert False

    except AttributeError:

        pass


def test_edge_types():

    assert (
        EdgeType.CONTAINS.value
        == "contains"
    )

    assert (
        EdgeType.IMPORTS.value
        == "imports"
    )

    assert (
        EdgeType.DEPENDS_ON.value
        == "depends_on"
    )

    assert (
        EdgeType.USES.value
        == "uses"
    )

    assert (
        EdgeType.IMPLEMENTS.value
        == "implements"
    )


def test_edge_properties_are_stored():

    properties = {
        "line": 42,
    }

    edge = Edge(
        id="edge-1",
        source_id="file-1",
        target_id="function-1",
        type=EdgeType.DEFINES,
        properties=properties,
        metadata={},
    )

    assert (
        edge.properties
        == properties
    )


def test_edge_metadata_is_stored():

    metadata = {
        "source": "repository_parser",
        "confidence": 1.0,
    }

    edge = Edge(
        id="edge-1",
        source_id="file-1",
        target_id="function-1",
        type=EdgeType.DEFINES,
        properties={},
        metadata=metadata,
    )

    assert (
        edge.metadata
        == metadata
    )