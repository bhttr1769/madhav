from brain.package_managers.parsers.signature_dependency_parser import (
    SignatureDependencyParser,
)

from brain.package_managers.registries.dependency_parser_registry import (
    DependencyParserRegistry,
)


def test_dependency_parser_registry():

    registry = (
        DependencyParserRegistry()
    )

    registry.register(
        SignatureDependencyParser(),
    )

    assert (
        registry.count()
        == 1
    )

    assert (
        len(
            registry.all(),
        )
        == 1
    )