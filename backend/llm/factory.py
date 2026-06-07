from llm.ollama_provider import OllamaProvider
from llm.openai_provider import OpenAIProvider


def get_provider(provider_name):

    if provider_name == "ollama":
        return OllamaProvider()

    if provider_name == "openai":
        return OpenAIProvider()

    raise ValueError(
        f"Unknown provider: {provider_name}"
    )