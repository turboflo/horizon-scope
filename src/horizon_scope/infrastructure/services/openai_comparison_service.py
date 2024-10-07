from __future__ import annotations
from typing import List, Dict
from openai import OpenAI
from horizon_scope.application.interfaces.comparison_service import ComparisonService
from horizon_scope.domain.entities.comparison import Comparison
from horizon_scope.infrastructure.config.config_manager import ConfigManager

MAX_PROJECT_LENGTH = 5000


class OpenAIComparisonService(ComparisonService):
    """Service for comparing project descriptions using OpenAI's language model.

    This service uses OpenAI to generate detailed comparisons between two project descriptions,
    providing insights into their similarities and differences.

    Attributes:
        config (ConfigManager): Configuration manager for accessing API keys and model information.
        client (OpenAI): OpenAI client for generating comparisons.
        model (str): The model used for generating the comparison.
    """

    def __init__(self, config: ConfigManager) -> None:
        """Initialize OpenAIComparisonService with configuration settings.

        Args:
            config (ConfigManager): Configuration manager for the service.
        """
        self.config = config
        openai_api_key = self.config.get(
            "horizon-scope", "comparison-service", "api_key"
        )
        self.client = OpenAI(api_key=openai_api_key)
        self.model = self.config.get("horizon-scope", "comparison-service", "model")

    def compare(self, my_project: str, existing_project: str) -> Comparison:
        """Compare two project descriptions using OpenAI.

        Args:
            my_project (str): Description of the user's project.
            existing_project (str): Description of the existing project.

        Returns:
            Comparison: A Comparison object containing the results of the comparison.

        Raises:
            ValueError: If either project description is empty or exceeds the maximum length.
        """
        self._validate_input(my_project, "My project")
        self._validate_input(existing_project, "Existing project")

        messages = self._create_comparison_prompt(my_project, existing_project)

        # completion = self.client.chat.completions.create(
        #     model=self.model,
        #     messages=messages,
        #     response_format={"type": "json_object"},
        # )
        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=messages,
            response_format=Comparison,
        )

        # response_content = completion.choices[0].message.content
        # return Comparison.model_validate_json(response_content)
        return completion.choices[0].message.parsed

    def _validate_input(self, project: str, project_name: str) -> None:
        """Validate the project description input.

        Args:
            project (str): The project description to validate.
            project_name (str): The name of the project (for error messages).

        Raises:
            ValueError: If the project description is empty or exceeds the maximum length.
        """
        if not project.strip():
            raise ValueError(f"{project_name} description cannot be empty")
        if len(project) > MAX_PROJECT_LENGTH:
            raise ValueError(
                f"{project_name} description exceeds maximum length of {MAX_PROJECT_LENGTH} characters"
            )

    def _create_comparison_prompt(
        self, my_project: str, existing_project: str
    ) -> List[Dict[str, str]]:
        """Create the prompt for the comparison model.

        Args:
            my_project (str): Description of the user's project.
            existing_project (str): Description of the existing project.

        Returns:
            List[Dict[str, str]]: A list of messages forming the prompt for the OpenAI model.
        """
        return [
            {
                "role": "system",
                "content": "You are a highly experienced academic research assistant specializing in EU Horizon projects. Your task is to conduct a thorough, scholarly comparison between two project descriptions, providing a structured and detailed analysis with an emphasis on their similarities and differences.",
            },
            {
                "role": "user",
                "content": f"""
Conduct an in-depth, academic-level comparison of the following two project descriptions:

1. **Input Project**: {my_project}
2. **Existing EU Horizon Project**: {existing_project}

Please structure your analysis as follows:

1. **Summary**:  
   Provide a concise, one-sentence summary of the existing EU Horizon project, focusing on its primary goals, innovative elements, and alignment with Horizon objectives.

2. **Commonalities**:  
   Discuss the significant similarities between the two projects, focusing on aspects such as:
   - **Research Objectives**: Shared ambitions and overarching goals.
   - **Methodological Approaches**: Similarities in research strategies or methods used.
   - **Technological Innovations**: Identify overlapping innovations or technologies.
   - **Potential Social or Economic Impacts**: Common expected societal or economic effects.
   - **Beneficiaries/Stakeholders**: Alignment in terms of intended beneficiaries or stakeholders.

3. **Key Differences**:  
   Highlight and analyze the main differences between the projects, considering:
   - **Scope and Scale of Research**: Compare the scope and depth of research activities.
   - **Unique Methodologies/Technologies**: Specific differences in methods or technologies used.
   - **Innovative Contributions**: Identify distinctive breakthroughs or novel approaches.
   - **Geographical or Demographic Focus**: Explore differences in the regional or demographic focus.
   - **Alignment with EU Horizon Objectives**: How each project aligns with Horizon Europe’s specific priorities.

4. **Similarity Score** (0 to 1 scale):  
   Assign a similarity score between 0 and 1, where 0 represents no similarity and 1 represents nearly identical projects.  
   **Instructions**:
   - **Weighting Factors**: Give more weight to core aspects like research objectives, while factors like geographic focus or stakeholder groups can receive less weight.
   - **Balancing**: Balance similarities and differences to ensure the final score reflects the overall resemblance between the projects.

5. **Confidence Score** (0 to 1 scale):  
   Assign a confidence score using the following formula:

   Confidence Score = (Input Quality * 0.25) + (Comparative Clarity * 0.20) + (Domain Knowledge Alignment * 0.20) + (Consistency * 0.15) + (Quantifiability * 0.20)

   - **Input Quality** (0.25): Rate from 0-1 based on the clarity, completeness, and specificity of both project descriptions.
   - **Comparative Clarity** (0.20): How clear and discernible are the similarities and differences between the two projects?
   - **Domain Knowledge Alignment** (0.20): How well do the projects align with EU Horizon’s overall goals and research focus?
   - **Consistency** (0.15): Are both project descriptions internally consistent and coherent?
   - **Quantifiability** (0.20): How many aspects of the comparison are measurable or objective?

   Round the final confidence score to two decimal places.

6. **Justification**:  
   Provide a thorough explanation for the assigned similarity and confidence scores, referring to specific elements from both project descriptions to justify your assessment.

Ensure your analysis remains objective, precise, and scholarly throughout, focusing on the comparative aspects while maintaining a formal academic tone.
""",
            },
        ]
