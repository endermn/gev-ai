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

from tools.agent_tools.todo import ToDoTool
from tools.agent_tools.read_files import CatFile
from tools.agent_tools.weather_tool import WeatherTool
from tools.agent_tools.system_health import SystemHealthTool

from google.genai import types, errors

from typing import Optional
import logging

from services.logger import GevaiLogger

logger: logging.Logger = GevaiLogger(name=__name__, file="gevai.log").get_logger()


class Orchestrator:
    """Orchestrates the workflow of the GevAI"""

    config: Config

    system_specs: Optional[str]
    files_in_pwd: Optional[str]
    terminal_history: str

    main_agent: Optional[Agent]
    search_agent: Optional[Agent]

    def __init__(self, config: Config) -> None:
        """Initializes the orchestrator and its main components"""
        self.config = config

        system_info: SystemInfoInterface = SystemInfo()
        self.files_in_pwd = system_info.get_pwd_files()
        self.system_specs = system_info.get_system_specs()

        history_parser: TerminalHistoryParser = TerminalHistoryParser()
        self.terminal_history = history_parser.get_terminal_history(self.config)

        api_key = settings.google_api_key
        if not api_key:
            print("Error: GENAI_API_KEY environment variable not set.")
            logger.error("GENAI_API_KEY environment variable not set")
            sys.exit(1)

        weather_tool: Tool = WeatherTool()
        health_tool: Tool = SystemHealthTool()
        cat_tool: Tool = CatFile()
        todo_tool: Tool = ToDoTool()

        main_tools = [
            weather_tool.get_weather_location,
            health_tool.get_system_health,
            cat_tool.cat_file,
            todo_tool.add_task,
            todo_tool.view_tasks,
            todo_tool.remove_task,
        ]

        self.main_agent = BaseAgent(
            model="gemini-2.5-flash-lite", api_key=api_key, tools=main_tools
        )

        self.search_agent = GoogleSearchAgent(
            model="gemini-2.5-flash-lite", api_key=api_key
        )

    def start_workflow(self, user_prompt: str) -> None:
        logger.info("Starting workflow")
        logger.info(f"User prompt: {user_prompt}")

        response = self.call_agent(agent=self.main_agent, prompt=user_prompt)
        if response is None:
            return

        if response.text and "google_search_agent" in response.text:
            search_results: Optional[types.GenerateContentResponse] = self.call_agent(
                agent=self.search_agent, prompt=user_prompt
            )
            if search_results is not None:
                print(search_results.text)
                logger.info(search_results)
                logger.info(search_results.text)

        else:
            print(response.text)
            logger.info(response)
            logger.info(response.text)

    def define_prompt(self, prompt: str) -> str:
        logger.info("Defining prompt")

        full_prompt: str = f"""
        ** System specs **
        {self.system_specs}

        ** Files in pwd **
        {self.files_in_pwd}

        ** Terminal history **
        {self.terminal_history}

        ** Question **
        {prompt}
        """

        return full_prompt

    def call_agent(
        self, agent: Optional[Agent], prompt: str
    ) -> Optional[types.GenerateContentResponse]:
        try:
            if agent is not None:
                return agent.call_agent(self.define_prompt(prompt))
        except errors.ServerError as e:
            print(f"A server error occurred: {e.message}")
            logger.error(f"Server error: {e.message}")
        except errors.APIError as e:
            print(f"An API error occurred: {e.message}")
            logger.error(f"API error: {e.message}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            logger.error(f"Unexpected error: {str(e)}")
            return None
