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
                "content": "You are an expert academic research assistant specializing in EU Horizon projects. Your objective is to conduct a thorough, scholarly comparison between two project descriptions, offering a structured and detailed analysis.",
            },
            {
                "role": "user",
                "content": f"""
Conduct a detailed, academic-level comparison of the following two project descriptions:

1. My project: {my_project}

2. Existing EU Horizon project: {existing_project}

Please structure your analysis as follows:

1. **Summary**: 
   Provide a concise, one-sentence summary of the existing EU Horizon project, highlighting its primary goals and innovations.

2. **Commonalities**: 
   Discuss the significant similarities between the two projects, focusing on aspects such as:
   - Research objectives and ambitions
   - Methodological strategies
   - Technological innovations
   - Potential social or economic impacts
   - Intended beneficiaries or stakeholders

3. **Key Differences**: 
   Highlight and analyze the main differences between the projects, considering:
   - Scope and scale of research activities
   - Specific methodologies or technologies used
   - Unique innovations or approaches
   - Geographical or demographic focus
   - Alignment with the EU Horizon program's specific objectives

4. **Similarity Score**: 
   Assign a similarity score on a scale of 0 to 1 (e.g., 0.85), where 0 indicates no similarity and 1 indicates identical projects. 
   
   **Calculation Instructions**:
   - **Weighting Factors**: Consider the importance of each aspect (e.g., research objectives might carry more weight than geographical focus). Assign appropriate weight to each factor based on its significance to the overall goals of the projects.
   - **Balancing Factors**: Balance these factors to reflect both the commonalities and differences. For example, strong similarities in research goals but differences in methodologies should result in a moderate score.
   - **Final Score**: Calculate the final score by aggregating the weighted similarities and differences, ensuring that the score accurately reflects the overall resemblance between the two projects.

5. **Confidence Score**:
   Assign a confidence score on a scale of 0 to 1 (e.g., 0.92), where 0 indicates low confidence and 1 indicates high confidence in the accuracy and reliability of your similarity score and overall analysis.
   
   **Calculation Instructions**:
   - **Input Quality**: Consider the completeness and clarity of the input provided. If the descriptions lack detail or are ambiguous, the confidence score should be lower.
   - **Data Consistency**: Assess the consistency and reliability of the data across the projects. Inconsistent or conflicting information should result in a lower confidence score.
   - **Overall Certainty**: Reflect on the overall certainty of your analysis based on the data provided. The confidence score should reflect how certain you are of the results given the available information.

6. **Justification**: 
   Provide a thorough, evidence-based explanation for the assigned similarity and confidence scores. Reference specific elements from both project descriptions to support your assessment.

Ensure your analysis is objective, precise, and grounded in the provided information. Maintain a formal academic tone throughout the response.
                """,
            },
        ]
