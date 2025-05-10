import yaml
from pathlib import Path
from typing import List, Optional


class ConfigError(Exception):
    """Custom exception for configuration errors."""
    pass


class Config:
    """Represents the application configuration loaded from YAML."""
    
    def __init__(self, interval_minutes: int, latency_threshold_ms: int, urls: List[str], telegram_token: Optional[str], telegram_chat_id: Optional[str]):
        self.interval_minutes = interval_minutes
        self.latency_threshold_ms = latency_threshold_ms
        self.urls = urls
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id

    @staticmethod
    def load_from_file(file_path: str = "config.yaml") -> "Config":
        """Load configuration from a YAML file."""
        path = Path(file_path)
        if not path.is_file():
            raise ConfigError(f"Configuration file not found: {file_path}")

        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        try:
            interval_minutes = data["interval_minutes"]
            latency_threshold_ms = data["latency_threshold_ms"]
            urls = data["urls"]
            
            telegram_data = data.get("notifier", {}).get("telegram", {})
            telegram_token = telegram_data.get("token")
            telegram_chat_id = telegram_data.get("chat_id")

            if not isinstance(urls, list) or not all(isinstance(url, str) for url in urls):
                raise ConfigError("URLs must be a list of strings.")

            return Config(
                interval_minutes=interval_minutes,
                latency_threshold_ms=latency_threshold_ms,
                urls=urls,
                telegram_token=telegram_token,
                telegram_chat_id=telegram_chat_id,
            )

        except KeyError as e:
            raise ConfigError(f"Missing required configuration key: {e}")

