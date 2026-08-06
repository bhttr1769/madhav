import pytest

from brain.graph.extraction.entity_extractor import (
    EntityExtractor,
)


def test_entity_extractor():

    with pytest.raises(TypeError):
        EntityExtractor()