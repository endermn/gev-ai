from tools.interfaces import Tool
import subprocess

class CatFile(Tool):
    @property
    def name(self) -> str:
        return "cat_file"
    @property
    def description(self) -> str:
        return "returns the contents of the given file"

    def cat_file(self, file: str) -> str:
        try:
            return subprocess.check_output(["cat", file], text=True)
        except Exception as e:
            return f"Error running cat: {e}"

