from dataclasses import dataclass
from horizon_match.domain.entities.comparison import Comparison
from horizon_match.domain.entities.project import Project


@dataclass
class HorizonMatchResult:
    project: Project
    comaprison: Comparison
