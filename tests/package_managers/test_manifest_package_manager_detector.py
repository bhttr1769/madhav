from brain.package_managers.models.dependency_file import (
    DependencyFile,
)

from brain.package_managers.plugins.managers.manifest_package_manager_detector import (
    ManifestPackageManagerDetector,
)


def test_manifest_package_manager_detector():

    managers = (
        ManifestPackageManagerDetector()
    ).detect(
        {
            DependencyFile(
                name="package.json",
                path="package.json",
                type="manifest",
            ),
        }
    )

    manager = next(
        iter(
            managers,
        )
    )

    assert manager.name == "npm"

    assert (
        manager.manifest
        == "package.json"
    )