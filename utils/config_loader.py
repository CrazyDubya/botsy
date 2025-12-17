import configparser
import os
from typing import Any, List

class ConfigManager:
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        self._config = configparser.ConfigParser()
        # Look for config.ini in root
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.ini')
        if os.path.exists(config_path):
            self._config.read(config_path)
        else:
            # Fallback or error
            pass

    def get(self, section: str, key: str, fallback: Any = None) -> str:
        return self._config.get(section, key, fallback=fallback)

    def get_int(self, section: str, key: str, fallback: int = 0) -> int:
        return self._config.getint(section, key, fallback=fallback)

    def get_boolean(self, section: str, key: str, fallback: bool = False) -> bool:
        return self._config.getboolean(section, key, fallback=fallback)

    def get_list(self, section: str, key: str, fallback: List = None) -> List[str]:
        val = self._config.get(section, key, fallback=None)
        if val:
            return [x.strip() for x in val.split(',')]
        return fallback or []

# Usage example:
# config = ConfigManager()
# api_key = config.get('API', 'news_api_key')
