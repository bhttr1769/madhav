from pathlib import Path

from brain.architecture.detectors.component_detector import (
    ComponentDetector,
)


def test_component_detector_groups_modules():

    files = [
        Path(
            "brain/safety/services/safety_service.py"
        ),
        Path(
            "brain/safety/services/approval_service.py"
        ),
        Path(
            "brain/workspace/workspace_manager.py"
        ),
    ]

    components = (
        ComponentDetector().detect(
            files,
        )
    )

    names = {
        component.name
        for component in components
    }

    assert names == {
        "safety",
        "workspace",
    }


def test_component_detector_collects_modules():

    files = [
        Path(
            "brain/safety/services/safety_service.py"
        ),
        Path(
            "brain/safety/services/approval_service.py"
        ),
    ]

    components = (
        ComponentDetector().detect(
            files,
        )
    )

    safety = next(
        component
        for component in components
        if component.name
        == "safety"
    )

    assert safety.modules == frozenset({
        "safety_service",
        "approval_service",
    })


def test_component_detector_preserves_component_path():

    files = [
        Path(
            "brain/workspace/workspace_manager.py"
        ),
    ]

    components = (
        ComponentDetector().detect(
            files,
        )
    )

    workspace = next(
        component
        for component in components
        if component.name
        == "workspace"
    )

    assert workspace.path == str(
        Path(
            "brain/workspace"
        )
    )


def test_component_detector_handles_empty_input():

    components = (
        ComponentDetector().detect(
            []
        )
    )

    assert components == frozenset()