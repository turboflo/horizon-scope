import os
import pytest
from horizon_match.infrastructure.config.config_manager import ConfigManager


@pytest.fixture
def sample_config_file(tmp_path):
    config_content = """
    database:
        host: localhost
        port: 5432
        username: "{DB_USER}"
        password: "{DB_PASSWORD}"
    api:
        url: "https://api.example.com"
        key: "{API_KEY}"
    """
    config_file = tmp_path / "test_config.yml"
    config_file.write_text(config_content)
    return str(config_file)


@pytest.fixture
def env_vars():
    os.environ["DB_USER"] = "testuser"
    os.environ["DB_PASSWORD"] = "testpass"
    os.environ["API_KEY"] = "testapikey"
    yield
    del os.environ["DB_USER"]
    del os.environ["DB_PASSWORD"]
    del os.environ["API_KEY"]


def test_config_loading(sample_config_file, env_vars):
    config = ConfigManager(sample_config_file)

    assert config.get("database", "host") == "localhost"
    assert config.get("database", "port") == 5432
    assert config.get("database", "username") == "testuser"
    assert config.get("database", "password") == "testpass"
    assert config.get("api", "url") == "https://api.example.com"
    assert config.get("api", "key") == "testapikey"


def test_nested_config_access(sample_config_file, env_vars):
    config = ConfigManager(sample_config_file)

    assert config.get("database") == {
        "host": "localhost",
        "port": 5432,
        "username": "testuser",
        "password": "testpass",
    }


def test_default_value(sample_config_file):
    config = ConfigManager(sample_config_file)

    assert config.get("nonexistent", "key", default="default_value") == "default_value"


def test_missing_env_var(sample_config_file):
    config = ConfigManager(sample_config_file)

    assert config.get("database", "username") == "{DB_USER}"
    assert config.get("database", "password") == "{DB_PASSWORD}"


def test_invalid_nested_access(sample_config_file):
    config = ConfigManager(sample_config_file)

    assert config.get("database", "host", "invalid", default="default") == "default"
