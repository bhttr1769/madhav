from core.ai.exceptions.ai_runtime_error import AIRuntimeError


class ModelNotFoundError(AIRuntimeError):

    def __init__(self, model_name: str):
        super().__init__(
            f"Model '{model_name}' was not found."
        )
        self.model_name = model_name