from brain.workspace.detectors.architecture_detector import (
    ArchitectureDetector,
)

from brain.workspace.detectors.dependency_detector import (
    DependencyDetector,
)

from brain.workspace.detectors.language_detector import (
    LanguageDetector,
)

from brain.workspace.plugins.architectures.fake_architecture_detector import (
    FakeArchitectureDetector,
)

from brain.workspace.plugins.dependencies.fake_dependency_detector import (
    FakeDependencyDetector,
)

from brain.workspace.plugins.languages.fake_language_detector import (
    FakeLanguageDetector,
)

from brain.workspace.registries.detector_registry import (
    DetectorRegistry,
)

from brain.workspace.workspace_manager import (
    WorkspaceManager,
)

from brain.workspace.workspace_learner import (
    WorkspaceLearner,
)


def test_workspace_manager(
    tmp_path,
):

    project = (
        tmp_path / "project"
    )

    project.mkdir()

    (
        project / "main.py"
    ).write_text(
        "hello"
    )

    registry = (
        DetectorRegistry()
    )

    registry.register(
        FakeLanguageDetector()
    )

    language = (
        LanguageDetector(
            registry,
        )
    )

    registry = (
        DetectorRegistry()
    )

    registry.register(
        FakeDependencyDetector()
    )

    dependency = (
        DependencyDetector(
            registry,
        )
    )

    registry = (
        DetectorRegistry()
    )

    registry.register(
        FakeArchitectureDetector()
    )

    architecture = (
        ArchitectureDetector(
            registry,
        )
    )

    learner = (
        WorkspaceLearner(
            language,
            dependency,
            architecture,
        )
    )

    summary = (
        WorkspaceManager(
            learner,
        )
    ).analyze(
        project,
    )

    assert (
        summary["files"]
        == 1
    )

    assert (
        summary["technologies"]
        == {
            "FakeLanguage"
        }
    )