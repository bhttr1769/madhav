import pytest

from brain.capabilities.capability_executor import (
    CapabilityExecutor,
)
from brain.capabilities.capability_registry import (
    CapabilityRegistry,
)
from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)


class ExampleCapability:
    @staticmethod
    def execute(input_data):
        return f"processed: {input_data}"


class InvalidCapability:
    pass


class NonCallableExecuteCapability:
    execute = "not callable"


class FailingCapability:
    @staticmethod
    def execute(input_data):
        raise RuntimeError("capability failed")


class FailingResolver:
    def resolve(self, entry_point):
        raise RuntimeError("resolution failed")


def create_descriptor(
    capability_id: str,
    entry_point: str,
) -> CapabilityDescriptor:
    return CapabilityDescriptor(
        id=capability_id,
        name=capability_id,
        description="Test capability",
        version="1.0.0",
        entry_point=entry_point,
        dependencies=frozenset(),
    )


def test_execute_invokes_registered_capability():
    capability = create_descriptor(
        "example",
        "tests.capabilities.test_capability_executor.ExampleCapability",
    )

    registry = CapabilityRegistry(
        capabilities=(capability,),
    )

    executor = CapabilityExecutor(
        registry,
    )

    result = executor.execute(
        "example",
        "hello",
    )

    assert result == "processed: hello"


def test_execute_rejects_unknown_capability():
    registry = CapabilityRegistry()
    executor = CapabilityExecutor(registry)

    with pytest.raises(
        KeyError,
        match="capability not found",
    ):
        executor.execute(
            "missing",
            "hello",
        )


@pytest.mark.parametrize(
    "capability_id",
    [
        "",
        "   ",
    ],
)
def test_execute_rejects_empty_capability_id(
    capability_id,
):
    registry = CapabilityRegistry()
    executor = CapabilityExecutor(registry)

    with pytest.raises(
        ValueError,
        match="capability_id must not be empty",
    ):
        executor.execute(
            capability_id,
            "hello",
        )


def test_execute_rejects_non_string_capability_id():
    registry = CapabilityRegistry()
    executor = CapabilityExecutor(registry)

    with pytest.raises(
        TypeError,
        match="capability_id must be a string",
    ):
        executor.execute(
            123,
            "hello",
        )


def test_execute_rejects_capability_without_execute():
    capability = create_descriptor(
        "invalid",
        "tests.capabilities.test_capability_executor.InvalidCapability",
    )

    registry = CapabilityRegistry(
        capabilities=(capability,),
    )

    executor = CapabilityExecutor(
        registry,
    )

    with pytest.raises(
        TypeError,
        match="provide an execute method",
    ):
        executor.execute(
            "invalid",
            "hello",
        )


def test_execute_rejects_non_callable_execute():
    capability = create_descriptor(
        "non_callable",
        "tests.capabilities.test_capability_executor."
        "NonCallableExecuteCapability",
    )

    registry = CapabilityRegistry(
        capabilities=(capability,),
    )

    executor = CapabilityExecutor(registry)

    with pytest.raises(
        TypeError,
        match="must be callable",
    ):
        executor.execute(
            "non_callable",
            "hello",
        )


def test_execute_propagates_capability_exception():
    capability = create_descriptor(
        "failing",
        "tests.capabilities.test_capability_executor."
        "FailingCapability",
    )

    registry = CapabilityRegistry(
        capabilities=(capability,),
    )

    executor = CapabilityExecutor(registry)

    with pytest.raises(
        RuntimeError,
        match="capability failed",
    ):
        executor.execute(
            "failing",
            "hello",
        )


def test_execute_propagates_resolver_exception():
    capability = create_descriptor(
        "example",
        "some.invalid.EntryPoint",
    )

    registry = CapabilityRegistry(
        capabilities=(capability,),
    )

    executor = CapabilityExecutor(
        registry,
        resolver=FailingResolver(),
    )

    with pytest.raises(
        RuntimeError,
        match="resolution failed",
    ):
        executor.execute(
            "example",
            "hello",
        )


def test_execute_does_not_mutate_registry():
    capability = create_descriptor(
        "example",
        "tests.capabilities.test_capability_executor."
        "ExampleCapability",
    )

    registry = CapabilityRegistry(
        capabilities=(capability,),
    )

    executor = CapabilityExecutor(registry)

    before = registry.all()

    executor.execute(
        "example",
        "hello",
    )

    after = registry.all()

    assert after == before