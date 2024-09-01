from __future__ import annotations
from pinecone import Pinecone
from openai import OpenAI
from typing import List
from datetime import datetime
from horizon_scope.application.interfaces.vector_search_service import (
    VectorSearchService,
)
from horizon_scope.domain.entities.project import Project
from horizon_scope.infrastructure.config.config_manager import ConfigManager


class PineconeSearchService(VectorSearchService):
    """Service for searching and indexing projects using Pinecone and OpenAI.

    This service integrates Pinecone for vector-based search and OpenAI for generating embeddings.

    Attributes:
        config (ConfigManager): Configuration manager for accessing API keys and model information.
        index (Pinecone.Index): Pinecone index for storing and querying project embeddings.
        openai_client (OpenAI): OpenAI client for generating embeddings.
        embedding_model (str): The model used for generating embeddings.
    """

    def __init__(self, config: ConfigManager) -> None:
        """Initialize PineconeSearchService with configuration settings.

        Args:
            config (ConfigManager): Configuration manager for the service.
        """
        self.config = config
        # Initialize Pinecone
        pinecone_api_key = self.config.get(
            "horizon-scope", "vector-search-service", "store", "api_key"
        )
        pc = Pinecone(api_key=pinecone_api_key)
        index_name = self.config.get(
            "horizon-scope", "vector-search-service", "store", "index"
        )
        self.index = pc.Index(index_name)
        # Initialize OpenAI client for embeddings
        openai_api_key = self.config.get(
            "horizon-scope", "vector-search-service", "embeddings", "api_key"
        )
        self.openai_client = OpenAI(api_key=openai_api_key)
        self.embedding_model = self.config.get(
            "horizon-scope", "vector-search-service", "embeddings", "model"
        )

    def search(self, query: str, k: int) -> List[Project]:
        """Search for projects matching the query.

        Args:
            query (str): The query string to search for.
            k (int): The number of top results to return.

        Returns:
            List[Project]: A list of projects matching the query.
        """
        # Generate embedding for the query
        embedding_response = self.openai_client.embeddings.create(
            model=self.embedding_model, input=query
        )
        query_embedding = embedding_response.data[0].embedding

        # Perform the search using Pinecone
        search_results = self.index.query(
            vector=query_embedding, top_k=k, include_metadata=True
        )

        # Convert results to Project objects
        projects = []
        for match in search_results.matches:
            project = Project(
                id=match.id,
                title=match.metadata.get("title", ""),
                description=match.metadata.get("objective", ""),
                content_update_date=match.metadata.get("contentUpdateDate", ""),
                similarity=match.score,
            )
            projects.append(project)
        return projects

    def index_project(self, project: Project) -> None:
        """Index a project in Pinecone.

        Args:
            project (Project): The project to be indexed.
        """
        # Generate embedding for the project description
        embedding_response = self.openai_client.embeddings.create(
            model=self.embedding_model, input=project.description
        )
        project_embedding = embedding_response.data[0].embedding

        # Index the project in Pinecone
        self.index.upsert(
            vectors=[
                {
                    "id": project.id,
                    "values": project_embedding,
                    "metadata": {
                        "title": project.title,
                        "objective": project.description,
                        "contentUpdateDate": project.content_update_date
                        or datetime.now().isoformat(),
                    },
                }
            ]
        )
