import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from horizon_scope.infrastructure.services.pinecone_search_service import (
    PineconeSearchService,
)
from horizon_scope.domain.entities.project import Project
from horizon_scope.infrastructure.config.config_manager import ConfigManager


@pytest.fixture
def mock_config():
    config = Mock(spec=ConfigManager)
    config.get.side_effect = lambda *args: {
        (
            "horizon-scope",
            "vector-search-service",
            "store",
            "api_key",
        ): "test_pinecone_api_key",
        ("horizon-scope", "vector-search-service", "store", "index"): "test_index",
        (
            "horizon-scope",
            "vector-search-service",
            "embeddings",
            "api_key",
        ): "test_openai_api_key",
        (
            "horizon-scope",
            "vector-search-service",
            "embeddings",
            "model",
        ): "text-embedding-ada-002",
    }[args]
    return config


@pytest.fixture
def mock_pinecone_index():
    return Mock()


@pytest.fixture
def mock_openai_client():
    return Mock()


@pytest.fixture
def pinecone_search_service(mock_config, mock_pinecone_index, mock_openai_client):
    with patch(
        "horizon_scope.infrastructure.services.pinecone_search_service.Pinecone"
    ) as mock_pinecone:
        mock_pinecone.return_value.Index.return_value = mock_pinecone_index
        with patch(
            "horizon_scope.infrastructure.services.pinecone_search_service.OpenAI"
        ) as mock_openai:
            mock_openai.return_value = mock_openai_client
            return PineconeSearchService(mock_config)


def test_search(pinecone_search_service, mock_openai_client, mock_pinecone_index):
    # Arrange
    query = "test query"
    k = 2
    mock_embedding = [0.1, 0.2, 0.3]
    mock_openai_client.embeddings.create.return_value.data = [
        Mock(embedding=mock_embedding)
    ]

    mock_search_results = Mock()
    mock_search_results.matches = [
        Mock(
            id="1",
            metadata={
                "title": "Project 1",
                "objective": "Description 1",
                "contentUpdateDate": "2023-01-01T00:00:00",
            },
            score=0.9,
        ),
        Mock(
            id="2",
            metadata={
                "title": "Project 2",
                "objective": "Description 2",
                "contentUpdateDate": "2023-01-02T00:00:00",
            },
            score=0.8,
        ),
    ]
    mock_pinecone_index.query.return_value = mock_search_results

    # Act
    results = pinecone_search_service.search(query, k)

    # Assert
    assert len(results) == 2
    assert isinstance(results[0], Project)
    assert results[0].id == "1"
    assert results[0].title == "Project 1"
    assert results[0].description == "Description 1"
    assert results[0].content_update_date == "2023-01-01T00:00:00"
    assert results[0].similarity == 0.9

    mock_openai_client.embeddings.create.assert_called_once_with(
        model="text-embedding-ada-002", input=query
    )
    mock_pinecone_index.query.assert_called_once_with(
        vector=mock_embedding, top_k=k, include_metadata=True
    )


def test_index_project(
    pinecone_search_service, mock_openai_client, mock_pinecone_index
):
    # Arrange
    project = Project(
        id="test_id",
        title="Test Project",
        description="Test Description",
        content_update_date="2023-01-01T00:00:00",
        similarity=0.5,
    )
    mock_embedding = [0.1, 0.2, 0.3]
    mock_openai_client.embeddings.create.return_value.data = [
        Mock(embedding=mock_embedding)
    ]

    # Act
    pinecone_search_service.index_project(project)

    # Assert
    mock_openai_client.embeddings.create.assert_called_once_with(
        model="text-embedding-ada-002", input=project.description
    )
    mock_pinecone_index.upsert.assert_called_once_with(
        vectors=[
            {
                "id": project.id,
                "values": mock_embedding,
                "metadata": {
                    "title": project.title,
                    "objective": project.description,
                    "contentUpdateDate": project.content_update_date,
                },
            }
        ]
    )


def test_index_project_without_content_update_date(
    pinecone_search_service, mock_openai_client, mock_pinecone_index
):
    # Arrange
    project = Project(
        id="test_id",
        title="Test Project",
        description="Test Description",
        similarity=0.5,
    )
    mock_embedding = [0.1, 0.2, 0.3]
    mock_openai_client.embeddings.create.return_value.data = [
        Mock(embedding=mock_embedding)
    ]

    # Act
    with patch(
        "horizon_scope.infrastructure.services.pinecone_search_service.datetime"
    ) as mock_datetime:
        mock_now = datetime(2023, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = mock_now
        pinecone_search_service.index_project(project)

    # Assert
    mock_pinecone_index.upsert.assert_called_once()
    called_args = mock_pinecone_index.upsert.call_args[1]["vectors"][0]
    assert called_args["metadata"]["contentUpdateDate"] == "2023-01-01T12:00:00"


def test_initialization(mock_config):
    # Act
    with patch(
        "horizon_scope.infrastructure.services.pinecone_search_service.Pinecone"
    ) as mock_pinecone:
        with patch(
            "horizon_scope.infrastructure.services.pinecone_search_service.OpenAI"
        ) as mock_openai:
            PineconeSearchService(mock_config)

    # Assert
    mock_pinecone.assert_called_once_with(api_key="test_pinecone_api_key")
    mock_pinecone.return_value.Index.assert_called_once_with("test_index")
    mock_openai.assert_called_once_with(api_key="test_openai_api_key")
