import pytest
from unittest.mock import Mock, patch
import json
from horizon_scope.infrastructure.services.openai_comparison_service import (
    OpenAIComparisonService,
    MAX_PROJECT_LENGTH,
)
from horizon_scope.domain.entities.comparison import Comparison
from horizon_scope.infrastructure.config.config_manager import ConfigManager


@pytest.fixture
def mock_config():
    config = Mock(spec=ConfigManager)
    config.get.side_effect = lambda *args: {
        ("horizon-scope", "comparison-service", "api_key"): "test_openai_api_key",
        ("horizon-scope", "comparison-service", "model"): "gpt-4",
    }[args]
    return config


@pytest.fixture
def mock_openai_client():
    return Mock()


@pytest.fixture
def comparison_service(mock_config, mock_openai_client):
    with patch(
        "horizon_scope.infrastructure.services.openai_comparison_service.OpenAI"
    ) as mock_openai:
        mock_openai.return_value = mock_openai_client
        return OpenAIComparisonService(mock_config)


def test_initialization(mock_config):
    with patch(
        "horizon_scope.infrastructure.services.openai_comparison_service.OpenAI"
    ) as mock_openai:
        service = OpenAIComparisonService(mock_config)

    mock_config.get.assert_any_call("horizon-scope", "comparison-service", "api_key")
    mock_config.get.assert_any_call("horizon-scope", "comparison-service", "model")
    mock_openai.assert_called_once_with(api_key="test_openai_api_key")
    assert service.model == "gpt-4"


def test_create_comparison_prompt(comparison_service):
    my_project = "My project description"
    existing_project = "Existing project description"

    prompt = comparison_service._create_comparison_prompt(my_project, existing_project)

    assert isinstance(prompt, list)
    assert len(prompt) == 2
    assert prompt[0]["role"] == "system"
    assert "academic research assistant" in prompt[0]["content"]
    assert prompt[1]["role"] == "user"
    assert my_project in prompt[1]["content"]
    assert existing_project in prompt[1]["content"]


def test_compare(comparison_service, mock_openai_client):
    my_project = "My project description"
    existing_project = "Existing project description"

    mock_comparison = Comparison(
        summary="Test summary",
        similarity="Test similarity",
        difference="Test difference",
        score=0.75,
        confidence=0.9,
        reason="Test reason",
    )

    mock_response = Mock()
    mock_response.choices = [
        Mock(message=Mock(content=json.dumps(mock_comparison.model_dump())))
    ]
    mock_openai_client.chat.completions.create.return_value = mock_response

    result = comparison_service.compare(my_project, existing_project)

    assert isinstance(result, Comparison)
    assert result == mock_comparison
    mock_openai_client.chat.completions.create.assert_called_once_with(
        model="gpt-4",
        messages=comparison_service._create_comparison_prompt(
            my_project, existing_project
        ),
        response_format={"type": "json_object"},
    )


def test_compare_error_handling(comparison_service, mock_openai_client):
    my_project = "My project description"
    existing_project = "Existing project description"

    mock_openai_client.chat.completions.create.side_effect = Exception("API Error")

    with pytest.raises(Exception, match="API Error"):
        comparison_service.compare(my_project, existing_project)


def test_compare_with_empty_input(comparison_service):
    with pytest.raises(ValueError, match="My project description cannot be empty"):
        comparison_service.compare("", "Existing project")

    with pytest.raises(
        ValueError, match="Existing project description cannot be empty"
    ):
        comparison_service.compare("My project", "")


def test_compare_with_long_input(comparison_service):
    long_project = "a" * (MAX_PROJECT_LENGTH + 1)

    with pytest.raises(
        ValueError,
        match=f"My project description exceeds maximum length of {MAX_PROJECT_LENGTH} characters",
    ):
        comparison_service.compare(long_project, "Existing project")

    with pytest.raises(
        ValueError,
        match=f"Existing project description exceeds maximum length of {MAX_PROJECT_LENGTH} characters",
    ):
        comparison_service.compare("My project", long_project)
