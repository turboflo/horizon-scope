from abc import ABC, abstractmethod
from horizon_scope.domain.entities.comparison import Comparison


class ComparisonService(ABC):
    """Abstract base class for comparison services.

    This class defines an interface for comparing two project descriptions. Concrete implementations
    should provide the specifics of how the comparison is performed and how the results are generated.

    Methods:
        compare (str, str) -> Comparison: Compare two project descriptions and return a Comparison object.
    """

    @abstractmethod
    def compare(self, my_project: str, existing_project: str) -> Comparison:
        """Compare two project descriptions and return a Comparison object.

        Args:
            my_project (str): The description of the user's project idea.
            existing_project (str): The description of an existing project to compare against.

        Returns:
            Comparison: An object containing the comparison details.
        """
        pass
