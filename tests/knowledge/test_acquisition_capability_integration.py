from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from brain.browser.integrations.browser_knowledge_integrator import (
    BrowserKnowledgeIntegrator,
)
from brain.capabilities.capability_discovery import (
    CapabilityDiscovery,
)
from brain.capabilities.capability_executor import (
    CapabilityExecutor,
)
from brain.capabilities.capability_integrator import (
    CapabilityIntegrator,
)
from brain.capabilities.capability_registry import (
    CapabilityRegistry,
)
from brain.capabilities.entry_point_resolver import (
    EntryPointResolver,
)
from brain.knowledge.acquisition_capability import (
    AcquisitionCapability,
)
from brain.manager import BrainManager
from brain.models.document import Document


def create_document(
    name: str,
    source: str,
) -> Document:
    timestamp = datetime.now()

    return Document(
        name=name,
        path=Path(name),
        extension=Path(name).suffix,
        content="test content",
        size=12,
        created_at=timestamp,
        modified_at=timestamp,
        language="unknown",
        source=source,
    )


def create_acquisition_capability():
    browser_integrator = MagicMock(
        spec=BrowserKnowledgeIntegrator
    )

    brain_manager = MagicMock(
        spec=BrainManager
    )

    capability = AcquisitionCapability(
        browser_integrator=browser_integrator,
        brain_manager=brain_manager,
    )

    return (
        capability,
        browser_integrator,
        brain_manager,
    )


class InjectedCapabilityResolver(
    EntryPointResolver
):
    def __init__(
        self,
        capability: AcquisitionCapability,
    ):
        self._capability = capability

    def resolve(
        self,
        entry_point: str,
    ) -> object:
        return self._capability


def test_acquisition_capability_is_discoverable():
    capability, _, _ = (
        create_acquisition_capability()
    )

    discovery = CapabilityDiscovery(
        providers=(capability,)
    )

    discovered = discovery.discover()

    assert len(discovered) == 1
    assert discovered[0].id == (
        "knowledge.acquisition"
    )


def test_acquisition_capability_can_be_registered():
    capability, _, _ = (
        create_acquisition_capability()
    )

    discovery = CapabilityDiscovery(
        providers=(capability,)
    )

    descriptor = discovery.discover()[0]

    registry = CapabilityRegistry()

    registry.register(descriptor)

    assert registry.has(
        "knowledge.acquisition"
    )

    assert (
        registry.get(
            "knowledge.acquisition"
        )
        == descriptor
    )


def test_acquisition_capability_integrates_into_registry():
    capability, _, _ = (
        create_acquisition_capability()
    )

    descriptor = (
        capability.capability_descriptor()
    )

    registry = CapabilityRegistry()

    integrator = CapabilityIntegrator(
        registry
    )

    integrator.integrate(
        capability=descriptor,
        verification_passed=True,
    )

    assert registry.has(
        "knowledge.acquisition"
    )

    assert registry.get(
        "knowledge.acquisition"
    ) == descriptor


def test_browser_acquisition_executes_through_capability_executor():
    (
        capability,
        browser_integrator,
        _,
    ) = create_acquisition_capability()

    document = create_document(
        name="example.html",
        source="browser",
    )

    browser_integrator.learn.return_value = (
        document
    )

    descriptor = (
        capability.capability_descriptor()
    )

    registry = CapabilityRegistry(
        capabilities=(descriptor,)
    )

    resolver = InjectedCapabilityResolver(
        capability
    )

    executor = CapabilityExecutor(
        registry=registry,
        resolver=resolver,
    )

    result = executor.execute(
        "knowledge.acquisition",
        {
            "source": "browser",
            "url": "https://example.com",
        },
    )

    browser_integrator.learn.assert_called_once_with(
        "https://example.com"
    )

    assert result is document


def test_file_acquisition_executes_through_capability_executor():
    (
        capability,
        _,
        brain_manager,
    ) = create_acquisition_capability()

    document = create_document(
        name="example.txt",
        source="local",
    )

    brain_manager.read.return_value = document
    brain_manager.learn_document.return_value = (
        document
    )

    descriptor = (
        capability.capability_descriptor()
    )

    registry = CapabilityRegistry(
        capabilities=(descriptor,)
    )

    resolver = InjectedCapabilityResolver(
        capability
    )

    executor = CapabilityExecutor(
        registry=registry,
        resolver=resolver,
    )

    result = executor.execute(
        "knowledge.acquisition",
        {
            "source": "file",
            "path": "example.txt",
        },
    )

    brain_manager.read.assert_called_once_with(
        "example.txt"
    )

    brain_manager.learn_document.assert_called_once_with(
        document
    )

    assert result is document


def test_browser_and_file_share_same_capability_entry_point():
    capability, _, _ = (
        create_acquisition_capability()
    )

    descriptor = (
        capability.capability_descriptor()
    )

    assert descriptor.id == (
        "knowledge.acquisition"
    )

    assert descriptor.entry_point == (
        "brain.knowledge.acquisition_capability."
        "AcquisitionCapability"
    )


def test_capability_dependencies_are_empty():
    capability, _, _ = (
        create_acquisition_capability()
    )

    descriptor = (
        capability.capability_descriptor()
    )

    assert descriptor.dependencies == frozenset()


def test_browser_acquisition_failure_propagates_through_executor():
    (
        capability,
        browser_integrator,
        _,
    ) = create_acquisition_capability()

    browser_integrator.learn.side_effect = (
        RuntimeError("browser acquisition failed")
    )

    descriptor = (
        capability.capability_descriptor()
    )

    registry = CapabilityRegistry(
        capabilities=(descriptor,)
    )

    resolver = InjectedCapabilityResolver(
        capability
    )

    executor = CapabilityExecutor(
        registry=registry,
        resolver=resolver,
    )

    with pytest.raises(
        RuntimeError,
        match="browser acquisition failed",
    ):
        executor.execute(
            "knowledge.acquisition",
            {
                "source": "browser",
                "url": "https://example.com",
            },
        )


def test_file_acquisition_failure_propagates_through_executor():
    (
        capability,
        _,
        brain_manager,
    ) = create_acquisition_capability()

    brain_manager.read.side_effect = (
        RuntimeError("file acquisition failed")
    )

    descriptor = (
        capability.capability_descriptor()
    )

    registry = CapabilityRegistry(
        capabilities=(descriptor,)
    )

    resolver = InjectedCapabilityResolver(
        capability
    )

    executor = CapabilityExecutor(
        registry=registry,
        resolver=resolver,
    )

    with pytest.raises(
        RuntimeError,
        match="file acquisition failed",
    ):
        executor.execute(
            "knowledge.acquisition",
            {
                "source": "file",
                "path": "example.txt",
            },
        )