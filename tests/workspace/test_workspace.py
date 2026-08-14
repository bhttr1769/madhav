from brain.workspace.models.architecture import (
    Architecture,
)
from brain.workspace.models.dependency import (
    Dependency,
)
from brain.workspace.models.repository import (
    Repository,
)
from brain.workspace.models.signature import (
    Signature,
)
from brain.workspace.models.technology import (
    Technology,
)
from brain.workspace.models.workspace import (
    Workspace,
)


def test_workspace():

    repository = Repository(
        files=1,
        directories=1,
        signatures={
            Signature(
                value="main.py",
                category="filename",
            )
        },
    )

    workspace = Workspace(
        repository=repository,
        technologies={
            Technology(
                name="Python",
                category="language",
            )
        },
        dependencies={
            Dependency(
                name="pytest",
            )
        },
        architectures={
            Architecture(
                name="Layered",
            )
        },
    )

    assert (
        workspace.repository.files
        == 1
    )

    assert (
        len(
            workspace.technologies
        )
        == 1
    )

    assert (
        len(
            workspace.dependencies
        )
        == 1
    )

    assert (
        len(
            workspace.architectures
        )
        == 1
    )