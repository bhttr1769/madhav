from brain.package_managers.models.dependency import (
    Dependency,
)


def test_dependency():

    dependency = Dependency(
        name="express",
        version="1.0.0",
        source="package.json",
    )

    assert (
        dependency.name
        == "express"
    )

    assert (
        dependency.version
        == "1.0.0"
    )

    assert (
        dependency.source
        == "package.json"
    )

    assert (
        len(
            dependency.metadata,
        )
        == 0
    )