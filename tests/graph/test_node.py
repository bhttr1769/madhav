from brain.graph.models.node import Node


def test_node():

    node = Node(
        id="1",
        name="Java",
        type="language",
    )

    assert node.id == "1"

    assert node.name == "Java"

    assert node.type == "language"

    assert node.metadata == {}