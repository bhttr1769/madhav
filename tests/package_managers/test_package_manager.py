from brain.package_managers.models.package_manager import (
    PackageManager,
)


def test_package_manager():

    manager = PackageManager(
        name="npm",
        manifest="package.json",
    )

    assert (
        manager.name
        == "npm"
    )

    assert (
        manager.manifest
        == "package.json"
    )