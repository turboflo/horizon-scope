from openai import OpenAI
from typing import List
from horizon_match.application.interfaces.comparison_service import ComparisonService
from horizon_match.domain.entities.comparison import Comparison
from horizon_match.infrastructure.config.config_manager import ConfigManager


class OpenAIComparisonService(ComparisonService):
    def __init__(self, config: ConfigManager):
        self.config = config
        openai_api_key = self.config.get(
            "horizon-match", "comparison-service", "api_key"
        )
        self.client = OpenAI(api_key=openai_api_key)
        self.model = self.config.get("horizon-match", "comparison-service", "model")

    def compare(self, my_project: str, existing_project: str) -> Comparison:
        messages = self._create_comparison_prompt(my_project, existing_project)

        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=messages,
            response_format=Comparison,
        )

        return completion.choices[0].message.parsed

    def _create_comparison_prompt(
        self, my_project: str, existing_project: str
    ) -> List[dict[str, str]]:
        return [
            {
                "role": "system",
                "content": "You are a highly specialized academic research assistant with expertise in EU Horizon projects. Your task is to conduct a rigorous, scholarly comparison of two project descriptions, providing a structured, in-depth analysis.",
            },
            {
                "role": "user",
                "content": f"""
Perform a comprehensive, academic-level comparison of the following two project descriptions:

My project: {my_project}

Existing EU Horizon project: {existing_project}

Provide your analysis using the following structure:

1. Summary:
   Deliver a concise, one-sentence summary of the existing EU Horizon project, highlighting its primary objectives and key innovations.

2. Similarities:
   Identify and elaborate on the significant commonalities between the two projects. Consider aspects such as:
   - Research goals and objectives
   - Methodological approaches
   - Technological focus areas
   - Potential societal or economic impacts
   - Target beneficiaries or stakeholders

3. Differences:
   Analyze and articulate the notable distinctions between the projects. Address factors including:
   - Scope and scale of the research
   - Specific techniques or technologies employed
   - Unique innovations or novel approaches
   - Geographic or demographic focus
   - Alignment with EU Horizon program objectives

4. Similarity Score:
   Assign a similarity score on a scale from 0 to 1, where 0 indicates no similarity and 1 indicates identical projects. Use two decimal places for precision (e.g., 0.75).

5. Justification:
   Provide a thorough, evidence-based explanation for the assigned similarity score. Reference specific elements from both project descriptions to support your assessment.

Ensure your analysis is objective, precise, and grounded in the information provided. Maintain a formal, academic tone throughout your response.
                """,
            },
        ]
