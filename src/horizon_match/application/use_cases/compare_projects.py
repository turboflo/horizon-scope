from typing import List
from horizon_match.application.interfaces.vector_search_service import (
    VectorSearchService,
)
from horizon_match.application.interfaces.comparison_service import ComparisonService
from horizon_match.domain.entities.comparison_result import ComparisonResult


class CompareProjects:
    def __init__(
        self,
        vector_search_service: VectorSearchService,
        comparison_service: ComparisonService,
    ):
        self.vector_search_service = vector_search_service
        self.comparison_service = comparison_service

    def execute(self, query: str, k: int) -> List[ComparisonResult]:
        """
        Execute the project comparison use case.

        This method performs a vector search to find similar projects,
        then compares each result with the input query.

        Args:
            query (str): The project description or search query.
            k (int): The number of similar projects to retrieve and compare.

        Returns:
            List[ComparisonResult]: A list of comparison results for the most similar projects.
        """
        # Perform vector search to find similar projects
        similar_projects = self.vector_search_service.search(query, k)

        # Compare the query with each similar project
        results = []
        for project in similar_projects:
            comparison = self.comparison_service.compare(query, project.description)
            results.append(comparison)

        return results
