from brain.architecture.detectors.layer_detector import (
    LayerDetector,
)

from brain.architecture.models.component import (
    Component,
)


def test_layer_detector_identifies_model_layer():

    components = frozenset({
        Component(
            name="models",
            path="brain/models",
            layer=None,
            modules=frozenset({
                "user",
                "project",
            }),
        ),
    })

    layers = LayerDetector().detect(
        components,
    )

    names = {
        layer.name
        for layer in layers
    }

    assert names == {
        "model",
    }


def test_layer_detector_identifies_multiple_layers():

    components = frozenset({
        Component(
            name="models",
            path="brain/models",
            layer=None,
            modules=frozenset({
                "user",
            }),
        ),
        Component(
            name="services",
            path="brain/services",
            layer=None,
            modules=frozenset({
                "user_service",
            }),
        ),
        Component(
            name="storage",
            path="brain/storage",
            layer=None,
            modules=frozenset({
                "database",
            }),
        ),
    })

    layers = LayerDetector().detect(
        components,
    )

    names = {
        layer.name
        for layer in layers
    }

    assert names == {
        "model",
        "service",
        "storage",
    }


def test_layer_detector_groups_components():

    components = frozenset({
        Component(
            name="models",
            path="brain/models",
            layer=None,
            modules=frozenset(),
        ),
        Component(
            name="domain",
            path="brain/domain",
            layer=None,
            modules=frozenset(),
        ),
    })

    layers = LayerDetector().detect(
        components,
    )

    model_layer = next(
        layer
        for layer in layers
        if layer.name == "model"
    )

    assert (
        model_layer.components
        == frozenset({
            "models",
            "domain",
        })
    )


def test_layer_detector_ignores_unknown_components():

    components = frozenset({
        Component(
            name="utils",
            path="brain/utils",
            layer=None,
            modules=frozenset(),
        ),
    })

    layers = LayerDetector().detect(
        components,
    )

    assert layers == frozenset()


def test_layer_detector_uses_full_confidence_for_exact_match():

    components = frozenset({
        Component(
            name="services",
            path="brain/services",
            layer=None,
            modules=frozenset(),
        ),
    })

    layers = LayerDetector().detect(
        components,
    )

    service_layer = next(
        layer
        for layer in layers
    )

    assert (
        service_layer.confidence
        == 1.0
    )