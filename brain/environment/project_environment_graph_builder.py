from brain.environment.models.project_environment import (
    ProjectEnvironment,
)

from brain.graph.models.edge import (
    Edge,
)

from brain.graph.models.node import (
    Node,
)

from brain.graph.storage.graph_store import (
    GraphStore,
)

from brain.workspace.workspace_graph_builder import (
    WorkspaceGraphBuilder,
)


class ProjectEnvironmentGraphBuilder:
    """
    Converts a complete project environment
    into graph knowledge.
    """

    def __init__(self):

        self._workspace_builder = (
            WorkspaceGraphBuilder()
        )

    def build(
        self,
        environment: ProjectEnvironment,
    ) -> GraphStore:

        graph = GraphStore()

        graph.add_node(
            Node(
                id="project",
                name="Project",
                type="project",
            )
        )

        os_name = (
            environment
            .operating_system
            .name
        )

        graph.add_node(
            Node(
                id=os_name,
                name=os_name,
                type="operating_system",
            )
        )

        graph.add_edge(
            Edge(
                id="runs_on",
                source="project",
                target=os_name,
                relation="runs_on",
            )
        )

        if (
            environment
            .git_repository
            .is_repository
        ):

            graph.add_node(
                Node(
                    id="git",
                    name="Git",
                    type="version_control",
                )
            )

            graph.add_edge(
                Edge(
                    id="uses_git",
                    source="project",
                    target="git",
                    relation="uses",
                )
            )

            branch = (
                environment
                .git_branch
                .name
            )

            if branch:

                graph.add_node(
                    Node(
                        id=branch,
                        name=branch,
                        type="branch",
                    )
                )

                graph.add_edge(
                    Edge(
                        id="current_branch",
                        source="git",
                        target=branch,
                        relation="current_branch",
                    )
                )

        if (
            environment
            .docker_environment
            .info
            .installed
        ):

            graph.add_node(
                Node(
                    id="docker",
                    name="Docker",
                    type="container",
                )
            )

            graph.add_edge(
                Edge(
                    id="uses_docker",
                    source="project",
                    target="docker",
                    relation="uses",
                )
            )

        workspace_graph = (
            self._workspace_builder.build(
                environment.workspace,
            )
        )

        for node in (
            workspace_graph
            .graph
            .nodes
            .values()
        ):

            if (
                graph.get_node(
                    node.id,
                )
                is None
            ):

                graph.add_node(
                    node,
                )

        for edge in (
            workspace_graph
            .graph
            .edges
            .values()
        ):

            if (
                graph.get_edge(
                    edge.id,
                )
                is None
            ):

                graph.add_edge(
                    edge,
                )

        return graph