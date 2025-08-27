from tools.interfaces import Tool
import subprocess


class WeatherTool(Tool):
    @property
    def name(self) -> str:
        return "get_weather_tool"

    @property
    def description(self) -> str:
        return "gets the current weather"

    def get_weather_location(self, location: str) -> str:
        try:
            command = ["curl", f"wttr.in/{location}"]

            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout
        except FileNotFoundError:
            return "Error: The 'curl' command was not found. Please ensure it is installed and in your PATH."
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {e}\n{e.stderr}"
