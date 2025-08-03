from utils.interfaces import Agent
from prompts.gemini_system_prompt import system_prompt

from google.genai import types
from google import genai

class GeminiAgent(Agent):
    client: genai.Client

    def __init__(self, model: str, api_key: str) -> None:
        super().__init__(model=model)
        self.client = genai.Client(api_key=api_key)

    def call_agent(self, content: str) -> types.GenerateContentResponse | None:
        response = self.client.models.generate_content(
            model = self.model,
            contents=content,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
            ),
        )
        return response
