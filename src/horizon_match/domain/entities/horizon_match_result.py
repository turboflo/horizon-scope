from dataclasses import dataclass
from horizon_match.domain.entities.comparison import Comparison
from horizon_match.domain.entities.project import Project


@dataclass
class HorizonMatchResult:
    """Represents the result of a comparison between a project and another entity.

    Attributes:
        project (Project): The project that is being compared.
        comparison (Comparison): The result of the comparison, including similarity and analysis details.
    """

    project: Project
    comparison: Comparison
