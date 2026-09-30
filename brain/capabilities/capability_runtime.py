from brain.capabilities.capability_executor import CapabilityExecutor
from brain.capabilities.models.capability_execution_request import (
    CapabilityExecutionRequest,
)
from brain.capabilities.models.capability_execution_result import (
    CapabilityExecutionResult,
)


class CapabilityRuntime:
    def __init__(
        self,
        executor: CapabilityExecutor,
    ):
        if not isinstance(executor, CapabilityExecutor):
            raise TypeError(
                "executor must be a CapabilityExecutor"
            )

        self._executor = executor

    def execute(
        self,
        request: CapabilityExecutionRequest,
    ) -> CapabilityExecutionResult:
        if not isinstance(
            request,
            CapabilityExecutionRequest,
        ):
            raise TypeError(
                "request must be a CapabilityExecutionRequest"
            )

        output = self._executor.execute(
            capability_id=request.capability_id,
            input_data=request.input_data,
        )

        return CapabilityExecutionResult(
            capability_id=request.capability_id,
            output=output,
        )