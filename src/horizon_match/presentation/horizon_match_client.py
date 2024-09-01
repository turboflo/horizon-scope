from __future__ import annotations
from typing import Any
from horizon_match.application.use_cases.compare_projects import CompareProjects
from horizon_match.domain.entities.horizon_match_result import HorizonMatchResult
from horizon_match.infrastructure.services.pinecone_search_service import (
    PineconeSearchService,
)
from horizon_match.infrastructure.services.openai_comparison_service import (
    OpenAIComparisonService,
)
from horizon_match.infrastructure.config.config_manager import ConfigManager
from horizon_match.domain.entities.project import Project


class HorizonMatchClient:
    """Client for handling horizon match operations.

    Attributes:
        config_manager (ConfigManager): Configuration manager for the client.
        vector_search_service (PineconeSearchService): Service for vector-based search operations.
        comparison_service (OpenAIComparisonService): Service for comparing results using OpenAI.
        compare_projects_use_case (CompareProjects): Use case for comparing projects.
    """

    def __init__(self, config_manager: ConfigManager) -> None:
        """Initialize the HorizonMatchClient with a configuration manager.

        Args:
            config_manager (ConfigManager): The configuration manager to use for setting up services.
        """
        self.config_manager = config_manager
        self.vector_search_service = PineconeSearchService(config_manager)
        self.comparison_service = OpenAIComparisonService(config_manager)
        self.compare_projects_use_case = CompareProjects(
            self.vector_search_service, self.comparison_service
        )

    @classmethod
    def from_config(cls, config_path: str = "config.yml") -> HorizonMatchClient:
        """Create a HorizonMatchClient instance from a configuration file.

        Args:
            config_path (str, optional): Path to the configuration file. Defaults to "config.yml".

        Returns:
            HorizonMatchClient: An instance of HorizonMatchClient initialized with the given configuration.
        """
        config = ConfigManager(config_path)
        return cls(config)

    def match(self, query: str, k: int) -> list[HorizonMatchResult]:
        """Perform a match operation using the provided query.

        Args:
            query (str): The query string to match against.
            k (int): The number of results to return.

        Returns:
            list[HorizonMatchResult]: A list of HorizonMatchResult objects matching the query.
        """
        return self.compare_projects_use_case.execute(query, k)

    def index_project(self, project: Project) -> None:
        """Index a project into the vector search service.

        Args:
            project (Project): The project to index.
        """
        self.vector_search_service.index_project(project)

    def search_projects(self, query: str, k: int) -> list[Project]:
        """Search for projects based on the provided query.

        Args:
            query (str): The query string to search for.
            k (int): The number of results to return.

        Returns:
            list[Project]: A list of Project objects matching the search query.
        """
        return self.vector_search_service.search(query, k)

    def get_config(self, *keys: str, default: Any = None) -> Any:
        """Retrieve configuration values based on the provided keys.

        Args:
            *keys (str): The keys for the configuration values to retrieve.
            default (Any, optional): The default value to return if the key is not found. Defaults to None.

        Returns:
            Any: The configuration value corresponding to the provided keys, or the default value if not found.
        """
        return self.config_manager.get(*keys, default=default)
