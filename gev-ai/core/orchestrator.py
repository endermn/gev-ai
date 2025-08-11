import shutil
import os
import sys
from services.system_info import SystemInfo
from utils.interfaces import SystemInfoInterface
from settings.config import Config
from utils.history_parser import HistoryParser

from utils.interfaces import Agent
from services.genai_service import GeminiAgent

from google.genai import types

class Orchestrator():
    """Orchestrates the workflow of the GevAI"""

    config: Config

    system_specs: str | None
    terminal_history: str

    agent: Agent | None

    def __init__(self, config: Config, agent_model: str) -> None:
        """Initializes the orchestrator and it's main components"""
        self.config = config

        system_info: SystemInfoInterface = SystemInfo()
        self.system_specs = self.get_system_specs(system_info=system_info)

        history_parser: HistoryParser = HistoryParser()
        self.terminal_history = history_parser.get_terminal_history(self.config)

        self.agent = self.define_agent(agent_model=agent_model)

    def get_system_specs(self, system_info: SystemInfo) -> str | None:
        if shutil.which("fastfetch"):
            return system_info.get_fastfetch_specs() 
        elif shutil.which("neofetch"):
            return system_info.get_neofetch_specs()
        else:
            return None
        
    def define_agent(self, agent_model: str) -> Agent | None:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            print("Error: GENAI_API_KEY environment variable not set.")
            sys.exit(1)

        if "gemini" in agent_model:
            return GeminiAgent(model=agent_model, api_key=api_key)

    def define_prompt(self, prompt: str) -> str:
        full_prompt: str = f"""
        Here are my system specs: {self.system_specs}
        Terminal history: {self.terminal_history}
        Question: {prompt}
        """

        return full_prompt

    def call_agent(self, prompt: str) -> types.GenerateContentResponse | None:
        if self.agent != None:
            return self.agent.call_agent(self.define_prompt(prompt)) 
        return None

