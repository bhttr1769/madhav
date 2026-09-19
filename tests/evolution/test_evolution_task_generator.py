import pytest

from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)
from brain.evolution.evolution_task_generator import (
    EvolutionTaskGenerator,
)


def create_capability(
    capability_id: str,
) -> CapabilityDescriptor:
    return CapabilityDescriptor(
        id=capability_id,
        name=capability_id,
        description=f"Capability {capability_id}",
        version="1.0.0",
        entry_point=(
            f"brain.{capability_id}.Capability"
        ),
        dependencies=frozenset(),
    )


def test_generates_task_for_missing_capability():
    generator = EvolutionTaskGenerator()

    result = generator.generate(
        required_capabilities=frozenset(
            {"repository_analysis"},
        ),
        available_capabilities=(),
    )

    assert result == (
        "implement capability: repository_analysis",
    )


def test_does_not_generate_task_for_available_capability():
    generator = EvolutionTaskGenerator()

    result = generator.generate(
        required_capabilities=frozenset(
            {"file_read"},
        ),
        available_capabilities=(
            create_capability("file_read"),
        ),
    )

    assert result == ()


def test_generates_tasks_for_multiple_missing_capabilities():
    generator = EvolutionTaskGenerator()

    result = generator.generate(
        required_capabilities=frozenset(
            {
                "repository_analysis",
                "project_graph",
            }
        ),
        available_capabilities=(
            create_capability("file_read"),
        ),
    )

    assert result == (
        "implement capability: project_graph",
        "implement capability: repository_analysis",
    )


def test_generates_only_missing_tasks():
    generator = EvolutionTaskGenerator()

    result = generator.generate(
        required_capabilities=frozenset(
            {
                "file_read",
                "repository_analysis",
            }
        ),
        available_capabilities=(
            create_capability("file_read"),
        ),
    )

    assert result == (
        "implement capability: repository_analysis",
    )


def test_returns_empty_when_no_capabilities_are_required():
    generator = EvolutionTaskGenerator()

    result = generator.generate(
        required_capabilities=frozenset(),
        available_capabilities=(
            create_capability("file_read"),
        ),
    )

    assert result == ()


def test_returns_empty_when_all_capabilities_are_available():
    generator = EvolutionTaskGenerator()

    result = generator.generate(
        required_capabilities=frozenset(
            {
                "file_read",
                "code_analysis",
            }
        ),
        available_capabilities=(
            create_capability("file_read"),
            create_capability("code_analysis"),
        ),
    )

    assert result == ()


def test_rejects_non_frozenset_requirements():
    generator = EvolutionTaskGenerator()

    with pytest.raises(
        TypeError,
        match="required_capabilities must be a frozenset",
    ):
        generator.generate(
            required_capabilities={"file_read"},
            available_capabilities=(),
        )


def test_rejects_non_tuple_capabilities():
    generator = EvolutionTaskGenerator()

    with pytest.raises(
        TypeError,
        match="available_capabilities must be a tuple",
    ):
        generator.generate(
            required_capabilities=frozenset(
                {"file_read"},
            ),
            available_capabilities=[
                create_capability("file_read"),
            ],
        )


def test_rejects_invalid_capability():
    generator = EvolutionTaskGenerator()

    with pytest.raises(
        TypeError,
        match="CapabilityDescriptor",
    ):
        generator.generate(
            required_capabilities=frozenset(
                {"file_read"},
            ),
            available_capabilities=("invalid",),
        )