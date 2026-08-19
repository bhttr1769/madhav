from brain.package_managers.detectors.dependency_file_detector import (
    DependencyFileDetector,
)

from brain.workspace.models.signature import (
    Signature,
)

from brain.package_managers.plugins.dependency_files.signature_dependency_file_detector import (
    SignatureDependencyFileDetector,
)

from brain.package_managers.registries.dependency_file_registry import (
    DependencyFileRegistry,
)


def test_dependency_file_detector():

    registry = (
        DependencyFileRegistry()
    )

    registry.register(
        SignatureDependencyFileDetector(),
    )

    files = (
        DependencyFileDetector(
            registry,
        )
    ).detect(
        {
            Signature(
                value="package.json",
                category="filename",
                path="package.json",
            ),
        },
    )

    assert len(
        files,
    ) == 1