from tools.agent_tools.interfaces import Tool


class CatFile(Tool):
    @property
    def name(self) -> str:
        return "cat_file"

    @property
    def description(self) -> str:
        return "returns the contents of the given file"

    def cat_file(self, file: str) -> str:
        with open(file, "r") as f:
            return f.read()
