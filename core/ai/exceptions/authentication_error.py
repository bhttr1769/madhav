from core.ai.exceptions.ai_runtime_error import AIRuntimeError


class AuthenticationError(AIRuntimeError):

    def __init__(self):
        super().__init__("Authentication failed.")