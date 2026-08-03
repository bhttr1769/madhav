from core.ai.exceptions.ai_runtime_error import AIRuntimeError


class ProviderNotFoundError(AIRuntimeError):

    def __init__(self, provider_name: str):
        super().__init__(
            f"Provider '{provider_name}' is not registered."
        )

        self.provider_name = provider_name