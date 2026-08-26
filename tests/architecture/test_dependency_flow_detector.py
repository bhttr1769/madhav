from pathlib import Path

from brain.architecture.detectors.dependency_flow_detector import (
    DependencyFlowDetector,
)

from brain.architecture.models.component import (
    Component,
)

from brain.code.models.import_model import (
    ImportModel,
)


def test_dependency_flow_detects_component_relationship():

    components = frozenset({
        Component(
            name="safety",
            path="brain/safety",
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

    imports = frozenset({
        ImportModel(
            module="brain.models.action",
            name="Action",
            alias=None,
            path="brain/safety/service.py",
        ),
    })

    flows = (
        DependencyFlowDetector().detect(
            components,
            imports,
        )
    )

    assert flows == frozenset({
        next(iter(flows))
    })

    flow = next(
        iter(flows)
    )

    assert flow.source == "safety"
    assert flow.target == "models"
    assert flow.imports == frozenset({
        "brain.models.action",
    })


def test_dependency_flow_ignores_internal_imports():

    components = frozenset({
        Component(
            name="safety",
            path="brain/safety",
            layer="service",
            modules=frozenset(),
        ),
    })

    imports = frozenset({
        ImportModel(
            module="brain.safety.models.action",
            name="Action",
            alias=None,
            path="brain/safety/service.py",
        ),
    })

    flows = (
        DependencyFlowDetector().detect(
            components,
            imports,
        )
    )

    assert flows == frozenset()


def test_dependency_flow_groups_multiple_imports():

    components = frozenset({
        Component(
            name="safety",
            path="brain/safety",
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

    imports = frozenset({
        ImportModel(
            module="brain.models.action",
            name="Action",
            alias=None,
            path="brain/safety/service.py",
        ),
        ImportModel(
            module="brain.models.user",
            name="User",
            alias=None,
            path="brain/safety/manager.py",
        ),
    })

    flows = (
        DependencyFlowDetector().detect(
            components,
            imports,
        )
    )

    assert len(flows) == 1

    flow = next(
        iter(flows)
    )

    assert flow.source == "safety"
    assert flow.target == "models"

    assert flow.imports == frozenset({
        "brain.models.action",
        "brain.models.user",
    })


def test_dependency_flow_ignores_external_imports():

    components = frozenset({
        Component(
            name="safety",
            path="brain/safety",
            layer="service",
            modules=frozenset(),
        ),
    })

    imports = frozenset({
        ImportModel(
            module="os",
            name=None,
            alias=None,
            path="brain/safety/service.py",
        ),
    })

    flows = (
        DependencyFlowDetector().detect(
            components,
            imports,
        )
    )

    assert flows == frozenset()


def test_dependency_flow_handles_empty_input():

    flows = (
        DependencyFlowDetector().detect(
            frozenset(),
            frozenset(),
        )
    )

    assert flows == frozenset()