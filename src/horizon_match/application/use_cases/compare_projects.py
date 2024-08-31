from typing import List
from horizon_match.application.interfaces.vector_search_service import (
    VectorSearchService,
)
from horizon_match.application.interfaces.comparison_service import ComparisonService
from horizon_match.domain.entities.comparison import Comparison
from horizon_match.domain.entities.horizon_match_result import HorizonMatchResult
from horizon_match.infrastructure.services.state_manager import StateManager


class CompareProjects:
    def __init__(
        self,
        vector_search_service: VectorSearchService,
        comparison_service: ComparisonService,
        state_manager: StateManager | None = None,
    ):
        self.vector_search_service = vector_search_service
        self.comparison_service = comparison_service
        self.state_manager = state_manager or StateManager()

    def execute(self, query: str, k: int) -> List[HorizonMatchResult]:
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
        self.state_manager.update_state("Searching for similar projects...")
        similar_projects = self.vector_search_service.search(query, k)

        # Compare the query with each similar project
        results = []
        for project in similar_projects:
            # Update state to show which project is being compared 1/k
            self.state_manager.update_state(
                f"Comparing project {len(results) + 1}/{k}..."
            )
            comparison = self.comparison_service.compare(query, project.description)
            result = HorizonMatchResult(project, comparison)
            results.append(result)

        # Sort project by AI similarity score
        self.state_manager.update_state("Sorting results by similarity score...")
        results.sort(key=lambda x: x.comparison.score, reverse=True)

        return results
