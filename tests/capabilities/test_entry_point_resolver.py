import pytest

from brain.capabilities.entry_point_resolver import (
    EntryPointResolver,
)


class ExampleCapability:
    pass


def test_resolve_class():
    resolver = EntryPointResolver()

    result = resolver.resolve(
        "tests.capabilities.test_entry_point_resolver.ExampleCapability"
    )

    assert result is ExampleCapability


@pytest.mark.parametrize(
    "entry_point",
    [
        "",
        "   ",
    ],
)
def test_resolve_rejects_empty_entry_point(
    entry_point,
):
    resolver = EntryPointResolver()

    with pytest.raises(
        ValueError,
        match="entry_point must not be empty",
    ):
        resolver.resolve(entry_point)


def test_resolve_rejects_invalid_format():
    resolver = EntryPointResolver()

    with pytest.raises(
        ValueError,
        match="module.path.Attribute",
    ):
        resolver.resolve("InvalidEntryPoint")


def test_resolve_rejects_missing_attribute():
    resolver = EntryPointResolver()

    with pytest.raises(
        AttributeError,
        match="entry point not found",
    ):
        resolver.resolve(
            "tests.capabilities.test_entry_point_resolver.MissingCapability"
        )