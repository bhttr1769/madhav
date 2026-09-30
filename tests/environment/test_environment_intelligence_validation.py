from brain.environment.docker.docker_compose_detector import (
    DockerComposeDetector,
)
from brain.environment.docker.docker_container_detector import (
    DockerContainerDetector,
)
from brain.environment.docker.docker_detector import (
    DockerDetector,
)
from brain.environment.docker.docker_environment_detector import (
    DockerEnvironmentDetector,
)
from brain.environment.environment_context_builder import (
    EnvironmentContextBuilder,
)
from brain.environment.project_environment_graph_builder import (
    ProjectEnvironmentGraphBuilder,
)
from brain.environment.project_environment_scanner import (
    ProjectEnvironmentScanner,
)
from brain.environment.project_environment_summary_builder import (
    ProjectEnvironmentSummaryBuilder,
)
from brain.environment.terminals.local_terminal import (
    LocalTerminal,
)
from brain.workspace.detectors.architecture_detector import (
    ArchitectureDetector,
)
from brain.workspace.detectors.dependency_detector import (
    DependencyDetector,
)
from brain.workspace.detectors.language_detector import (
    LanguageDetector,
)
from brain.workspace.registries.detector_registry import (
    DetectorRegistry,
)
from brain.workspace.workspace_learner import (
    WorkspaceLearner,
)
from brain.workspace.workspace_manager import (
    WorkspaceManager,
)


def create_scanner():

    terminal = LocalTerminal()

    docker_environment = (
        DockerEnvironmentDetector(
            docker_detector=(
                DockerDetector()
            ),
            container_detector=(
                DockerContainerDetector(
                    terminal,
                )
            ),
            compose_detector=(
                DockerComposeDetector()
            ),
        )
    )

    learner = (
        WorkspaceLearner(
            language_detector=(
                LanguageDetector(
                    DetectorRegistry(),
                )
            ),
            dependency_detector=(
                DependencyDetector(
                    DetectorRegistry(),
                )
            ),
            architecture_detector=(
                ArchitectureDetector(
                    DetectorRegistry()
                )
            ),
        )
    )

    manager = WorkspaceManager(
        learner,
    )

    return ProjectEnvironmentScanner(
        manager,
        docker_environment,
    )


def test_environment_intelligence_validation():

    scanner = create_scanner()

    environment = scanner.scan(".")

    context = (
        EnvironmentContextBuilder(
            scanner,
        )
        .build(".")
    )

    assert context.operating_system is not None
    assert context.git_repository is not None
    assert context.docker_environment is not None
    assert context.workspace is not None

    summary = (
        ProjectEnvironmentSummaryBuilder()
        .build(environment)
    )

    assert summary["operating_system"] == (
        environment.operating_system.name
    )

    assert summary["git_repository"] == (
        environment.git_repository.is_repository
    )

    assert summary["git_branch"] == (
        environment.git_branch.name
    )

    assert summary["git_clean"] == (
        environment.git_status.is_clean
    )

    assert summary["docker_installed"] == (
        environment
        .docker_environment
        .info
        .installed
    )

    assert summary["docker_compose"] == (
        environment
        .docker_environment
        .compose
        .exists
    )

    assert summary["workspace_files"] == (
        environment.workspace.repository.files
    )

    assert summary["workspace_directories"] == (
        environment.workspace.repository.directories
    )

    assert summary["technologies"] == {
        technology.name
        for technology in environment.workspace.technologies
    }

    assert summary["dependencies"] == {
        dependency.name
        for dependency in environment.workspace.dependencies
    }

    assert summary["architectures"] == {
        architecture.name
        for architecture in environment.workspace.architectures
    }