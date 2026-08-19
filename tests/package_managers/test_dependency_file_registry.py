from brain.package_managers.plugins.dependency_files.signature_dependency_file_detector import (
    SignatureDependencyFileDetector,
)

from brain.package_managers.registries.dependency_file_registry import (
    DependencyFileRegistry,
)


def test_dependency_file_registry():

    registry = (
        DependencyFileRegistry()
    )

    registry.register(
        SignatureDependencyFileDetector(),
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