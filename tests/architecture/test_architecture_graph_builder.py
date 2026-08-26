from brain.architecture.models.architecture_model import (
    ArchitectureModel,
)

from brain.architecture.models.architecture_pattern import (
    ArchitecturePattern,
)

from brain.architecture.models.component import (
    Component,
)

from brain.architecture.models.dependency_flow import (
    DependencyFlow,
)

from brain.architecture.models.layer import (
    Layer,
)

from brain.knowledge.builders.graph_builder import (
    GraphBuilder,
)

from brain.knowledge.integrations.architecture_graph_builder import (
    ArchitectureKnowledgeBuilder,
)

from brain.knowledge.models.edge_type import (
    EdgeType,
)

from brain.knowledge.models.node_type import (
    NodeType,
)

from brain.knowledge.stores.graph_store import (
    GraphStore,
)


def create_builder():
    store = GraphStore()

    builder = GraphBuilder(
        store,
    )

    return (
        store,
        ArchitectureKnowledgeBuilder(
            builder,
        ),
    )


def test_architecture_builder_creates_architecture_node():

    store, builder = create_builder()

    architecture = ArchitectureModel(
        name="workspace",
        pattern="layered",
        components=frozenset({
            "models",
            "services",
        }),
        layers=frozenset({
            "model",
            "service",
        }),
    )

    builder.build(
        architecture=architecture,
        components=frozenset(),
        layers=frozenset(),
        flows=frozenset(),
        patterns=frozenset(),
    )

    node = store.get_node(
        "architecture:workspace",
    )

    assert node is not None
    assert node.type == NodeType.ARCHITECTURE
    assert node.name == "workspace"
    assert node.properties["pattern"] == "layered"


def test_architecture_builder_connects_workspace():

    store, builder = create_builder()

    architecture = ArchitectureModel(
        name="workspace",
        pattern="layered",
        components=frozenset(),
        layers=frozenset(),
    )

    builder.build(
        architecture=architecture,
        components=frozenset(),
        layers=frozenset(),
        flows=frozenset(),
        patterns=frozenset(),
    )

    edge = next(
        edge
        for edge in store.edges()
        if edge.source_id == "workspace"
        and edge.target_id == "architecture:workspace"
    )

    assert edge.type == EdgeType.BUILT_WITH


def test_architecture_builder_creates_components():

    store, builder = create_builder()

    architecture = ArchitectureModel(
        name="workspace",
        pattern="layered",
        components=frozenset({
            "models",
        }),
        layers=frozenset({
            "model",
        }),
    )

    components = frozenset({
        Component(
            name="models",
            path="brain/models",
            layer="model",
            modules=frozenset({
                "user",
            }),
        ),
    })

    builder.build(
        architecture=architecture,
        components=components,
        layers=frozenset(),
        flows=frozenset(),
        patterns=frozenset(),
    )

    node = store.get_node(
        "architecture-component:models",
    )

    assert node is not None
    assert node.type == NodeType.DIRECTORY
    assert node.properties["path"] == "brain/models"
    assert node.properties["layer"] == "model"


def test_architecture_builder_creates_layers():

    store, builder = create_builder()

    architecture = ArchitectureModel(
        name="workspace",
        pattern="layered",
        components=frozenset({
            "models",
        }),
        layers=frozenset({
            "model",
        }),
    )

    layers = frozenset({
        Layer(
            name="model",
            components=frozenset({
                "models",
            }),
            confidence=0.9,
        ),
    })

    builder.build(
        architecture=architecture,
        components=frozenset(),
        layers=layers,
        flows=frozenset(),
        patterns=frozenset(),
    )

    node = store.get_node(
        "architecture-layer:model",
    )

    assert node is not None
    assert node.type == NodeType.ARCHITECTURE
    assert node.properties["confidence"] == 0.9


def test_architecture_builder_creates_patterns():

    store, builder = create_builder()

    architecture = ArchitectureModel(
        name="workspace",
        pattern="layered",
        components=frozenset(),
        layers=frozenset(),
    )

    patterns = frozenset({
        ArchitecturePattern(
            name="layered",
            confidence=0.85,
            evidence=frozenset({
                "multiple architectural layers",
            }),
        ),
    })

    builder.build(
        architecture=architecture,
        components=frozenset(),
        layers=frozenset(),
        flows=frozenset(),
        patterns=patterns,
    )

    node = store.get_node(
        "architecture-pattern:layered",
    )

    assert node is not None
    assert node.type == NodeType.ARCHITECTURE
    assert node.properties["confidence"] == 0.85


def test_architecture_builder_creates_dependency_flow():

    store, builder = create_builder()

    architecture = ArchitectureModel(
        name="workspace",
        pattern="layered",
        components=frozenset({
            "services",
            "models",
        }),
        layers=frozenset({
            "service",
            "model",
        }),
    )

    components = frozenset({
        Component(
            name="services",
            path="brain/services",
            layer="service",
            modules=frozenset(),
        ),
        Component(
            name="models",
            path="brain/models",
            layer="model",
            modules=frozenset(),
        ),
    })

    flows = frozenset({
        DependencyFlow(
            source="services",
            target="models",
            imports=frozenset({
                "brain.models.user",
            }),
        ),
    })

    builder.build(
        architecture=architecture,
        components=components,
        layers=frozenset(),
        flows=flows,
        patterns=frozenset(),
    )

    source = store.get_node(
        "architecture-component:services",
    )

    target = store.get_node(
        "architecture-component:models",
    )

    assert source is not None
    assert target is not None

    edge = next(
        edge
        for edge in store.edges()
        if edge.source_id == source.id
        and edge.target_id == target.id
    )

    assert edge.type == EdgeType.DEPENDS_ON

    assert edge.properties["imports"] == [
        "brain.models.user",
    ]