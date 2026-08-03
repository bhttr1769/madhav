from core.ai.exceptions.ai_runtime_error import AIRuntimeError


class UnsupportedCapabilityError(AIRuntimeError):

    def __init__(self, capability: str):
        super().__init__(
            f"Provider does not support '{capability}'."
        )
        self.capability = capability