import os

from dotenv import load_dotenv
from openai import OpenAI

from llm.provider import LLMProvider

load_dotenv()


class OpenAIProvider(LLMProvider):

    def __init__(self, model="gpt-4.1-mini"):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.model = model

    def generate(self, prompt):

        response = self.client.responses.create(
            model=self.model,
            input=prompt
        )

        return response.output_text