from pydantic import BaseModel, Field


class Comparison(BaseModel):
    summary: str = Field(
        ..., description="One-sentence summary of the existing project"
    )
    similarity: str = Field(..., description="Similarities between the projects")
    difference: str = Field(..., description="Differences between the projects")
    score: float = Field(
        ..., description="Similarity score (0 to 1 with 1 being most similar)"
    )
    reason: str = Field(..., description="Brief explanation for the score")
