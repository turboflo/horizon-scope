from __future__ import annotations
from typing import Any
from horizon_scope.application.use_cases.compare_projects import CompareProjects
from horizon_scope.domain.entities.comparison import Comparison
from horizon_scope.domain.entities.horizon_scope_result import HorizonScopeResult
from horizon_scope.infrastructure.services.pinecone_search_service import (
    PineconeSearchService,
)
from horizon_scope.infrastructure.services.openai_comparison_service import (
    OpenAIComparisonService,
)
from horizon_scope.infrastructure.config.config_manager import ConfigManager
from horizon_scope.domain.entities.project import Project


class HorizonScopeClient:
    """Client for handling horizon scope operations.

    Attributes:
        config_manager (ConfigManager): Configuration manager for the client.
        vector_search_service (PineconeSearchService): Service for vector-based search operations.
        comparison_service (OpenAIComparisonService): Service for comparing results using OpenAI.
        compare_projects_use_case (CompareProjects): Use case for comparing projects.
    """

    def __init__(self, config_manager: ConfigManager) -> None:
        """Initialize the HorizonScopeClient with a configuration manager.

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
    def from_config(cls, config_path: str = "config.yml") -> HorizonScopeClient:
        """Create a HorizonScopeClient instance from a configuration file.

        Args:
            config_path (str, optional): Path to the configuration file. Defaults to "config.yml".

        Returns:
            HorizonScopeClient: An instance of HorizonScopeClient initialized with the given configuration.
        """
        config = ConfigManager(config_path)
        return cls(config)

    def match(self, query: str, k: int) -> list[HorizonScopeResult]:
        """Perform a match operation using the provided query.

        Args:
            query (str): The query string to match against.
            k (int): The number of results to return.

        Returns:
            list[HorizonScopeResult]: A list of HorizonScopeResult objects matching the query.
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

    def compare_projects(self, my_project: str, existing_project: str) -> Comparison:
        """Compare two projects.

        Args:
            my_project (str): The description of my project.
            existing_project (str): The description of the existing project.

        Returns:
            Comparison: The comparison result between the two projects.
        """
        return self.comparison_service.compare(my_project, existing_project)

    def get_config(self, *keys: str, default: Any = None) -> Any:
        """Retrieve configuration values based on the provided keys.

        Args:
            *keys (str): The keys for the configuration values to retrieve.
            default (Any, optional): The default value to return if the key is not found. Defaults to None.

        Returns:
            Any: The configuration value corresponding to the provided keys, or the default value if not found.
        """
        return self.config_manager.get(*keys, default=default)
