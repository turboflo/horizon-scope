from pydantic import BaseModel, Field
from horizon_scope.domain.entities.comparison import Comparison
from horizon_scope.domain.entities.project import Project


class HorizonScopeResult(BaseModel):
    """Represents the result of a comparison between a project and another entity.

    Attributes:
        project (Project): The project that is being compared.
        comparison (Comparison): The result of the comparison, including similarity and analysis details.
    """

    project: Project = Field(..., description="The project that is being compared.")
    comparison: Comparison = Field(
        ...,
        description="The result of the comparison, including similarity and analysis details.",
    )
