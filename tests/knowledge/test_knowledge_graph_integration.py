from brain.knowledge.builders.graph_builder import (
    GraphBuilder,
)

from brain.knowledge.integrations.package_manager_graph_builder import (
    PackageManagerKnowledgeBuilder,
)

from brain.knowledge.integrations.workspace_graph_builder import (
    WorkspaceKnowledgeBuilder,
)

from brain.knowledge.models.edge_type import (
    EdgeType,
)

from brain.knowledge.models.node_type import (
    NodeType,
)

from brain.knowledge.services.query_service import (
    QueryService,
)

from brain.knowledge.stores.graph_store import (
    GraphStore,
)

from brain.package_managers.models.build_lifecycle import (
    BuildLifecycle,
)

from brain.package_managers.models.dependency import (
    Dependency as PackageDependency,
)

from brain.package_managers.models.dependency_file import (
    DependencyFile,
)

from brain.package_managers.models.package_manager import (
    PackageManager,
)

from brain.package_managers.models.package_manager_environment import (
    PackageManagerEnvironment,
)

from brain.package_managers.models.project_commands import (
    ProjectCommand,
)

from brain.workspace.models.architecture import (
    Architecture,
)

from brain.workspace.models.dependency import (
    Dependency as WorkspaceDependency,
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


def create_workspace():

    repository = Repository(
        files=2,
        directories=1,
        signatures={
            Signature(
                value="main.py",
                category="filename",
                path="src/main.py",
            ),
            Signature(
                value="utils.py",
                category="filename",
                path="src/utils.py",
            ),
            Signature(
                value="src",
                category="directory",
                path="src",
            ),
        },
    )

    return Workspace(
        repository=repository,
        technologies={
            Technology(
                name="Python",
                category="language",
            ),
        },
        dependencies={
            WorkspaceDependency(
                name="pytest",
            ),
        },
        architectures={
            Architecture(
                name="Layered",
            ),
        },
    )


def create_package_environment():

    return PackageManagerEnvironment(
        managers={
            PackageManager(
                name="pip",
                manifest="requirements.txt",
            ),
        },
        dependency_files={
            DependencyFile(
                name="requirements.txt",
                path="requirements.txt",
                type="manifest",
            ),
        },
        dependencies={
            PackageDependency(
                name="requests",
                version="2.32.0",
                source="requirements.txt",
                metadata=frozenset({
                    (
                        "scope",
                        "runtime",
                    ),
                }),
            ),
        },
        lifecycles={
            BuildLifecycle(
                commands=frozenset({
                    ProjectCommand(
                        name="install",
                        command=(
                            "pip install "
                            "-r requirements.txt"
                        ),
                    ),
                    ProjectCommand(
                        name="test",
                        command="pytest",
                    ),
                }),
            ),
        },
    )


def create_graph():

    store = GraphStore()

    graph_builder = GraphBuilder(
        store,
    )

    workspace_builder = (
        WorkspaceKnowledgeBuilder(
            graph_builder,
        )
    )

    package_builder = (
        PackageManagerKnowledgeBuilder(
            graph_builder,
        )
    )

    return (
        store,
        workspace_builder,
        package_builder,
    )


def test_workspace_and_package_manager_share_graph():

    (
        store,
        workspace_builder,
        package_builder,
    ) = create_graph()

    workspace_builder.build(
        create_workspace(),
    )

    package_builder.build(
        create_package_environment(),
    )

    assert (
        store.get_node(
            "workspace",
        )
        is not None
    )

    assert (
        store.get_node(
            "technology:Python",
        )
        is not None
    )

    assert (
        store.get_node(
            "package-manager:pip",
        )
        is not None
    )

    assert (
        store.get_node(
            "package-dependency:"
            "requests:"
            "2.32.0:"
            "requirements.txt",
        )
        is not None
    )


def test_workspace_relationships_remain_intact():

    (
        store,
        workspace_builder,
        package_builder,
    ) = create_graph()

    workspace_builder.build(
        create_workspace(),
    )

    package_builder.build(
        create_package_environment(),
    )

    query = QueryService(
        store,
    )

    files = (
        query.related_nodes_by_type(
            "workspace",
            EdgeType.CONTAINS,
        )
    )

    names = {
        node.name
        for node in files
    }

    assert "main.py" in names
    assert "utils.py" in names
    assert "requirements.txt" in names


def test_workspace_technology_relationship_remains():

    (
        store,
        workspace_builder,
        package_builder,
    ) = create_graph()

    workspace_builder.build(
        create_workspace(),
    )

    package_builder.build(
        create_package_environment(),
    )

    query = QueryService(
        store,
    )

    technologies = (
        query.related_nodes_by_type(
            "workspace",
            EdgeType.USES,
        )
    )

    names = {
        node.name
        for node in technologies
    }

    assert "Python" in names
    assert "pip" in names


def test_workspace_dependencies_and_package_dependencies_coexist():

    (
        store,
        workspace_builder,
        package_builder,
    ) = create_graph()

    workspace_builder.build(
        create_workspace(),
    )

    package_builder.build(
        create_package_environment(),
    )

    query = QueryService(
        store,
    )

    dependencies = (
        query.related_nodes_by_type(
            "workspace",
            EdgeType.DEPENDS_ON,
        )
    )

    names = {
        node.name
        for node in dependencies
    }

    assert "pytest" in names
    assert "requests" in names


def test_architecture_and_build_lifecycle_coexist():

    (
        store,
        workspace_builder,
        package_builder,
    ) = create_graph()

    workspace_builder.build(
        create_workspace(),
    )

    package_builder.build(
        create_package_environment(),
    )

    query = QueryService(
        store,
    )

    built_with = (
        query.related_nodes_by_type(
            "workspace",
            EdgeType.BUILT_WITH,
        )
    )

    names = {
        node.name
        for node in built_with
    }

    assert "Layered" in names

    assert any(
        node.metadata.get("entity")
        == "build_lifecycle"
        for node in built_with
    )


def test_dependency_properties_are_preserved():

    (
        store,
        workspace_builder,
        package_builder,
    ) = create_graph()

    workspace_builder.build(
        create_workspace(),
    )

    package_builder.build(
        create_package_environment(),
    )

    dependency = store.get_node(
        "package-dependency:"
        "requests:"
        "2.32.0:"
        "requirements.txt",
    )

    assert dependency is not None

    assert (
        dependency.properties["version"]
        == "2.32.0"
    )

    assert (
        dependency.properties["source"]
        == "requirements.txt"
    )

    assert (
        dependency.metadata["scope"]
        == "runtime"
    )


def test_graph_contains_expected_entity_types():

    (
        store,
        workspace_builder,
        package_builder,
    ) = create_graph()

    workspace_builder.build(
        create_workspace(),
    )

    package_builder.build(
        create_package_environment(),
    )

    types = {
        node.type
        for node in store.nodes()
    }

    assert NodeType.PROJECT in types
    assert NodeType.FILE in types
    assert NodeType.DIRECTORY in types
    assert NodeType.TECHNOLOGY in types
    assert NodeType.PACKAGE in types
    assert NodeType.DEPENDENCY in types
    assert NodeType.ARCHITECTURE in types


def test_all_edges_reference_existing_nodes():

    (
        store,
        workspace_builder,
        package_builder,
    ) = create_graph()

    workspace_builder.build(
        create_workspace(),
    )

    package_builder.build(
        create_package_environment(),
    )

    for edge in store.edges():

        assert (
            store.get_node(
                edge.source_id,
            )
            is not None
        )

        assert (
            store.get_node(
                edge.target_id,
            )
            is not None
        )


def test_query_service_can_traverse_final_graph():

    (
        store,
        workspace_builder,
        package_builder,
    ) = create_graph()

    workspace_builder.build(
        create_workspace(),
    )

    package_builder.build(
        create_package_environment(),
    )

    query = QueryService(
        store,
    )

    workspace = query.get_node(
        "workspace",
    )

    assert workspace is not None

    all_related = query.related_nodes(
        workspace.id,
    )

    names = {
        node.name
        for node in all_related
    }

    assert "main.py" in names
    assert "utils.py" in names
    assert "Python" in names
    assert "pip" in names
    assert "pytest" in names
    assert "requests" in names
    assert "Layered" in names