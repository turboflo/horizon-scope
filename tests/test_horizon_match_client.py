import pytest
from unittest.mock import Mock, patch
from horizon_scope.presentation.horizon_scope_client import HorizonScopeClient
from horizon_scope.domain.entities.project import Project
from horizon_scope.domain.entities.comparison import Comparison
from horizon_scope.domain.entities.horizon_scope_result import HorizonScopeResult
from horizon_scope.infrastructure.config.config_manager import ConfigManager
from horizon_scope.infrastructure.services.pinecone_search_service import (
    PineconeSearchService,
)
from horizon_scope.infrastructure.services.openai_comparison_service import (
    OpenAIComparisonService,
)
from horizon_scope.application.use_cases.compare_projects import CompareProjects


@pytest.fixture
def mock_config_manager():
    return Mock(spec=ConfigManager)


@pytest.fixture
def mock_vector_search_service():
    return Mock(spec=PineconeSearchService)


@pytest.fixture
def mock_comparison_service():
    return Mock(spec=OpenAIComparisonService)


@pytest.fixture
def mock_compare_projects():
    return Mock(spec=CompareProjects)


@pytest.fixture
def horizon_scope_client(
    mock_config_manager,
    mock_vector_search_service,
    mock_comparison_service,
    mock_compare_projects,
):
    with patch(
        "horizon_scope.presentation.horizon_scope_client.PineconeSearchService",
        return_value=mock_vector_search_service,
    ), patch(
        "horizon_scope.presentation.horizon_scope_client.OpenAIComparisonService",
        return_value=mock_comparison_service,
    ), patch(
        "horizon_scope.presentation.horizon_scope_client.CompareProjects",
        return_value=mock_compare_projects,
    ):
        return HorizonScopeClient(mock_config_manager)


def test_initialization(mock_config_manager):
    with patch(
        "horizon_scope.presentation.horizon_scope_client.PineconeSearchService"
    ) as mock_pinecone, patch(
        "horizon_scope.presentation.horizon_scope_client.OpenAIComparisonService"
    ) as mock_openai, patch(
        "horizon_scope.presentation.horizon_scope_client.CompareProjects"
    ) as mock_compare_projects:

        client = HorizonScopeClient(mock_config_manager)

        mock_pinecone.assert_called_once_with(mock_config_manager)
        mock_openai.assert_called_once_with(mock_config_manager)
        mock_compare_projects.assert_called_once()


def test_from_config():
    with patch(
        "horizon_scope.presentation.horizon_scope_client.ConfigManager"
    ) as mock_config_manager, patch(
        "horizon_scope.presentation.horizon_scope_client.HorizonScopeClient.__init__",
        return_value=None,
    ) as mock_init:

        HorizonScopeClient.from_config("test_config.yml")

        mock_config_manager.assert_called_once_with("test_config.yml")
        mock_init.assert_called_once()


def test_match(horizon_scope_client, mock_compare_projects):
    query = "test query"
    k = 5
    mock_results = [Mock(spec=HorizonScopeResult) for _ in range(k)]
    mock_compare_projects.execute.return_value = mock_results

    results = horizon_scope_client.match(query, k)

    mock_compare_projects.execute.assert_called_once_with(query, k)
    assert results == mock_results


def test_index_project(horizon_scope_client, mock_vector_search_service):
    project = Mock(spec=Project)

    horizon_scope_client.index_project(project)

    mock_vector_search_service.index_project.assert_called_once_with(project)


def test_search_projects(horizon_scope_client, mock_vector_search_service):
    query = "test query"
    k = 5
    mock_projects = [Mock(spec=Project) for _ in range(k)]
    mock_vector_search_service.search.return_value = mock_projects

    results = horizon_scope_client.search_projects(query, k)

    mock_vector_search_service.search.assert_called_once_with(query, k)
    assert results == mock_projects


def test_get_config(horizon_scope_client, mock_config_manager):
    keys = ["test", "key"]
    default_value = "default"
    expected_value = "config_value"
    mock_config_manager.get.return_value = expected_value

    result = horizon_scope_client.get_config(*keys, default=default_value)

    mock_config_manager.get.assert_called_once_with(*keys, default=default_value)
    assert result == expected_value


def test_integration(mock_config_manager):
    with patch(
        "horizon_scope.presentation.horizon_scope_client.PineconeSearchService"
    ) as mock_pinecone, patch(
        "horizon_scope.presentation.horizon_scope_client.OpenAIComparisonService"
    ) as mock_openai, patch(
        "horizon_scope.presentation.horizon_scope_client.CompareProjects"
    ) as mock_compare_projects:

        client = HorizonScopeClient(mock_config_manager)

        # Test match
        query = "test query"
        k = 3
        mock_results = [Mock(spec=HorizonScopeResult) for _ in range(k)]
        mock_compare_projects.return_value.execute.return_value = mock_results

        results = client.match(query, k)
        assert results == mock_results

        # Test index_project
        project = Mock(spec=Project)
        client.index_project(project)
        mock_pinecone.return_value.index_project.assert_called_once_with(project)

        # Test search_projects
        mock_projects = [Mock(spec=Project) for _ in range(k)]
        mock_pinecone.return_value.search.return_value = mock_projects

        search_results = client.search_projects(query, k)
        assert search_results == mock_projects

        # Test get_config
        client.get_config("test", "key")
        mock_config_manager.get.assert_called_once_with("test", "key", default=None)
