import shutil
import sys
from typing import Callable

from settings.settings import settings

from services.system_info import SystemInfo
from utils.interfaces import SystemInfoInterface
from settings.config import Config
from utils.history_parser import HistoryParser

from core.interfaces import Agent
from services.genai_service import GeminiAgent

from tools.interfaces import Tool

from tools.read_files import CatFile
from tools.weather_tool import WeatherTool
from tools.system_health import SystemHealthTool


from google.genai import types


class Orchestrator:
    """Orchestrates the workflow of the GevAI"""

    config: Config

    system_specs: str | None
    files_in_pwd: str | None
    terminal_history: str

    agent: Agent | None

    def __init__(self, config: Config, agent_model: str) -> None:
        """Initializes the orchestrator and it's main components"""
        self.config = config

        system_info: SystemInfoInterface = SystemInfo()
        self.files_in_pwd = system_info.get_pwd_files()
        self.system_specs = self.get_system_specs(system_info=system_info)

        history_parser: HistoryParser = HistoryParser()
        self.terminal_history = history_parser.get_terminal_history(self.config)

        tools: list[Callable] = self.get_tools()

        self.agent = self.define_agent(agent_model=agent_model, tools=tools)

    def get_tools(self) -> list[Callable]:
        weather_tool: Tool = WeatherTool()
        health_tool: Tool = SystemHealthTool()
        cat_tool: Tool = CatFile()
        # grounding_tool: types.Tool = types.Tool(
        #     google_search=types.GoogleSearch()
        # )
        tools = [
            weather_tool.get_weather_location,
            health_tool.get_system_health,
            cat_tool.cat_file,
        ]
        return tools

    def define_agent(self, agent_model: str, tools: list[Callable]) -> Agent | None:
        api_key = settings.google_api_key
        if not api_key:
            print("Error: GENAI_API_KEY environment variable not set.")
            sys.exit(1)

        if "gemini" in agent_model:
            return GeminiAgent(model=agent_model, api_key=api_key, tools=tools)

    def get_system_specs(self, system_info: SystemInfo) -> str | None:
        if shutil.which("fastfetch"):
            return system_info.get_fastfetch_specs()
        elif shutil.which("neofetch"):
            return system_info.get_neofetch_specs()
        else:
            return None

    def define_prompt(self, prompt: str) -> str:
        full_prompt: str = f"""
        ** System specs **
        {self.system_specs}

        ** Files in pwd **
        {self.files_in_pwd}

        ** Terminal history**
        {self.terminal_history}

        ** Question **
        {prompt}
        """

        return full_prompt

    def call_agent(self, prompt: str) -> types.GenerateContentResponse | None:
        if self.agent != None:
            return self.agent.call_agent(self.define_prompt(prompt))
        return None
