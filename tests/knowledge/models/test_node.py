from brain.knowledge.models.node import (
    Node,
)

from brain.knowledge.models.node_type import (
    NodeType,
)


def test_node_creation():

    node = Node(
        id="project-1",
        type=NodeType.PROJECT,
        name="Madhav",
        properties={
            "language": "Python",
        },
        metadata={
            "source": "workspace",
        },
    )

    assert (
        node.id
        == "project-1"
    )

    assert (
        node.type
        == NodeType.PROJECT
    )

    assert (
        node.name
        == "Madhav"
    )

    assert (
        node.properties[
            "language"
        ]
        == "Python"
    )

    assert (
        node.metadata[
            "source"
        ]
        == "workspace"
    )


def test_node_is_immutable():

    node = Node(
        id="file-1",
        type=NodeType.FILE,
        name="main.py",
        properties={},
        metadata={},
    )

    try:

        node.name = "other.py"

        assert False

    except AttributeError:

        pass


def test_node_types():

    assert (
        NodeType.PROJECT.value
        == "project"
    )

    assert (
        NodeType.FILE.value
        == "file"
    )

    assert (
        NodeType.PACKAGE.value
        == "package"
    )

    assert (
        NodeType.DEPENDENCY.value
        == "dependency"
    )

    assert (
        NodeType.TECHNOLOGY.value
        == "technology"
    )


def test_node_properties_are_stored():

    properties = {
        "path": "src/main.py",
        "language": "python",
    }

    node = Node(
        id="file-1",
        type=NodeType.FILE,
        name="main.py",
        properties=properties,
        metadata={},
    )

    assert (
        node.properties
        == properties
    )


def test_node_metadata_is_stored():

    metadata = {
        "source": "workspace",
        "confidence": 1.0,
    }

    node = Node(
        id="file-1",
        type=NodeType.FILE,
        name="main.py",
        properties={},
        metadata=metadata,
    )

    assert (
        node.metadata
        == metadata
    )