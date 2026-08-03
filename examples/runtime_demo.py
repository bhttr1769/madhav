from core.ai.config.model_config import ModelConfig
from core.ai.config.provider_config import ProviderConfig
from core.ai.config.runtime_config import RuntimeConfig
from core.ai.runtime.runtime_factory import RuntimeFactory


def main():

    config = RuntimeConfig(
        provider=ProviderConfig(
            name="ollama",
            endpoint="http://localhost:11434",
        ),
        chat_model=ModelConfig(
            name="qwen2.5:1.5b",
        ),
        embedding_model=ModelConfig(
            name="nomic-embed-text",
        ),
    )

    runtime = RuntimeFactory.create(config)

    # Test Chat
    print("===== CHAT =====")
    print(runtime.chat.chat("Hello! Who are you?"))

    # Test Embeddings
    print("\n===== EMBEDDINGS =====")

    vector = runtime.embedding.embed("Hello World")

    print(f"Vector Dimensions : {len(vector)}")
    print(f"First 10 values   : {vector[:10]}")

    #Test Health
    print("\n===== HEALTH =====")

    health = runtime.health.status()

    print(health)


if __name__ == "__main__":
    main()