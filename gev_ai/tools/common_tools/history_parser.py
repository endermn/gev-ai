import os
from typing import Optional
from tools.tool_utils import logger
from settings.settings import settings


class TerminalHistoryParser:
    def __init__(self, rag_service=None):
        """
        Initialize the parser with optional RAG service.
        
        Args:
            rag_service: Optional TerminalHistoryRAG service for semantic retrieval
        """
        self.rag_service = rag_service

    @property
    def name(self) -> str:
        return "terminal_history_parser"

    @property
    def description(self) -> str:
        return "parses the terminal history and returns relevant commands using RAG (Retrieval Augmented Generation)"

    def _get_default_history_path(self) -> str:
        shell = settings.shell.lower()

        if "zsh" in shell:
            return "~/.zsh_history"
        elif "fish" in shell:
            return "~/.local/share/fish/fish_history"
        # Defaulting to bash for other Unix-like shells
        elif os.name == "posix":
            return "~/.bash_history"
        elif os.name == "nt":
            return os.path.join(
                settings.app_data,
                "Microsoft\\Windows\\PowerShell\\PSReadLine\\ConsoleHost_history.txt",
            )

    def get_terminal_history(self, config, query: Optional[str] = None) -> str:
        """
        Get terminal history using RAG if available, otherwise fallback to recent commands.
        
        Args:
            config: Configuration object
            query: Optional query for semantic search
            
        Returns:
            Relevant terminal history commands
        """
        logger.info("Tool 'get_terminal_history' called")
        config_parser = config.read_config()

        path = config_parser.get(
            "settings", "history", fallback=self._get_default_history_path()
        )

        history_file = os.path.expanduser(str(path))
        
        # If RAG service is available, use it
        if self.rag_service:
            try:
                # Sync commands from history file if needed
                self.rag_service.sync_from_history_file(history_file)
                
                # Retrieve relevant commands using RAG
                if query:
                    return self.rag_service.retrieve_relevant_commands(query, top_k=10)
                else:
                    # If no query, get recent commands
                    return self._get_recent_commands_fallback(history_file)
            except Exception as e:
                logger.error(f"Error using RAG service: {e}")
                # Fallback to traditional method
                return self._get_recent_commands_fallback(history_file)
        
        # Fallback to traditional method if no RAG service
        return self._get_recent_commands_fallback(history_file)

    def _get_recent_commands_fallback(self, history_file: str) -> str:
        """Fallback method to get recent commands without RAG."""
        try:
            with open(history_file, "r", errors="ignore") as f:
                lines: list[str] = f.readlines()
            hyphen_lines = [line for line in lines if line.strip().startswith("-")]
            return "".join(hyphen_lines[-10:])
        except FileNotFoundError:
            return f"Error: History file not found at '{history_file}'. Please check the path or configure it with 'gevai config history=<path>'."
        except Exception as e:
            return f"An unexpected error occurred: {e}"
