import subprocess
import re
from utils.interfaces import SystemInfoInterface


class SystemInfo(SystemInfoInterface):
    def get_fastfetch_specs(self) -> str:
        try:
            output = subprocess.check_output(["fastfetch"], text=True)
            clean_output = re.sub(r"\x1B\[[0-?]*[ -/]*[@-~]", "", output)
        except Exception as e:
            print(f"Error running fastfetch: {e}")
            clean_output = "fastfetch could not be run."
        return clean_output

    def get_neofetch_specs(self) -> str:
        try:
            output = subprocess.check_output(["neofetch", "--stdout"], text=True)
            clean_output = re.sub(r"\x1B\[[0-?]*[ -/]*[@-~]", "", output)
        except FileNotFoundError:
            clean_output = "neofetch is not installed or not in the system's PATH."
        except Exception as e:
            print(f"Error running neofetch: {e}")
            clean_output = "neofetch could not be run."
        return clean_output
