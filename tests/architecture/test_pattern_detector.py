from brain.architecture.detectors.pattern_detector import (
    PatternDetector,
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


def test_pattern_detector_detects_layered_architecture():

    components = frozenset({
        Component(
            name="models",
            path="brain/models",
            layer="model",
            modules=frozenset(),
        ),
        Component(
            name="services",
            path="brain/services",
            layer="service",
            modules=frozenset(),
        ),
        Component(
            name="storage",
            path="brain/storage",
            layer="storage",
            modules=frozenset(),
        ),
    })

    layers = frozenset({
        Layer(
            name="model",
            components=frozenset({
                "models",
            }),
            confidence=1.0,
        ),
        Layer(
            name="service",
            components=frozenset({
                "services",
            }),
            confidence=1.0,
        ),
        Layer(
            name="storage",
            components=frozenset({
                "storage",
            }),
            confidence=1.0,
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
        DependencyFlow(
            source="services",
            target="storage",
            imports=frozenset({
                "brain.storage.database",
            }),
        ),
    })

    patterns = PatternDetector().detect(
        components,
        layers,
        flows,
    )

    assert len(patterns) == 1

    pattern = next(
        iter(patterns)
    )

    assert pattern.name == "layered"

    assert (
        pattern.confidence
        >= 0.8
    )

    assert (
        "multiple architectural layers"
        in pattern.evidence
    )


def test_pattern_detector_requires_multiple_layers():

    components = frozenset({
        Component(
            name="services",
            path="brain/services",
            layer="service",
            modules=frozenset(),
        ),
    })

    layers = frozenset({
        Layer(
            name="service",
            components=frozenset({
                "services",
            }),
            confidence=1.0,
        ),
    })

    patterns = PatternDetector().detect(
        components,
        layers,
        frozenset(),
    )

    assert patterns == frozenset()


def test_pattern_detector_increases_confidence_with_dependency_flow():

    components = frozenset({
        Component(
            name="models",
            path="brain/models",
            layer="model",
            modules=frozenset(),
        ),
        Component(
            name="services",
            path="brain/services",
            layer="service",
            modules=frozenset(),
        ),
    })

    layers = frozenset({
        Layer(
            name="model",
            components=frozenset({
                "models",
            }),
            confidence=1.0,
        ),
        Layer(
            name="service",
            components=frozenset({
                "services",
            }),
            confidence=1.0,
        ),
    })

    without_flow = PatternDetector().detect(
        components,
        layers,
        frozenset(),
    )

    with_flow = PatternDetector().detect(
        components,
        layers,
        frozenset({
            DependencyFlow(
                source="services",
                target="models",
                imports=frozenset({
                    "brain.models.user",
                }),
            ),
        }),
    )

    first = next(
        iter(without_flow)
    )

    second = next(
        iter(with_flow)
    )

    assert (
        second.confidence
        > first.confidence
    )


def test_pattern_detector_handles_empty_input():

    patterns = PatternDetector().detect(
        frozenset(),
        frozenset(),
        frozenset(),
    )

    assert patterns == frozenset()