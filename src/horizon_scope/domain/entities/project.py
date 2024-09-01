from pydantic import BaseModel, Field
from typing import Optional


class Project(BaseModel):
    """Represents a project with details for comparison and indexing.

    Attributes:
        id (str): Unique identifier for the project.
        description (str): Detailed description of the project.
        title (Optional[str]): Title of the project. Defaults to None.
        content_update_date (Optional[str]): Date when the project content was last updated. Defaults to None.
        similarity (Optional[float]): Similarity score of the project compared to another project. Defaults to None.
    """

    id: str = Field(..., description="Unique identifier for the project")
    description: str = Field(..., description="Detailed description of the project")
    title: Optional[str] = Field(None, description="Title of the project")
    content_update_date: Optional[str] = Field(
        None, description="Date when the project content was last updated"
    )
    similarity: Optional[float] = Field(
        None, description="Similarity score of the project compared to another project"
    )
