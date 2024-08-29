import os
import yaml
from typing import Any, Dict
from dotenv import load_dotenv


class ConfigManager:
    def __init__(self, config_path: str = "config.yml"):
        load_dotenv()

        with open(config_path, "r") as config_file:
            self.config = yaml.safe_load(config_file)

        self._process_config(self.config)

    def _process_config(self, config: Dict[str, Any]):
        for key, value in config.items():
            if isinstance(value, dict):
                self._process_config(value)
            elif (
                isinstance(value, str) and value.startswith("{") and value.endswith("}")
            ):
                env_var = value.strip("{}")
                config[key] = os.getenv(env_var, value)

    def get(self, *keys: str, default: Any = None) -> Any:
        result = self.config
        for key in keys:
            if isinstance(result, dict):
                result = result.get(key, default)
            else:
                return default
        return result
