from brain.vector.models.vector import Vector


def test_vector_creation():

    vector = Vector(
        values=[1.0, 2.0, 3.0]
    )

    assert vector.values == [1.0, 2.0, 3.0]

    assert vector.dimensions == 3

    assert len(vector) == 3