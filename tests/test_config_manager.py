import pytest
import yaml
from horizon_scope.infrastructure.config.config_manager import ConfigManager


@pytest.fixture
def temp_config_file(tmp_path):
    config_data = {
        "database": {
            "host": "localhost",
            "port": 5432,
            "username": "{DB_USERNAME}",
            "password": "{DB_PASSWORD}",
        },
        "api": {"key": "{API_KEY}", "url": "https://api.example.com"},
        "debug": True,
    }
    config_file = tmp_path / "test_config.yml"
    with open(config_file, "w") as f:
        yaml.dump(config_data, f)
    return config_file


@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("DB_USERNAME", "testuser")
    monkeypatch.setenv("DB_PASSWORD", "testpass")
    monkeypatch.setenv("API_KEY", "testapikey")


def test_config_manager_initialization(temp_config_file, mock_env_vars):
    config_manager = ConfigManager(config_path=str(temp_config_file))
    assert isinstance(config_manager.config, dict)
    assert config_manager.config["database"]["username"] == "testuser"
    assert config_manager.config["database"]["password"] == "testpass"
    assert config_manager.config["api"]["key"] == "testapikey"


def test_config_manager_get_method(temp_config_file, mock_env_vars):
    config_manager = ConfigManager(config_path=str(temp_config_file))
    assert config_manager.get("database", "host") == "localhost"
    assert config_manager.get("database", "username") == "testuser"
    assert config_manager.get("api", "key") == "testapikey"
    assert config_manager.get("api", "url") == "https://api.example.com"
    assert config_manager.get("debug") == True


def test_config_manager_get_method_with_default(temp_config_file, mock_env_vars):
    config_manager = ConfigManager(config_path=str(temp_config_file))
    assert config_manager.get("nonexistent", default="default_value") == "default_value"
    assert config_manager.get("database", "nonexistent", default=5000) == 5000


def test_config_manager_get_method_nested_keys(temp_config_file, mock_env_vars):
    config_manager = ConfigManager(config_path=str(temp_config_file))
    assert config_manager.get("database", "username") == "testuser"
    assert config_manager.get("database", "host") == "localhost"


def test_config_manager_with_missing_env_vars(temp_config_file, monkeypatch):
    monkeypatch.delenv("DB_USERNAME", raising=False)
    monkeypatch.delenv("DB_PASSWORD", raising=False)
    monkeypatch.delenv("API_KEY", raising=False)

    config_manager = ConfigManager(config_path=str(temp_config_file))
    assert config_manager.get("database", "username") == None
    assert config_manager.get("database", "password") == None
    assert config_manager.get("api", "key") == None


def test_config_manager_with_partial_env_vars(temp_config_file, monkeypatch):
    monkeypatch.setenv("DB_USERNAME", "testuser")
    monkeypatch.delenv("DB_PASSWORD", raising=False)
    monkeypatch.delenv("API_KEY", raising=False)

    config_manager = ConfigManager(config_path=str(temp_config_file))
    assert config_manager.get("database", "username") == "testuser"
    assert config_manager.get("database", "password") == None
    assert config_manager.get("api", "key") == None


def test_config_manager_with_nonexistent_config_file():
    with pytest.raises(FileNotFoundError):
        ConfigManager(config_path="nonexistent_config.yml")


def test_config_manager_with_invalid_yaml_file(tmp_path):
    invalid_config_file = tmp_path / "invalid_config.yml"
    with open(invalid_config_file, "w") as f:
        f.write("invalid: yaml: content")

    with pytest.raises(yaml.YAMLError):
        ConfigManager(config_path=str(invalid_config_file))
