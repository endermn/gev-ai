import subprocess
import re
from utils.interfaces import SystemInfoInterface


class SystemInfo(SystemInfoInterface):
    def get_fastfetch_specs(self) -> str | None:
        try:
            output = subprocess.check_output(["fastfetch"], text=True)
            clean_output = re.sub(r"\x1B\[[0-?]*[ -/]*[@-~]", "", output)
        except Exception as e:
            print(f"Error running fastfetch: {e}")
            clean_output = None
        return clean_output

    def get_neofetch_specs(self) -> str | None:
        try:
            output = subprocess.check_output(["neofetch", "--stdout"], text=True)
            clean_output = re.sub(r"\x1B\[[0-?]*[ -/]*[@-~]", "", output)
        except Exception as e:
            print(f"Error running neofetch: {e}")
            clean_output = None
        return clean_output

    def get_pwd_files(self) -> str | None:
        try:
            output = subprocess.check_output(["ls", "-R"], text=True)
        except Exception as e:
            print(f"Error running neofetch: {e}")
            output = None
        return output
