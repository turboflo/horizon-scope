from pydantic import BaseModel, Field


class Comparison(BaseModel):
    summary: str = Field(
        ...,
        description="Concise, one-sentence summary of the existing EU Horizon project, highlighting primary objectives and key innovations",
    )
    similarity: str = Field(
        ...,
        description="Detailed analysis of significant commonalities between the projects, considering research goals, methodologies, technological focus, impacts, and stakeholders",
    )
    difference: str = Field(
        ...,
        description="Comprehensive examination of notable distinctions between the projects, addressing scope, techniques, innovations, geographic focus, and alignment with EU Horizon objectives",
    )
    score: float = Field(
        ...,
        description="Similarity score from 0 to 1 (with two decimal places precision), where 0 indicates no similarity and 1 indicates identical projects",
    )
    reason: str = Field(
        ...,
        description="Thorough, evidence-based justification for the assigned similarity score, referencing specific elements from both project descriptions",
    )
