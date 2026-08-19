from brain.package_managers.detectors.package_manager_detector import (
    PackageManagerDetector,
)

from brain.package_managers.plugins.managers.fake_package_manager_detector import (
    FakePackageManagerDetector,
)

from brain.package_managers.registries.package_manager_registry import (
    PackageManagerRegistry,
)


def test_package_manager_detector():

    registry = (
        PackageManagerRegistry()
    )

    registry.register(
        FakePackageManagerDetector(),
    )

    managers = (
        PackageManagerDetector(
            registry,
        )
    ).detect(
        set(),
    )

    assert len(
        managers,
    ) == 1

    assert next(
        iter(
            managers,
        )
    ).name == (
        "FakePackageManager"
    )