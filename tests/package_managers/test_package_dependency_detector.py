from brain.package_managers.detectors.dependency_detector import (
    DependencyDetector,
)

from brain.package_managers.models.dependency_file import (
    DependencyFile,
)

from brain.package_managers.parsers.signature_dependency_parser import (
    SignatureDependencyParser,
)

from brain.package_managers.registries.dependency_parser_registry import (
    DependencyParserRegistry,
)


def test_dependency_detector():

    registry = (
        DependencyParserRegistry()
    )

    registry.register(
        SignatureDependencyParser(),
    )

    dependencies = (
        DependencyDetector(
            registry,
        )
    ).detect(
        {
            DependencyFile(
                name="package.json",
                path="package.json",
                type="manifest",
            ),
        },
    )

    assert (
        len(
            dependencies,
        )
        == 1
    )