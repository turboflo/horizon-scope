from openai import OpenAI
from typing import List
from horizon_match.application.interfaces.comparison_service import ComparisonService
from horizon_match.domain.entities.comparison_result import ComparisonResult
from horizon_match.infrastructure.config.config_manager import ConfigManager


class OpenAIComparisonService(ComparisonService):
    def __init__(self, config: ConfigManager):
        self.config = config
        openai_api_key = self.config.get(
            "horizon-match", "comparison-service", "api_key"
        )
        self.client = OpenAI(api_key=openai_api_key)
        self.model = self.config.get("horizon-match", "comparison-service", "model")

    def compare(self, my_project: str, existing_project: str) -> ComparisonResult:
        messages = self._create_comparison_prompt(my_project, existing_project)

        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=messages,
            response_format=ComparisonResult,
        )

        return completion.choices[0].message.parsed

    def _create_comparison_prompt(
        self, my_project: str, existing_project: str
    ) -> List[dict[str, str]]:
        return [
            {
                "role": "system",
                "content": "You are an academic researcher's assistant. Compare two project descriptions and provide a structured analysis.",
            },
            {
                "role": "user",
                "content": f"""
                Compare the following two project descriptions:

                My project: {my_project}

                Existing project: {existing_project}

                Provide your analysis with the following structure:
                - summary: One-sentence summary of the existing project
                - similarity: Similarities between the projects
                - difference: Differences between the projects
                - score: Similarity score (0-100)
                - reason: Brief explanation for the score

                Ensure that the score is an integer between 0 and 100.
                """,
            },
        ]
