from core.ai.exceptions.ai_runtime_error import AIRuntimeError


class RateLimitError(AIRuntimeError):

    def __init__(self):
        super().__init__("Rate limit exceeded.")