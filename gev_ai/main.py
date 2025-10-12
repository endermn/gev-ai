import sys
import logging

from settings.config import Config
from tools.common_tools.history_parser import TerminalHistoryParser
from core.orchestrator import Orchestrator
from services.logger import GevaiLogger

config: Config = Config()
history_parser: TerminalHistoryParser = TerminalHistoryParser()

logger: logging.Logger = GevaiLogger(name=__name__, file="gevai.log").get_logger()

def main(args: list[str]) -> None:
	if len(args) < 2:
		print("Please provide a query. Use 'gevai help' for more information.")
		sys.exit(1)
	if args[1] == "config" and len(args) >= 3 and "history" in args[2]:
		config.change_config(setting=args[2:][0], history_parser=history_parser)
		return
	elif args[1] == "config" and len(args) == 2:
		print(
			"To set path to terminal history use gevai config history='path_to_history_file'"
		)
		return
	elif args[1] == "help":
		print("Usage: gevai <your query>")
		print("To set path to terminal history use gevai config history='path_to_history_file' (set history='default' to reset to default path)")
		print("If it's your first time using gevai, please run the installation script first.")
		return

	user_prompt: str = " ".join(args[1:])
	orchestrator: Orchestrator = Orchestrator(config=config)

	orchestrator.start_workflow(user_prompt=user_prompt)


if __name__ == "__main__":
	main(sys.argv)
