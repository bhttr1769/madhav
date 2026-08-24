from brain.knowledge.builders.graph_builder import (
    GraphBuilder,
)

from brain.knowledge.integrations.package_manager_graph_builder import (
    PackageManagerKnowledgeBuilder,
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
    Dependency,
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


def create_environment():

    return PackageManagerEnvironment(
        managers={
            PackageManager(
                name="Maven",
                manifest="pom.xml",
            ),
        },
        dependency_files={
            DependencyFile(
                name="pom.xml",
                path="pom.xml",
                type="manifest",
            ),
        },
        dependencies={
            Dependency(
                name="spring-boot",
                version="3.5.0",
                source="pom.xml",
                metadata=frozenset({
                    (
                        "scope",
                        "compile",
                    ),
                }),
            ),
        },
        lifecycles={
            BuildLifecycle(
                commands=frozenset({
                    ProjectCommand(
                        name="build",
                        command="mvn package",
                    ),
                    ProjectCommand(
                        name="test",
                        command="mvn test",
                    ),
                }),
            ),
        },
    )


def create_builder():

    store = GraphStore()

    graph_builder = GraphBuilder(
        store,
    )

    package_builder = (
        PackageManagerKnowledgeBuilder(
            graph_builder,
        )
    )

    return (
        store,
        package_builder,
    )


def test_package_manager_node_is_created():

    store, builder = (
        create_builder()
    )

    builder.build(
        create_environment(),
    )

    node = store.get_node(
        "package-manager:Maven",
    )

    assert node is not None

    assert (
        node.type
        == NodeType.PACKAGE
    )

    assert (
        node.name
        == "Maven"
    )

    assert (
        node.properties["manifest"]
        == "pom.xml"
    )


def test_dependency_file_node_is_created():

    store, builder = (
        create_builder()
    )

    builder.build(
        create_environment(),
    )

    node = store.get_node(
        "dependency-file:pom.xml",
    )

    assert node is not None

    assert (
        node.type
        == NodeType.FILE
    )

    assert (
        node.name
        == "pom.xml"
    )

    assert (
        node.properties["path"]
        == "pom.xml"
    )

    assert (
        node.properties["type"]
        == "manifest"
    )


def test_dependency_node_is_created():

    store, builder = (
        create_builder()
    )

    builder.build(
        create_environment(),
    )

    node = store.get_node(
        "package-dependency:"
        "spring-boot:"
        "3.5.0:"
        "pom.xml",
    )

    assert node is not None

    assert (
        node.type
        == NodeType.DEPENDENCY
    )

    assert (
        node.name
        == "spring-boot"
    )

    assert (
        node.properties["version"]
        == "3.5.0"
    )

    assert (
        node.properties["source"]
        == "pom.xml"
    )


def test_dependency_metadata_is_preserved():

    store, builder = (
        create_builder()
    )

    builder.build(
        create_environment(),
    )

    node = store.get_node(
        "package-dependency:"
        "spring-boot:"
        "3.5.0:"
        "pom.xml",
    )

    assert (
        node.metadata["scope"]
        == "compile"
    )


def test_lifecycle_node_is_created():

    store, builder = (
        create_builder()
    )

    builder.build(
        create_environment(),
    )

    node = store.get_node(
        "build-lifecycle:0",
    )

    assert node is not None

    assert (
        node.type
        == NodeType.ARCHITECTURE
    )

    assert (
        node.metadata["entity"]
        == "build_lifecycle"
    )

    assert len(
        node.properties["commands"]
    ) == 2


def test_workspace_uses_package_manager():

    store, builder = (
        create_builder()
    )

    builder.build(
        create_environment(),
    )

    query = QueryService(
        store,
    )

    managers = (
        query.related_nodes_by_type(
            "workspace",
            EdgeType.USES,
        )
    )

    assert [
        node.name
        for node in managers
    ] == [
        "Maven",
    ]


def test_workspace_contains_dependency_file():

    store, builder = (
        create_builder()
    )

    builder.build(
        create_environment(),
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

    assert [
        node.name
        for node in files
    ] == [
        "pom.xml",
    ]


def test_workspace_depends_on_dependency():

    store, builder = (
        create_builder()
    )

    builder.build(
        create_environment(),
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

    assert [
        node.name
        for node in dependencies
    ] == [
        "spring-boot",
    ]


def test_workspace_built_with_lifecycle():

    store, builder = (
        create_builder()
    )

    builder.build(
        create_environment(),
    )

    query = QueryService(
        store,
    )

    lifecycles = (
        query.related_nodes_by_type(
            "workspace",
            EdgeType.BUILT_WITH,
        )
    )

    assert len(lifecycles) == 1

    assert (
        lifecycles[0].metadata["entity"]
        == "build_lifecycle"
    )


def test_custom_workspace_id():

    store, builder = (
        create_builder()
    )

    builder.build(
        create_environment(),
        workspace_id="project-123",
    )

    assert (
        store.get_node(
            "project-123",
        )
        is not None
    )

    manager = store.get_node(
        "package-manager:Maven",
    )

    assert manager is not None

    edges = [
        edge
        for edge in store.edges()
        if edge.source_id
        == "project-123"
        and edge.target_id
        == manager.id
    ]

    assert len(edges) == 1

    assert (
        edges[0].type
        == EdgeType.USES
    )