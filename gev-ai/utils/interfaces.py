from abc import ABC, abstractmethod
from google.genai import types

class SystemInfoInterface(ABC):
    @abstractmethod
    def get_fastfetch_specs(self) -> str | None:
        pass

    @abstractmethod
    def get_neofetch_specs(self) -> str | None:
        pass

class Agent(ABC):
    model: str

    def __init__(self, model: str) -> None:
        self.model = model
    
    @abstractmethod
    def call_agent(self, content: str) -> types.GenerateContentResponse | None:
        pass
