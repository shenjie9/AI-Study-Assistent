import requests

from llm.provider import LLMProvider


class OllamaProvider(LLMProvider):

    def __init__(self, model="llama3.2:1b"):
        self.model = model

    def generate(self, prompt):

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )

        response.raise_for_status()

        return response.json()["response"]