from brain.workspace.models.workspace_understanding import (
    WorkspaceUnderstanding,
)

from brain.workspace.workspace_context_analyzer import (
    WorkspaceContextAnalyzer,
)


def test_detects_software_project():

    understanding = WorkspaceUnderstanding(
        name="Madhav",
        root="C:/Madhav",
        files=100,
        directories=10,
        technologies=frozenset({
            "Python",
        }),
        dependencies=frozenset({
            "pytest",
        }),
        architectures=frozenset({
            "layered",
        }),
    )

    context = (
        WorkspaceContextAnalyzer().analyze(
            understanding,
        )
    )

    assert context.workspace_type == (
        "software_project"
    )

    assert context.primary_technology == (
        "Python"
    )

    assert context.primary_architecture == (
        "layered"
    )


def test_detects_small_workspace():

    understanding = WorkspaceUnderstanding(
        name="small",
        root="C:/small",
        files=20,
        directories=2,
        technologies=frozenset(),
        dependencies=frozenset(),
        architectures=frozenset(),
    )

    context = (
        WorkspaceContextAnalyzer().analyze(
            understanding,
        )
    )

    assert context.scale == "small"


def test_detects_medium_workspace():

    understanding = WorkspaceUnderstanding(
        name="medium",
        root="C:/medium",
        files=200,
        directories=20,
        technologies=frozenset(),
        dependencies=frozenset(),
        architectures=frozenset(),
    )

    context = (
        WorkspaceContextAnalyzer().analyze(
            understanding,
        )
    )

    assert context.scale == "medium"


def test_detects_large_workspace():

    understanding = WorkspaceUnderstanding(
        name="large",
        root="C:/large",
        files=1000,
        directories=100,
        technologies=frozenset(),
        dependencies=frozenset(),
        architectures=frozenset(),
    )

    context = (
        WorkspaceContextAnalyzer().analyze(
            understanding,
        )
    )

    assert context.scale == "large"


def test_detects_empty_workspace():

    understanding = WorkspaceUnderstanding(
        name="empty",
        root="C:/empty",
        files=0,
        directories=0,
        technologies=frozenset(),
        dependencies=frozenset(),
        architectures=frozenset(),
    )

    context = (
        WorkspaceContextAnalyzer().analyze(
            understanding,
        )
    )

    assert context.workspace_type == "empty"
    assert context.scale == "empty"
    assert context.primary_technology is None
    assert context.primary_architecture is None
    assert context.confidence == 0.0


def test_confidence_uses_available_evidence():

    understanding = WorkspaceUnderstanding(
        name="project",
        root="C:/project",
        files=100,
        directories=10,
        technologies=frozenset({
            "Python",
        }),
        dependencies=frozenset(),
        architectures=frozenset(),
    )

    context = (
        WorkspaceContextAnalyzer().analyze(
            understanding,
        )
    )

    assert context.confidence == 0.5