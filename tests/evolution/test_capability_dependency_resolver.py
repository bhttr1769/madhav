import pytest

from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)
from brain.evolution.capability_dependency_resolver import (
    CapabilityDependencyResolver,
)


def create_capability(
    capability_id: str,
    dependencies: frozenset[str] = frozenset(),
) -> CapabilityDescriptor:
    return CapabilityDescriptor(
        id=capability_id,
        name=capability_id,
        description=f"Capability {capability_id}",
        version="1.0.0",
        entry_point=(
            f"brain.{capability_id}.Capability"
        ),
        dependencies=dependencies,
    )


def test_resolves_direct_dependencies():
    resolver = CapabilityDependencyResolver()

    result = resolver.resolve(
        required_capabilities=frozenset(
            {"repository_analysis"},
        ),
        available_capabilities=(
            create_capability(
                "repository_analysis",
                frozenset({"file_read"}),
            ),
            create_capability("file_read"),
        ),
    )

    assert result == frozenset(
        {
            "repository_analysis",
            "file_read",
        }
    )


def test_resolves_transitive_dependencies():
    resolver = CapabilityDependencyResolver()

    result = resolver.resolve(
        required_capabilities=frozenset(
            {"repository_analysis"},
        ),
        available_capabilities=(
            create_capability(
                "repository_analysis",
                frozenset({"code_analysis"}),
            ),
            create_capability(
                "code_analysis",
                frozenset({"file_read"}),
            ),
            create_capability("file_read"),
        ),
    )

    assert result == frozenset(
        {
            "repository_analysis",
            "code_analysis",
            "file_read",
        }
    )


def test_ignores_missing_dependencies():
    resolver = CapabilityDependencyResolver()

    result = resolver.resolve(
        required_capabilities=frozenset(
            {"repository_analysis"},
        ),
        available_capabilities=(
            create_capability(
                "repository_analysis",
                frozenset(
                    {
                        "file_read",
                        "missing_dependency",
                    }
                ),
            ),
            create_capability("file_read"),
        ),
    )

    assert result == frozenset(
        {
            "repository_analysis",
            "file_read",
        }
    )


def test_resolves_multiple_dependency_branches():
    resolver = CapabilityDependencyResolver()

    result = resolver.resolve(
        required_capabilities=frozenset(
            {"repository_analysis"},
        ),
        available_capabilities=(
            create_capability(
                "repository_analysis",
                frozenset(
                    {
                        "file_read",
                        "code_analysis",
                    }
                ),
            ),
            create_capability("file_read"),
            create_capability("code_analysis"),
        ),
    )

    assert result == frozenset(
        {
            "repository_analysis",
            "file_read",
            "code_analysis",
        }
    )


def test_resolves_capability_without_dependencies():
    resolver = CapabilityDependencyResolver()

    result = resolver.resolve(
        required_capabilities=frozenset(
            {"file_read"},
        ),
        available_capabilities=(
            create_capability("file_read"),
        ),
    )

    assert result == frozenset(
        {"file_read"}
    )


def test_returns_empty_for_missing_required_capability():
    resolver = CapabilityDependencyResolver()

    result = resolver.resolve(
        required_capabilities=frozenset(
            {"missing"},
        ),
        available_capabilities=(
            create_capability("file_read"),
        ),
    )

    assert result == frozenset()


def test_detects_direct_dependency_cycle():
    resolver = CapabilityDependencyResolver()

    with pytest.raises(
        ValueError,
        match="cyclic capability dependency detected",
    ):
        resolver.resolve(
            required_capabilities=frozenset(
                {"capability_a"},
            ),
            available_capabilities=(
                create_capability(
                    "capability_a",
                    frozenset({"capability_b"}),
                ),
                create_capability(
                    "capability_b",
                    frozenset({"capability_a"}),
                ),
            ),
        )


def test_detects_transitive_dependency_cycle():
    resolver = CapabilityDependencyResolver()

    with pytest.raises(
        ValueError,
        match="cyclic capability dependency detected",
    ):
        resolver.resolve(
            required_capabilities=frozenset(
                {"capability_a"},
            ),
            available_capabilities=(
                create_capability(
                    "capability_a",
                    frozenset({"capability_b"}),
                ),
                create_capability(
                    "capability_b",
                    frozenset({"capability_c"}),
                ),
                create_capability(
                    "capability_c",
                    frozenset({"capability_a"}),
                ),
            ),
        )


def test_rejects_non_frozenset_requirements():
    resolver = CapabilityDependencyResolver()

    with pytest.raises(
        TypeError,
        match="required_capabilities must be a frozenset",
    ):
        resolver.resolve(
            required_capabilities={"file_read"},
            available_capabilities=(),
        )


def test_rejects_non_tuple_capabilities():
    resolver = CapabilityDependencyResolver()

    with pytest.raises(
        TypeError,
        match="available_capabilities must be a tuple",
    ):
        resolver.resolve(
            required_capabilities=frozenset(
                {"file_read"},
            ),
            available_capabilities=[
                create_capability("file_read"),
            ],
        )


def test_rejects_invalid_capability():
    resolver = CapabilityDependencyResolver()

    with pytest.raises(
        TypeError,
        match="CapabilityDescriptor",
    ):
        resolver.resolve(
            required_capabilities=frozenset(
                {"file_read"},
            ),
            available_capabilities=("invalid",),
        )