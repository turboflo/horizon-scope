from pydantic import BaseModel, Field


class Comparison(BaseModel):
    """Represents the result of a comparison between two projects.

    Attributes:
        summary (str): A concise, one-sentence summary of the existing EU Horizon project, highlighting its primary objectives and key innovations.
        similarity (str): Detailed analysis of significant commonalities between the projects, considering research goals, methodologies, technological focus, impacts, and stakeholders.
        difference (str): Comprehensive examination of notable distinctions between the projects, addressing scope, techniques, innovations, geographic focus, and alignment with EU Horizon objectives.
        score (float): Similarity score ranging from 0 to 1 (with two decimal places precision), where 0 indicates no similarity and 1 indicates identical projects.
        confidence (float): Confidence score ranging from 0 to 1 (with two decimal places precision), where 0 indicates low confidence and 1 indicates high confidence in the accuracy and reliability of the similarity score and analysis.
        reason (str): Thorough, evidence-based justification for the assigned similarity and confidence scores, referencing specific elements from both project descriptions.
    """

    summary: str = Field(
        ...,
        description="Concise, one-sentence summary of the existing EU Horizon project, highlighting primary objectives and key innovations.",
    )
    similarity: str = Field(
        ...,
        description="Detailed analysis of significant commonalities between the projects, considering research goals, methodologies, technological focus, impacts, and stakeholders.",
    )
    difference: str = Field(
        ...,
        description="Comprehensive examination of notable distinctions between the projects, addressing scope, techniques, innovations, geographic focus, and alignment with EU Horizon objectives.",
    )
    score: float = Field(
        ...,
        description="Similarity score from 0 to 1 (with two decimal places precision), where 0 indicates no similarity and 1 indicates identical projects.",
    )
    confidence: float = Field(
        ...,
        description="Confidence score from 0 to 1 (with two decimal places precision), where 0 indicates low confidence and 1 indicates high confidence in the accuracy and reliability of the similarity score and analysis.",
    )
    reason: str = Field(
        ...,
        description="Thorough, evidence-based justification for the assigned similarity and confidence scores, referencing specific elements from both project descriptions.",
    )
