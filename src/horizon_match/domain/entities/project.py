from pydantic import BaseModel, Field
from typing import Optional


class Project(BaseModel):
    id: str = Field(..., description="Unique identifier for the project")
    description: str = Field(..., description="Detailed description of the project")
    title: Optional[str] = Field(None, description="Title of the project")
    created_at: Optional[str] = Field(None, description="Creation date of the project")
    similarity: Optional[float] = Field(
        None, description="Simmilarity score of the project"
    )
