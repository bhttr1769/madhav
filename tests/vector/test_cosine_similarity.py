import pytest

from brain.vector.models.vector import Vector
from brain.vector.similarity.cosine_similarity import (
    CosineSimilarity,
)


def test_identical_vectors():

    first = Vector([1.0, 2.0, 3.0])

    second = Vector([1.0, 2.0, 3.0])

    similarity = CosineSimilarity.compute(
        first,
        second,
    )

    assert similarity == pytest.approx(1.0)


def test_perpendicular_vectors():

    first = Vector([1.0, 0.0])

    second = Vector([0.0, 1.0])

    similarity = CosineSimilarity.compute(
        first,
        second,
    )

    assert similarity == pytest.approx(0.0)


def test_dimension_mismatch():

    with pytest.raises(ValueError):

        CosineSimilarity.compute(
            Vector([1.0]),
            Vector([1.0, 2.0]),
        )


def test_zero_vector():

    similarity = CosineSimilarity.compute(
        Vector([0.0, 0.0]),
        Vector([1.0, 2.0]),
    )

    assert similarity == 0.0