from ollama import Client, ResponseError

from core.ai.config.runtime_config import RuntimeConfig
from core.ai.providers.base.base_chat_provider import BaseChatProvider
from core.ai.providers.base.base_embedding_provider import (
    BaseEmbeddingProvider,
)
from ollama import ResponseError

from core.ai.exceptions import (
    ModelNotFoundError,
    ProviderUnavailableError,
)


class OllamaProvider(
    BaseChatProvider,
    BaseEmbeddingProvider,
):
    """
    AI provider backed by a local Ollama server.
    """

    def __init__(self, config: RuntimeConfig):
        self._config = config
        self._client = Client(
            host=config.provider.endpoint,
        )

    @property
    def name(self) -> str:
        return self._config.provider.name

    def is_available(self) -> bool:
        try:
            self._client.list()
            return True
        except Exception:
            return False

    def chat(self, prompt: str) -> str:

        try:

            response = self._client.chat(
                model=self._config.chat_model.name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            return response["message"]["content"]

        except ResponseError as e:

            if e.status_code == 404:
                raise ModelNotFoundError(
                    self._config.chat_model.name
                ) from e

            raise

        except ConnectionError as e:

            raise ProviderUnavailableError(
                self.name
            ) from e

    def embed(self, text: str) -> list[float]:

        try:

            response = self._client.embed(
                model=self._config.embedding_model.name,
                input=text,
            )

            return response["embeddings"][0]

        except ResponseError as e:
        
            if e.status_code == 404:
                raise ModelNotFoundError(
                    self._config.embedding_model.name
                ) from e

            raise

        except ConnectionError as e:

            raise ProviderUnavailableError(
                self.name
            ) from e