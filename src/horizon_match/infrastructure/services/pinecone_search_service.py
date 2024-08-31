from pinecone import Pinecone
from openai import OpenAI
from typing import List
from datetime import datetime
from horizon_match.application.interfaces.vector_search_service import (
    VectorSearchService,
)
from horizon_match.domain.entities.project import Project
from horizon_match.infrastructure.config.config_manager import ConfigManager


class PineconeSearchService(VectorSearchService):
    def __init__(self, config: ConfigManager):
        self.config = config

        # Initialize Pinecone
        pinecone_api_key = self.config.get(
            "horizon-match", "vector-search-service", "store", "api_key"
        )
        pc = Pinecone(api_key=pinecone_api_key)
        index_name = self.config.get(
            "horizon-match", "vector-search-service", "store", "index"
        )
        self.index = pc.Index(index_name)

        # Initialize OpenAI client for embeddings
        openai_api_key = self.config.get(
            "horizon-match", "vector-search-service", "embeddings", "api_key"
        )
        self.openai_client = OpenAI(api_key=openai_api_key)
        self.embedding_model = self.config.get(
            "horizon-match", "vector-search-service", "embeddings", "model"
        )

    def search(self, query: str, k: int) -> List[Project]:
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
                author=match.metadata.get("author", ""),
                created_at=match.metadata.get("contentUpdateDate", ""),
                tags=match.metadata.get("tags", []),
                similarity=match.get("score", None),
            )
            projects.append(project)

        return projects

    def index_project(self, project: Project):
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
                        "author": project.author,
                        "contentUpdateDate": project.created_at
                        or datetime.now().isoformat(),
                        "tags": project.tags,
                    },
                }
            ]
        )
