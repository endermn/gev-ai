import os
import configparser
from utils.history_parser import HistoryParser


class Config():
    config_file: str
    config_dir: str

    def __init__(self) -> None:
        if os.name == 'nt':
            self.config_dir = os.path.join(os.environ['APPDATA'], 'gevai')
        else:
            self.config_dir = os.path.join(os.path.expanduser('~'), '.config', 'gevai')
        self.config_file = os.path.join(self.config_dir, 'config.ini')

    def read_config(self) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        config.read(self.config_file)
        return config
    
    def write_config(self, config) -> None:
        os.makedirs(self.config_dir, exist_ok=True)
        with open(self.config_file, 'w') as file:
            config.write(file)

    def change_config(self, history_parser: HistoryParser, setting: str) -> None:
        default_value = history_parser._get_default_history_path()

        if '=' in setting:
            key, value = setting.split('=', 1)
            
            config_obj = self.read_config()
            if 'settings' not in config_obj:
                config_obj['settings'] = {}
            if value == "default":
                config_obj["settings"][key] = default_value
            else:
                config_obj['settings'][key] = value
            self.write_config(config_obj)
            print(f"Configuration updated: {key} = {value}")
        else:
            key = setting
            config_obj = self.read_config()
            value = config_obj.get('settings', key, fallback=None)

            if value is not None:
                print(f"{key} = {value} (set explicitly)")
            else:
                # If not explicitly set, find and show the default
                if key == 'history':
                    print(f"{key} = {default_value} (default)")
                else:
                    print(f"{key} = Not set (no default)")
