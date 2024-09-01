from typing import List
from horizon_match.application.interfaces.vector_search_service import (
    VectorSearchService,
)
from horizon_match.application.interfaces.comparison_service import ComparisonService
from horizon_match.domain.entities.horizon_match_result import HorizonMatchResult


class CompareProjects:
    """Handles the comparison of a query project against a set of similar projects.

    This class uses a vector search service to find projects similar to the query and then uses
    a comparison service to evaluate the similarity of each found project. Results are sorted
    by similarity score.

    Attributes:
        vector_search_service (VectorSearchService): Service for performing vector-based searches to find similar projects.
        comparison_service (ComparisonService): Service for comparing project descriptions to determine similarity.
    """

    def __init__(
        self,
        vector_search_service: VectorSearchService,
        comparison_service: ComparisonService,
    ) -> None:
        """Initialize CompareProjects with vector search and comparison services.

        Args:
            vector_search_service (VectorSearchService): The service to search for similar projects.
            comparison_service (ComparisonService): The service to compare project descriptions.
        """
        self.vector_search_service = vector_search_service
        self.comparison_service = comparison_service

    def execute(self, query: str, k: int) -> List[HorizonMatchResult]:
        """Perform the comparison of the query project with similar projects.

        Args:
            query (str): The description of the query project to compare.
            k (int): The number of similar projects to retrieve and compare.

        Returns:
            List[HorizonMatchResult]: A list of HorizonMatchResult objects, sorted by similarity score in descending order.
        """
        # Perform vector search to find similar projects
        similar_projects = self.vector_search_service.search(query, k)

        # Compare the query with each similar project
        results: List[HorizonMatchResult] = []
        for project in similar_projects:
            # Compare the query description with the project description
            comparison = self.comparison_service.compare(query, project.description)
            result = HorizonMatchResult(project=project, comparison=comparison)
            results.append(result)

        # Sort results by AI similarity score in descending order
        results.sort(key=lambda x: x.comparison.score, reverse=True)

        return results
