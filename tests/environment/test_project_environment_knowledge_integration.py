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
from brain.environment.project_environment_graph_builder import (
    ProjectEnvironmentGraphBuilder,
)
from brain.environment.project_environment_scanner import (
    ProjectEnvironmentScanner,
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
                    DetectorRegistry(),
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


def test_project_environment_knowledge_integration():

    scanner = create_scanner()

    environment = scanner.scan(".")

    graph = (
        ProjectEnvironmentGraphBuilder()
        .build(environment)
    )

    assert graph is not None

    assert graph.get_node("project") is not None
    assert graph.get_node(
        environment.operating_system.name
    ) is not None

    assert graph.get_edge("runs_on") is not None