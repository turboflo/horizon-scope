import os
import yaml
from typing import Any, Dict
from dotenv import load_dotenv


class ConfigManager:
    """Manages configuration settings loaded from a YAML file and environment variables.

    This class reads configuration settings from a YAML file and allows access to those settings.
    It also supports interpolation of environment variables in the configuration values.

    Attributes:
        config (Dict[str, Any]): The configuration settings loaded from the YAML file.
    """

    def __init__(self, config_path: str = "config.yml") -> None:
        """Initialize ConfigManager with configuration settings.

        Args:
            config_path (str): Path to the YAML configuration file. Defaults to "config.yml".
        """
        load_dotenv()

        with open(config_path, "r") as config_file:
            self.config = yaml.safe_load(config_file)

        self._process_config(self.config)

    def _process_config(self, config: Dict[str, Any]) -> None:
        """Process the configuration dictionary to substitute environment variables.

        Args:
            config (Dict[str, Any]): The configuration dictionary to process.
        """
        for key, value in config.items():
            if isinstance(value, dict):
                self._process_config(value)
            elif (
                isinstance(value, str) and value.startswith("{") and value.endswith("}")
            ):
                env_var = value.strip("{}")
                config[key] = (
                    os.getenv(env_var) if os.getenv(env_var) is not None else None
                )

    def get(self, *keys: str, default: Any = None) -> Any:
        """Retrieve a configuration value based on a sequence of keys.

        Args:
            *keys (str): The sequence of keys to access nested values in the configuration.
            default (Any): The default value to return if the key path is not found. Defaults to None.

        Returns:
            Any: The configuration value associated with the provided keys, or the default value if not found.
        """
        result = self.config
        for key in keys:
            if isinstance(result, dict):
                result = result.get(key, default)
            else:
                return default
        return result

    def is_openai_api_key_set(self) -> bool:
        """Überprüft, ob der OpenAI API-Schlüssel gesetzt ist.

        Returns:
            bool: True, wenn der API-Schlüssel gesetzt ist, sonst False.
        """
        comparison_key = self.get("horizon-scope", "comparison-service", "api_key")
        # embedding_key = self.get(
        #     "horizon-scope", "vector-search-service", "embeddings", "api_key"
        # )
        return bool(comparison_key)
