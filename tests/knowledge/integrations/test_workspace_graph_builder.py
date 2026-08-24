from brain.knowledge.builders.graph_builder import (
    GraphBuilder,
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
            Signature(
                value=".py",
                category="extension",
                path="src/main.py",
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
            Dependency(
                name="pytest",
            ),
        },
        architectures={
            Architecture(
                name="Layered",
            ),
        },
    )


def create_builder():

    store = GraphStore()

    graph_builder = GraphBuilder(
        store,
    )

    workspace_builder = (
        WorkspaceKnowledgeBuilder(
            graph_builder,
        )
    )

    return (
        store,
        workspace_builder,
    )


def test_workspace_node_is_created():

    store, builder = (
        create_builder()
    )

    builder.build(
        create_workspace(),
    )

    node = store.get_node(
        "workspace",
    )

    assert node is not None

    assert (
        node.type
        == NodeType.PROJECT
    )

    assert (
        node.name
        == "Workspace"
    )

    assert (
        node.properties["files"]
        == 2
    )

    assert (
        node.properties["directories"]
        == 1
    )


def test_file_nodes_are_created():

    store, builder = (
        create_builder()
    )

    builder.build(
        create_workspace(),
    )

    node = store.get_node(
        "filename:src/main.py",
    )

    assert node is not None

    assert (
        node.type
        == NodeType.FILE
    )

    assert (
        node.name
        == "main.py"
    )

    assert (
        node.properties["path"]
        == "src/main.py"
    )


def test_directory_nodes_are_created():

    store, builder = (
        create_builder()
    )

    builder.build(
        create_workspace(),
    )

    node = store.get_node(
        "directory:src",
    )

    assert node is not None

    assert (
        node.type
        == NodeType.DIRECTORY
    )


def test_extension_signatures_are_not_nodes():

    store, builder = (
        create_builder()
    )

    builder.build(
        create_workspace(),
    )

    nodes = store.nodes()

    assert not any(
        node.name == ".py"
        for node in nodes
    )


def test_technology_node_is_created():

    store, builder = (
        create_builder()
    )

    builder.build(
        create_workspace(),
    )

    node = store.get_node(
        "technology:Python",
    )

    assert node is not None

    assert (
        node.type
        == NodeType.TECHNOLOGY
    )

    assert (
        node.properties["category"]
        == "language"
    )


def test_dependency_node_is_created():

    store, builder = (
        create_builder()
    )

    builder.build(
        create_workspace(),
    )

    node = store.get_node(
        "dependency:pytest",
    )

    assert node is not None

    assert (
        node.type
        == NodeType.DEPENDENCY
    )


def test_architecture_node_is_created():

    store, builder = (
        create_builder()
    )

    builder.build(
        create_workspace(),
    )

    node = store.get_node(
        "architecture:Layered",
    )

    assert node is not None

    assert (
        node.type
        == NodeType.ARCHITECTURE
    )


def test_workspace_contains_files():

    store, builder = (
        create_builder()
    )

    builder.build(
        create_workspace(),
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

    file_names = {
        node.name
        for node in files
    }

    assert (
        "main.py"
        in file_names
    )

    assert (
        "utils.py"
        in file_names
    )


def test_workspace_uses_technology():

    store, builder = (
        create_builder()
    )

    builder.build(
        create_workspace(),
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

    assert [
        node.name
        for node in technologies
    ] == [
        "Python",
    ]


def test_workspace_depends_on_dependency():

    store, builder = (
        create_builder()
    )

    builder.build(
        create_workspace(),
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
        "pytest",
    ]


def test_workspace_builds_architecture_relationship():

    store, builder = (
        create_builder()
    )

    builder.build(
        create_workspace(),
    )

    query = QueryService(
        store,
    )

    architectures = (
        query.related_nodes_by_type(
            "workspace",
            EdgeType.BUILT_WITH,
        )
    )

    assert [
        node.name
        for node in architectures
    ] == [
        "Layered",
    ]