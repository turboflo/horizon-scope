from pydantic import BaseModel, Field


class Comparison(BaseModel):
    summary: str = Field(
        ..., description="One-sentence summary of the existing project"
    )
    similarity: str = Field(..., description="Similarities between the projects")
    difference: str = Field(..., description="Differences between the projects")
    score: float = Field(..., description="Similarity score (0.0 - 1.0)")
    reason: str = Field(..., description="Brief explanation for the score")
