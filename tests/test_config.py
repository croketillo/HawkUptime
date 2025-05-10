import pytest
import tempfile
import yaml
from uptime_monitor.config import Config, ConfigError


def test_load_valid_config():
    """Test that a valid YAML config is loaded correctly."""
    config_data = {
        "interval_minutes": 5,
        "latency_threshold_ms": 500,
        "urls": ["https://example.com"],
        "notifier": {
            "telegram": {
                "token": "dummy-token",
                "chat_id": "123456"
            }
        },
        "log_retention_days": 30
    }

    with tempfile.NamedTemporaryFile("w+", suffix=".yaml") as tmp:
        yaml.dump(config_data, tmp)
        tmp.flush()
        config = Config.load_from_file(tmp.name)

        assert config.interval_minutes == 5
        assert config.latency_threshold_ms == 500
        assert config.urls == ["https://example.com"]
        assert config.telegram_token == "dummy-token"
        assert config.telegram_chat_id == "123456"
        assert config.__dict__.get("log_retention_days", 30) == 30


def test_load_invalid_config_missing_keys():
    """Test that missing required keys raise ConfigError."""
    config_data = {"urls": ["https://example.com"]}
    
    with tempfile.NamedTemporaryFile("w+", suffix=".yaml") as tmp:
        yaml.dump(config_data, tmp)
        tmp.flush()
        with pytest.raises(ConfigError):
            Config.load_from_file(tmp.name)
