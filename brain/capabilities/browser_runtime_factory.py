
from brain.browser.interactive import browser_capability as browser_module
from brain.capabilities.capability_executor import CapabilityExecutor
from brain.capabilities.capability_registry import CapabilityRegistry
from brain.capabilities.capability_runtime import CapabilityRuntime
from brain.safety.services.safety_service import SafetyService


def create_browser_capability_runtime(
    safety_service: SafetyService,
) -> CapabilityRuntime:
    """
    Compose the interactive browser capability with explicit
    safety enforcement and the existing capability runtime.

    The caller must supply a fully configured SafetyService.
    Browser-session configuration remains the caller's responsibility.
    """
    if not isinstance(safety_service, SafetyService):
        raise TypeError(
            "safety_service must be a SafetyService"
        )

    browser = browser_module.configure_browser_capability(
        safety_service
    )

    registry = CapabilityRegistry(
        capabilities=(
            browser.capability_descriptor(),
        )
    )

    executor = CapabilityExecutor(
        registry=registry,
    )

    return CapabilityRuntime(
        executor=executor,
    )
