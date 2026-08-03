from core.ai.exceptions.ai_runtime_error import AIRuntimeError


class TimeoutError(AIRuntimeError):

    def __init__(self):
        super().__init__("The request timed out.")