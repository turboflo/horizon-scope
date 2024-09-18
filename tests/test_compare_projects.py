import pytest
from unittest.mock import Mock, MagicMock
from typing import List

from horizon_scope.application.interfaces.vector_search_service import (
    VectorSearchService,
)
from horizon_scope.application.interfaces.comparison_service import ComparisonService
from horizon_scope.domain.entities.horizon_scope_result import HorizonScopeResult
from horizon_scope.application.use_cases.compare_projects import CompareProjects
from horizon_scope.domain.entities.comparison import Comparison
from horizon_scope.domain.entities.project import Project


class MockProject(Project):
    def __init__(self, id: str, description: str):
        super().__init__(id=id, description=description)


class MockComparison(Comparison):
    def __init__(self, score: float):
        super().__init__(
            score=score,
            summary="Mock summary",
            similarity="Mock similarity",
            difference="Mock difference",
            confidence=0.8,
            reason="Mock reason",
        )


@pytest.fixture
def vector_search_service_mock():
    return Mock(spec=VectorSearchService)


@pytest.fixture
def comparison_service_mock():
    return Mock(spec=ComparisonService)


@pytest.fixture
def compare_projects(vector_search_service_mock, comparison_service_mock):
    return CompareProjects(vector_search_service_mock, comparison_service_mock)


def test_execute_returns_correct_number_of_results(
    compare_projects, vector_search_service_mock, comparison_service_mock
):
    # Arrange
    query = "test query"
    k = 3
    mock_projects = [MockProject(str(i), f"Project {i}") for i in range(k)]
    vector_search_service_mock.search.return_value = mock_projects
    comparison_service_mock.compare.return_value = MockComparison(0.5)

    # Act
    results = compare_projects.execute(query, k)

    # Assert
    assert len(results) == k
    vector_search_service_mock.search.assert_called_once_with(query, k)
    assert comparison_service_mock.compare.call_count == k


def test_execute_sorts_results_by_score(
    compare_projects, vector_search_service_mock, comparison_service_mock
):
    # Arrange
    query = "test query"
    k = 3
    mock_projects = [MockProject(str(i), f"Project {i}") for i in range(k)]
    vector_search_service_mock.search.return_value = mock_projects
    comparison_service_mock.compare.side_effect = [
        MockComparison(0.3),
        MockComparison(0.7),
        MockComparison(0.5),
    ]

    # Act
    results = compare_projects.execute(query, k)

    # Assert
    assert results[0].comparison.score == 0.7
    assert results[1].comparison.score == 0.5
    assert results[2].comparison.score == 0.3


def test_execute_returns_horizon_match_results(
    compare_projects, vector_search_service_mock, comparison_service_mock
):
    # Arrange
    query = "test query"
    k = 1
    mock_project = MockProject("1", "Project 1")
    vector_search_service_mock.search.return_value = [mock_project]
    comparison_service_mock.compare.return_value = MockComparison(0.5)

    # Act
    results = compare_projects.execute(query, k)

    # Assert
    assert isinstance(results[0], HorizonScopeResult)
    assert results[0].project == mock_project
    assert results[0].comparison.score == 0.5


def test_execute_handles_empty_search_results(
    compare_projects, vector_search_service_mock
):
    # Arrange
    query = "test query"
    k = 5
    vector_search_service_mock.search.return_value = []

    # Act
    results = compare_projects.execute(query, k)

    # Assert
    assert len(results) == 0


def test_execute_uses_correct_arguments_for_comparison(
    compare_projects, vector_search_service_mock, comparison_service_mock
):
    # Arrange
    query = "test query"
    k = 1
    mock_project = MockProject("1", "Project 1")
    vector_search_service_mock.search.return_value = [mock_project]
    comparison_service_mock.compare.return_value = MockComparison(0.5)

    # Act
    compare_projects.execute(query, k)

    # Assert
    comparison_service_mock.compare.assert_called_once_with(
        query, mock_project.description
    )
