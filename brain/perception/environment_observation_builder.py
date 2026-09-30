from brain.environment.models.project_environment import (
    ProjectEnvironment,
)

from brain.perception.models.observation import (
    Observation,
)


class EnvironmentObservationBuilder:
    """
    Converts an existing project environment
    into perception observations.
    """

    def build(
        self,
        environment: ProjectEnvironment,
    ) -> frozenset[Observation]:

        if not isinstance(
            environment,
            ProjectEnvironment,
        ):
            raise TypeError(
                "environment must be a ProjectEnvironment"
            )

        observations = set()

        observations.add(
            Observation(
                source="environment",
                category="operating_system",
                subject="project",
                value=(
                    environment
                    .operating_system
                    .name
                ),
            )
        )

        if (
            environment
            .git_repository
            .is_repository
        ):
            observations.add(
                Observation(
                    source="environment",
                    category="version_control",
                    subject="project",
                    value="git",
                )
            )

            branch = (
                environment
                .git_branch
                .name
            )

            if branch:
                observations.add(
                    Observation(
                        source="environment",
                        category="branch",
                        subject="repository",
                        value=branch,
                    )
                )

            observations.add(
                Observation(
                    source="environment",
                    category="git_status",
                    subject="repository",
                    value=(
                        "clean"
                        if environment
                        .git_status
                        .is_clean
                        else "dirty"
                    ),
                )
            )

        if (
            environment
            .docker_environment
            .info
            .installed
        ):
            observations.add(
                Observation(
                    source="environment",
                    category="container",
                    subject="project",
                    value="docker",
                )
            )

            if (
                environment
                .docker_environment
                .compose
                .exists
            ):
                observations.add(
                    Observation(
                        source="environment",
                        category="container_orchestration",
                        subject="project",
                        value="docker_compose",
                    )
                )

        for technology in (
            environment
            .workspace
            .technologies
        ):
            observations.add(
                Observation(
                    source="environment",
                    category="technology",
                    subject="workspace",
                    value=technology.name,
                )
            )

        for dependency in (
            environment
            .workspace
            .dependencies
        ):
            observations.add(
                Observation(
                    source="environment",
                    category="dependency",
                    subject="workspace",
                    value=dependency.name,
                )
            )

        for architecture in (
            environment
            .workspace
            .architectures
        ):
            observations.add(
                Observation(
                    source="environment",
                    category="architecture",
                    subject="workspace",
                    value=architecture.name,
                )
            )

        return frozenset(observations)