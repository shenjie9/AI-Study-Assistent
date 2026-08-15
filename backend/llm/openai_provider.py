import os

from dotenv import load_dotenv
from openai import OpenAI

from llm.provider import LLMProvider

load_dotenv()


class OpenAIProvider(LLMProvider):
    def __init__(self, model="gpt-4.1-mini"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OpenAI is supported, but OPENAI_API_KEY is not configured."
            )

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, prompt):
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )
        return response.output_text
