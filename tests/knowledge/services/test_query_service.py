from brain.knowledge.builders.graph_builder import (
    GraphBuilder,
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


def create_graph():

    store = GraphStore()

    builder = GraphBuilder(
        store,
    )

    project = builder.add_node(
        node_type=NodeType.PROJECT,
        name="Madhav",
        node_id="project-1",
    )

    main_file = builder.add_node(
        node_type=NodeType.FILE,
        name="main.py",
        node_id="file-1",
    )

    utils_file = builder.add_node(
        node_type=NodeType.FILE,
        name="utils.py",
        node_id="file-2",
    )

    flask = builder.add_node(
        node_type=NodeType.PACKAGE,
        name="Flask",
        node_id="package-1",
    )

    builder.add_edge(
        source_id=project.id,
        target_id=main_file.id,
        edge_type=EdgeType.CONTAINS,
        edge_id="edge-1",
    )

    builder.add_edge(
        source_id=project.id,
        target_id=utils_file.id,
        edge_type=EdgeType.CONTAINS,
        edge_id="edge-2",
    )

    builder.add_edge(
        source_id=project.id,
        target_id=flask.id,
        edge_type=EdgeType.USES,
        edge_id="edge-3",
    )

    builder.add_edge(
        source_id=main_file.id,
        target_id=utils_file.id,
        edge_type=EdgeType.IMPORTS,
        edge_id="edge-4",
    )

    return (
        store,
        project,
        main_file,
        utils_file,
        flask,
    )


def test_get_node():

    (
        store,
        project,
        _,
        _,
        _,
    ) = create_graph()

    query = QueryService(
        store,
    )

    assert (
        query.get_node(
            "project-1",
        )
        == project
    )


def test_get_missing_node():

    store, _, _, _, _ = (
        create_graph()
    )

    query = QueryService(
        store,
    )

    assert (
        query.get_node(
            "missing",
        )
        is None
    )


def test_find_by_type():

    (
        store,
        _,
        main_file,
        utils_file,
        _,
    ) = create_graph()

    query = QueryService(
        store,
    )

    result = query.find_by_type(
        NodeType.FILE,
    )

    assert (
        result
        == [
            main_file,
            utils_file,
        ]
    )


def test_find_by_name():

    store, _, main_file, _, _ = (
        create_graph()
    )

    query = QueryService(
        store,
    )

    assert (
        query.find_by_name(
            "main.py",
        )
        == [
            main_file,
        ]
    )


def test_find_by_name_contains():

    (
        store,
        _,
        main_file,
        utils_file,
        _,
    ) = create_graph()

    query = QueryService(
        store,
    )

    result = query.find_by_name_contains(
        ".py",
    )

    assert (
        result
        == [
            main_file,
            utils_file,
        ]
    )


def test_get_edge():

    store, _, _, _, _ = (
        create_graph()
    )

    query = QueryService(
        store,
    )

    edge = query.get_edge(
        "edge-1",
    )

    assert edge is not None

    assert (
        edge.type
        == EdgeType.CONTAINS
    )


def test_outgoing_edges():

    store, project, _, _, _ = (
        create_graph()
    )

    query = QueryService(
        store,
    )

    edges = query.outgoing_edges(
        project.id,
    )

    assert len(edges) == 3

    assert [
        edge.type
        for edge in edges
    ] == [
        EdgeType.CONTAINS,
        EdgeType.CONTAINS,
        EdgeType.USES,
    ]


def test_incoming_edges():

    store, _, _, utils_file, _ = (
        create_graph()
    )

    query = QueryService(
        store,
    )

    edges = query.incoming_edges(
        utils_file.id,
    )

    assert len(edges) == 2

    assert {
        edge.type
        for edge in edges
    } == {
        EdgeType.CONTAINS,
        EdgeType.IMPORTS,
    }


def test_outgoing_edges_by_type():

    store, project, _, _, _ = (
        create_graph()
    )

    query = QueryService(
        store,
    )

    edges = (
        query.outgoing_edges_by_type(
            project.id,
            EdgeType.CONTAINS,
        )
    )

    assert len(edges) == 2

    assert all(
        edge.type
        == EdgeType.CONTAINS
        for edge in edges
    )


def test_incoming_edges_by_type():

    store, _, _, utils_file, _ = (
        create_graph()
    )

    query = QueryService(
        store,
    )

    edges = (
        query.incoming_edges_by_type(
            utils_file.id,
            EdgeType.IMPORTS,
        )
    )

    assert len(edges) == 1

    assert (
        edges[0].source_id
        == "file-1"
    )


def test_related_nodes():

    (
        store,
        project,
        main_file,
        utils_file,
        flask,
    ) = create_graph()

    query = QueryService(
        store,
    )

    result = query.related_nodes(
        project.id,
    )

    assert (
        result
        == [
            main_file,
            utils_file,
            flask,
        ]
    )


def test_related_nodes_by_type():

    (
        store,
        project,
        main_file,
        utils_file,
        _,
    ) = create_graph()

    query = QueryService(
        store,
    )

    result = (
        query.related_nodes_by_type(
            project.id,
            EdgeType.CONTAINS,
        )
    )

    assert (
        result
        == [
            main_file,
            utils_file,
        ]
    )