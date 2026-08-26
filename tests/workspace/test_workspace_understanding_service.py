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

from brain.workspace.models.workspace_understanding import (
    WorkspaceUnderstanding,
)

from brain.workspace.workspace_understanding_service import (
    WorkspaceUnderstandingService,
)


def create_workspace():

    return Workspace(
        repository=Repository(
            files=10,
            directories=4,
            signatures=frozenset({
                Signature(
                    value="main.py",
                    category="filename",
                    path="main.py",
                ),
            }),
        ),
        technologies=frozenset({
            Technology(
                name="Python",
                category="language",
            ),
        }),
        dependencies=frozenset({
            Dependency(
                name="pytest",
            ),
        }),
        architectures=frozenset({
            Architecture(
                name="layered",
            ),
        }),
    )


def test_workspace_understanding_summarizes_workspace():

    understanding = (
        WorkspaceUnderstandingService().analyze(
            create_workspace(),
            "C:/project",
        )
    )

    assert isinstance(
        understanding,
        WorkspaceUnderstanding,
    )

    assert understanding.name == "project"

    assert understanding.root == (
        str(
            __import__("pathlib").Path(
                "C:/project"
            ).resolve()
        )
    )

    assert understanding.files == 10

    assert understanding.directories == 4

    assert understanding.technologies == frozenset({
        "Python",
    })

    assert understanding.dependencies == frozenset({
        "pytest",
    })

    assert understanding.architectures == frozenset({
        "layered",
    })


def test_workspace_understanding_accepts_custom_name():

    understanding = (
        WorkspaceUnderstandingService().analyze(
            create_workspace(),
            "C:/project",
            name="Madhav",
        )
    )

    assert understanding.name == "Madhav"


def test_workspace_understanding_handles_empty_knowledge():

    workspace = Workspace(
        repository=Repository(
            files=0,
            directories=0,
            signatures=frozenset(),
        ),
        technologies=frozenset(),
        dependencies=frozenset(),
        architectures=frozenset(),
    )

    understanding = (
        WorkspaceUnderstandingService().analyze(
            workspace,
            "C:/empty",
        )
    )

    assert understanding.files == 0
    assert understanding.directories == 0
    assert understanding.technologies == frozenset()
    assert understanding.dependencies == frozenset()
    assert understanding.architectures == frozenset()