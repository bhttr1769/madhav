import pytest

from brain.graph.extraction.relationship_extractor import (
    RelationshipExtractor,
)


def test_relationship_extractor():

    with pytest.raises(TypeError):
        RelationshipExtractor()