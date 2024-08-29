from abc import ABC, abstractmethod
from horizon_match.domain.entities.comparison_result import ComparisonResult


class ComparisonService(ABC):
    @abstractmethod
    def compare(self, my_project: str, existing_project: str) -> ComparisonResult:
        """
        Compare two project descriptions and return a ComparisonResult.

        Args:
            my_project (str): The description of the user's project idea.
            existing_project (str): The description of an existing project to compare against.

        Returns:
            ComparisonResult: An object containing the comparison details.
        """
        pass
