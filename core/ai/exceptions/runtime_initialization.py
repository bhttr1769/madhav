from core.ai.exceptions.ai_runtime_error import AIRuntimeError


class RuntimeInitializationError(AIRuntimeError):

    def __init__(self, message: str):
        super().__init__(message)