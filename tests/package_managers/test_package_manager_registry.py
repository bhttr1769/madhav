from brain.package_managers.plugins.managers.fake_package_manager_detector import (
    FakePackageManagerDetector,
)

from brain.package_managers.registries.package_manager_registry import (
    PackageManagerRegistry,
)


def test_package_manager_registry():

    registry = (
        PackageManagerRegistry()
    )

    registry.register(
        FakePackageManagerDetector(),
    )

    assert (
        registry.count()
        == 1
    )

    assert len(
        registry.all(),
    ) == 1