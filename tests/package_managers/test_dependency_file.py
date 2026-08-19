from brain.package_managers.models.dependency_file import (
    DependencyFile,
)


def test_dependency_file():

    dependency_file = DependencyFile(
        name="package.json",
        path="package.json",
        type="manifest",
    )

    assert (
        dependency_file.name
        == "package.json"
    )

    assert (
        dependency_file.path
        == "package.json"
    )