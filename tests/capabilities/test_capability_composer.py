import pytest

from brain.capabilities.capability_composer import (
    CapabilityComposer,
)
from brain.capabilities.models.capability_composition import (
    CapabilityComposition,
)
from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)


def create_capability(
    capability_id: str,
) -> CapabilityDescriptor:
    return CapabilityDescriptor(
        id=capability_id,
        name=capability_id,
        description=f"Capability {capability_id}",
        version="1.0.0",
        entry_point=f"brain.{capability_id}.Capability",
        dependencies=frozenset(),
    )


def test_compose_creates_capability_composition():
    composer = CapabilityComposer()

    first = create_capability("first")
    second = create_capability("second")

    result = composer.compose(
        capability_id="composed",
        name="Composed Capability",
        description="A composed capability.",
        version="1.0.0",
        capabilities=(first, second),
    )

    assert isinstance(
        result,
        CapabilityComposition,
    )

    assert result.id == "composed"
    assert result.name == "Composed Capability"
    assert result.description == (
        "A composed capability."
    )
    assert result.version == "1.0.0"
    assert result.capabilities == (
        first,
        second,
    )


def test_compose_rejects_empty_capabilities():
    composer = CapabilityComposer()

    with pytest.raises(
        ValueError,
        match="capabilities must not be empty",
    ):
        composer.compose(
            capability_id="composed",
            name="Composed Capability",
            description="A composed capability.",
            version="1.0.0",
            capabilities=(),
        )


def test_compose_rejects_non_tuple_capabilities():
    composer = CapabilityComposer()

    with pytest.raises(
        TypeError,
        match="capabilities must be a tuple",
    ):
        composer.compose(
            capability_id="composed",
            name="Composed Capability",
            description="A composed capability.",
            version="1.0.0",
            capabilities=[
                create_capability("first"),
            ],
        )


def test_compose_rejects_invalid_capability():
    composer = CapabilityComposer()

    with pytest.raises(
        TypeError,
        match="CapabilityDescriptor",
    ):
        composer.compose(
            capability_id="composed",
            name="Composed Capability",
            description="A composed capability.",
            version="1.0.0",
            capabilities=("invalid",),
        )


@pytest.mark.parametrize(
    "capability_id",
    [
        "",
        "   ",
    ],
)
def test_compose_rejects_empty_capability_id(
    capability_id,
):
    composer = CapabilityComposer()

    with pytest.raises(
        ValueError,
        match="capability_id must not be empty",
    ):
        composer.compose(
            capability_id=capability_id,
            name="Composed Capability",
            description="A composed capability.",
            version="1.0.0",
            capabilities=(
                create_capability("first"),
            ),
        )


def test_composition_is_immutable():
    composer = CapabilityComposer()

    result = composer.compose(
        capability_id="composed",
        name="Composed Capability",
        description="A composed capability.",
        version="1.0.0",
        capabilities=(
            create_capability("first"),
        ),
    )

    with pytest.raises(
        AttributeError,
    ):
        result.id = "changed"


def test_composer_preserves_capability_contracts():
    first = CapabilityDescriptor(
        id="text_source",
        name="Text Source",
        description="Produces text.",
        version="1.0.0",
        entry_point="tests.capabilities.TextSource",
        dependencies=frozenset(),
        input_contract="object",
        output_contract="text",
    )

    second = CapabilityDescriptor(
        id="text_length",
        name="Text Length",
        description="Calculates text length.",
        version="1.0.0",
        entry_point="tests.capabilities.TextLength",
        dependencies=frozenset(),
        input_contract="text",
        output_contract="number",
    )

    composition = CapabilityComposer().compose(
        capability_id="text_pipeline",
        name="Text Pipeline",
        description="Composed text processing capability.",
        version="1.0.0",
        capabilities=(
            first,
            second,
        ),
    )

    assert composition.capabilities == (
        first,
        second,
    )

    assert composition.capabilities[0] is first
    assert composition.capabilities[0].input_contract == "object"
    assert composition.capabilities[0].output_contract == "text"

    assert composition.capabilities[1] is second
    assert composition.capabilities[1].input_contract == "text"
    assert composition.capabilities[1].output_contract == "number"