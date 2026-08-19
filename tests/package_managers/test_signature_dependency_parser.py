from brain.package_managers.models.dependency_file import (
    DependencyFile,
)

from brain.package_managers.parsers.signature_dependency_parser import (
    SignatureDependencyParser,
)


def test_signature_dependency_parser():

    dependencies = (
        SignatureDependencyParser()
    ).parse(
        DependencyFile(
            name="package.json",
            path="package.json",
            type="manifest",
        ),
    )

    dependency = next(
        iter(
            dependencies,
        )
    )

    assert (
        dependency.name
        == "fake"
    )

    assert (
        dependency.source
        == "package.json"
    )