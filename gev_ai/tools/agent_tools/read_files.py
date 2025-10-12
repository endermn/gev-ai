from .interfaces import Tool
from tools.tool_utils import tools


class CatFile(Tool):
    @property
    def name(self) -> str:
        return "cat_file"

    @property
    def description(self) -> str:
        return "returns the contents of the given file"

    @tools
    def cat_file(self, file: str) -> str:
        with open(file, "r") as f:
            return f.read()
