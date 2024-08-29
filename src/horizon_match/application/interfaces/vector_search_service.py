from abc import ABC, abstractmethod
from typing import List
from horizon_match.domain.entities.project import Project


class VectorSearchService(ABC):
    @abstractmethod
    def search(self, query: str, k: int) -> List[Project]:
        """
        Perform a vector search for similar projects based on the given query.

        Args:
            query (str): The project description or search query.
            k (int): The number of similar projects to return.

        Returns:
            List[Project]: A list of Project objects representing the most similar projects.
        """
        pass
