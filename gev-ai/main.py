import sys
from dotenv import load_dotenv

from settings.config import Config
from utils.history_parser import HistoryParser
from core.orchestrator import Orchestrator

config: Config = Config()
history_parser: HistoryParser = HistoryParser()

def main(args: list[str]) -> None:
    # pesho

    load_dotenv()

    if len(args) < 2:
        print("Usage: gevai <your query>")
        sys.exit(1)
    if args[1] == "config" and len(args) >= 3:
        config.change_config(setting=args[2:][0], history_parser=history_parser) 
        return
    elif args[1] == "config" and len(args) == 2:
        print("To set path to terminal history use gevai config history='path_to_history_file'")
        return
        
    orchestrator: Orchestrator = Orchestrator(config=config, agent_model="gemini-2.5-flash-lite")

    user_prompt: str = " ".join(args[1:])
    response = orchestrator.call_agent(user_prompt)
    if response != None:
        print(response.text)

if __name__ == "__main__":
    main(sys.argv)
