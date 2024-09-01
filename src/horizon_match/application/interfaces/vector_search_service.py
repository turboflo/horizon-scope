from abc import ABC, abstractmethod
from typing import List
from horizon_match.domain.entities.project import Project


class VectorSearchService(ABC):
    """Abstract base class for vector search services.

    This class defines an interface for performing vector-based searches to find projects similar
    to a given query. Concrete implementations should provide the specifics of how the search
    is executed and how the results are retrieved.

    Methods:
        search (str, int) -> List[Project]: Perform a vector search for similar projects based on the given query.
    """

    @abstractmethod
    def search(self, query: str, k: int) -> List[Project]:
        """Perform a vector search for similar projects based on the given query.

        Args:
            query (str): The project description or search query.
            k (int): The number of similar projects to return.

        Returns:
            List[Project]: A list of Project objects representing the most similar projects.
        """
        pass
