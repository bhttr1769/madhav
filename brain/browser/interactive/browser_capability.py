import os

from brain.browser.interactive.browser_observation_builder import (
    BrowserObservationBuilder,
)
from brain.browser.interactive.browser_session import BrowserSession
from brain.browser.interactive.models.browser_action import BrowserAction
from brain.browser.interactive.models.browser_observation import (
    BrowserObservation,
)
from brain.browser.interactive.playwright_browser_executor import (
    PlaywrightBrowserExecutor,
)
from brain.browser.interactive.playwright_browser_session import (
    PlaywrightBrowserSession,
)
from brain.browser.interactive.safety_browser_action_executor import (
    SafetyBrowserActionExecutor,
)
from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)
from brain.safety.services.safety_service import SafetyService


class BrowserCapability:
    """
    Composes the interactive browser subsystem into one
    capability compatible with the existing capability runtime.

    The capability owns one persistent BrowserSession so that
    browser state survives across multiple capability executions.
    """

    CAPABILITY_ID = "browser.interactive"

    def __init__(
        self,
        session: BrowserSession | None = None,
        safety_service: SafetyService | None = None,
        observation_builder: BrowserObservationBuilder | None = None,
        action_executor: SafetyBrowserActionExecutor | None = None,
    ):
        if session is not None and not isinstance(
            session,
            BrowserSession,
        ):
            raise TypeError(
                "session must be a BrowserSession"
            )

        if safety_service is not None and not isinstance(
            safety_service,
            SafetyService,
        ):
            raise TypeError(
                "safety_service must be a SafetyService"
            )

        if observation_builder is not None and not isinstance(
            observation_builder,
            BrowserObservationBuilder,
        ):
            raise TypeError(
                "observation_builder must be a "
                "BrowserObservationBuilder"
            )

        if action_executor is not None and not isinstance(
           action_executor,
           SafetyBrowserActionExecutor,
        ):
            raise TypeError(
            "action_executor must be a "
            "SafetyBrowserActionExecutor"
        )

        self._session = session
        self._safety_service = safety_service
        self._observation_builder = (
            observation_builder
            if observation_builder is not None
            else BrowserObservationBuilder()
        )

        self._executor = action_executor

    def capability_descriptor(self) -> CapabilityDescriptor:
        return CapabilityDescriptor(
            id=self.CAPABILITY_ID,
            name="Interactive Browser",
            description=(
                "Provides controlled interactive browser "
                "session, navigation, observation, and "
                "browser action execution."
            ),
            version="1.0.0",
            entry_point=(
                "brain.browser.interactive."
                "browser_capability.browser_capability"
            ),
            dependencies=frozenset(),
            input_contract="browser_command",
            output_contract="browser_result",
        )

    def execute(self, input_data: object) -> object:
        if not isinstance(input_data, dict):
            raise TypeError(
                "input_data must be a dict"
            )

        operation = input_data.get("operation")

        if not isinstance(operation, str):
            raise TypeError(
                "operation must be a string"
            )

        if not operation.strip():
            raise ValueError(
                "operation must not be empty"
            )

        if operation == "start":
            return self._start()

        if operation == "close":
            return self._close()

        if operation == "navigate":
            return self._navigate(input_data)

        if operation == "observe":
            return self._observe()

        if operation == "action":
            return self._action(input_data)

        raise ValueError(
            f"unsupported browser operation: {operation}"
        )

    def _start(self) -> BrowserObservation | object:
        session = self._ensure_session()

        session.start()

        return session.current_state()

    def _close(self) -> object:
        if self._session is None:
            return None

        self._session.close()

        return self._session.current_state()

    def _navigate(self, input_data: dict) -> object:
        self._ensure_session()
        executor = self._ensure_executor()

        url = input_data.get("url")

        if not isinstance(url, str):
            raise TypeError(
                "navigate operation requires a string url"
            )

        action = BrowserAction(
            action_type="navigate",
            url=url,
        )

        approval = input_data.get("approval")

        executor.execute(
            action,
            approval,
        ) 

        return self._session.current_state()

    def _observe(self) -> frozenset:
        session = self._ensure_session()

        observation = session.observe()

        return self._observation_builder.build(
            observation
        )

    def _action(self, input_data: dict) -> object:
        self._ensure_session()
        executor = self._ensure_executor()

        action = input_data.get("action")

        if not isinstance(action, BrowserAction):
            raise TypeError(
                "action operation requires a BrowserAction"
            )

        approval = input_data.get("approval")

        executor.execute(
            action,
            approval,
        )

        return self._session.current_state()

    def _ensure_session(self) -> BrowserSession:
        if self._session is not None:
            return self._session

        executable_path = os.environ.get(
            "MADHAV_BROWSER_EXECUTABLE_PATH"
        )

        if not executable_path:
            raise RuntimeError(
                "browser session is not configured; "
                "provide a BrowserSession or set "
                "MADHAV_BROWSER_EXECUTABLE_PATH"
            )

        self._session = PlaywrightBrowserSession(
            executable_path=executable_path,
        )

        return self._session

    def _ensure_executor(self) -> SafetyBrowserActionExecutor:
        if self._executor is not None:
            return self._executor

        if self._safety_service is None:
            raise RuntimeError(
                "safety service is not configured"
            )

        self._executor = SafetyBrowserActionExecutor(
            safety_service=self._safety_service,
            executor=PlaywrightBrowserExecutor(
                self._ensure_session()
            ),
        )

        return self._executor


browser_capability = BrowserCapability()