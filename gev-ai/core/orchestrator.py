import shutil
import sys

from settings.settings import settings

from services.system_info import SystemInfo
from tools.common_tools.interfaces import SystemInfoInterface
from settings.config import Config
from tools.common_tools.history_parser import TerminalHistoryParser

from agents.interfaces import Agent
from agents.main_agent import BaseAgent
from agents.google_search_agent import GoogleSearchAgent

from tools.agent_tools.interfaces import Tool

from tools.agent_tools.read_files import CatFile
from tools.agent_tools.weather_tool import WeatherTool
from tools.agent_tools.system_health import SystemHealthTool


from google.genai import types


class Orchestrator:
    """Orchestrates the workflow of the GevAI"""

    config: Config

    system_specs: str | None
    files_in_pwd: str | None
    terminal_history: str

    main_agent: Agent | None
    search_agent: Agent | None

    def __init__(self, config: Config) -> None:
        """Initializes the orchestrator and it's main components"""
        self.config = config

        system_info: SystemInfoInterface = SystemInfo()
        self.files_in_pwd = system_info.get_pwd_files()
        self.system_specs = self.get_system_specs(system_info=system_info)

        history_parser: TerminalHistoryParser = TerminalHistoryParser()
        self.terminal_history = history_parser.get_terminal_history(self.config)

        api_key = settings.google_api_key
        if not api_key:
            print("Error: GENAI_API_KEY environment variable not set.")
            sys.exit(1)

        weather_tool: Tool = WeatherTool()
        health_tool: Tool = SystemHealthTool()
        cat_tool: Tool = CatFile()
        main_tools = [
            weather_tool.get_weather_location,
            health_tool.get_system_health,
            cat_tool.cat_file,
        ]

        self.main_agent = BaseAgent(
            model="gemini-2.5-flash-lite", api_key=api_key, tools=main_tools
        )

        self.search_agent = GoogleSearchAgent(
            model="gemini-2.5-flash-lite", api_key=api_key
        )

    def start_workflow(self, user_prompt: str) -> None:
        response = self.call_agent(agent=self.main_agent, prompt=user_prompt)
        if response == None:
            return
        match response.text:
            case "google_search_agent":
                print("IN GOOGLE SEARCH AGENT ==============================")
                search_results = self.call_agent(
                    agent=self.search_agent, prompt=user_prompt
                )
                if search_results != None:
                    print(search_results.text)
            case _:
                print(response.text)

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

    def call_agent(
        self, agent: Agent | None, prompt: str
    ) -> types.GenerateContentResponse | None:
        if agent != None:
            return agent.call_agent(self.define_prompt(prompt))
        return None
