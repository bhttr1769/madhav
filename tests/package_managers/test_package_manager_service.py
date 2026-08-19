from brain.package_managers.detectors.build_lifecycle_detector import (
    BuildLifecycleDetector,
)

from brain.package_managers.detectors.dependency_detector import (
    DependencyDetector,
)

from brain.package_managers.detectors.dependency_file_detector import (
    DependencyFileDetector,
)

from brain.package_managers.detectors.package_manager_detector import (
    PackageManagerDetector,
)

from brain.package_managers.plugins.dependency_files.signature_dependency_file_detector import (
    SignatureDependencyFileDetector,
)

from brain.package_managers.plugins.lifecycles.fake_build_lifecycle_detector import (
    FakeBuildLifecycleDetector,
)

from brain.package_managers.plugins.managers.fake_package_manager_detector import (
    FakePackageManagerDetector,
)

from brain.package_managers.registries.build_lifecycle_registry import (
    BuildLifecycleRegistry,
)

from brain.package_managers.registries.dependency_file_registry import (
    DependencyFileRegistry,
)

from brain.package_managers.registries.dependency_parser_registry import (
    DependencyParserRegistry,
)

from brain.package_managers.registries.package_manager_registry import (
    PackageManagerRegistry,
)

from brain.package_managers.services.package_manager_service import (
    PackageManagerService,
)

from brain.workspace.models.signature import (
    Signature,
)


def test_package_manager_service():

    dependency_file_registry = (
        DependencyFileRegistry()
    )

    dependency_file_registry.register(
        SignatureDependencyFileDetector(),
    )

    package_manager_registry = (
        PackageManagerRegistry()
    )

    package_manager_registry.register(
        FakePackageManagerDetector(),
    )

    dependency_parser_registry = (
        DependencyParserRegistry()
    )

    build_lifecycle_registry = (
        BuildLifecycleRegistry()
    )

    build_lifecycle_registry.register(
        FakeBuildLifecycleDetector(),
    )

    environment = (
        PackageManagerService(
            dependency_file_detector=(
                DependencyFileDetector(
                    dependency_file_registry,
                )
            ),
            package_manager_detector=(
                PackageManagerDetector(
                    package_manager_registry,
                )
            ),
            dependency_detector=(
                DependencyDetector(
                    dependency_parser_registry,
                )
            ),
            build_lifecycle_detector=(
                BuildLifecycleDetector(
                    build_lifecycle_registry,
                )
            ),
        )
    ).analyze(
        {
            Signature(
                value="package.json",
                category="filename",
                path="package.json",
            ),
        },
    )

    assert len(
        environment.dependency_files,
    ) > 0

    assert len(
        environment.managers,
    ) > 0

    assert len(
        environment.lifecycles,
    ) > 0