from typing import Any, List
from horizon_match.application.use_cases.compare_projects import CompareProjects
from horizon_match.domain.entities.horizon_match_result import HorizonMatchResult
from horizon_match.infrastructure.services.pinecone_search_service import (
    PineconeSearchService,
)
from horizon_match.infrastructure.services.openai_comparison_service import (
    OpenAIComparisonService,
)
from horizon_match.infrastructure.config.config_manager import ConfigManager
from horizon_match.domain.entities.comparison import Comparison
from horizon_match.domain.entities.project import Project


class HorizonMatchClient:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.vector_search_service = PineconeSearchService(config_manager)
        self.comparison_service = OpenAIComparisonService(config_manager)
        self.compare_projects_use_case = CompareProjects(
            self.vector_search_service, self.comparison_service
        )

    @classmethod
    def from_config(cls, config_path: str = "config.yml") -> "HorizonMatchClient":
        config = ConfigManager(config_path)
        return cls(config)

    def match(self, query: str, k: int) -> List[HorizonMatchResult]:
        return self.compare_projects_use_case.execute(query, k)

    def index_project(self, project: Project) -> None:
        self.vector_search_service.index_project(project)

    def search_projects(self, query: str, k: int) -> List[Project]:
        return self.vector_search_service.search(query, k)

    def get_config(self, *keys: str, default: Any = None) -> Any:
        return self.config_manager.get(*keys, default=default)
