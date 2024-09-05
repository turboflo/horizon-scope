# Horizon Scope ✨📑

[![CI](https://img.shields.io/github/actions/workflow/status/turboflo/horizon-scope/ci.yml?branch=development&flat&logo=github&label=CI)](https://github.com/turboflo/horizon-scope/actions/workflows/ci.yml)
[![GitHub Release](https://img.shields.io/github/v/release/turboflo/horizon-scope?style=fflat&logo=github)](https://github.com/turboflo/horizon-scope/releases)
[![GitHub contributors](https://img.shields.io/github/contributors/turboflo/horizon-scope?style=flat&logo=github)](https://github.com/turboflo/horizon-scope/graphs/contributors)



**Horizon Scope** is a project comparison and analysis tool that leverages vector search and AI-powered comparisons to help users discover similar projects and gain valuable insights.

## Try It Out 🚀

Experience Horizon Scope in action! Visit my live demo:

[![Streamlit App](https://img.shields.io/badge/Streamlit-Open_App-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://horizon-scope.streamlit.app)

## Key Features 🌟

- **Vector-based Project Search** 🔍: 
  - Utilizes [Pinecone](https://www.pinecone.io/) for efficient similarity searches across a database of projects.
- **AI-powered Project Comparison** 🤖:
  - Employs [OpenAI's GPT models](https://openai.com/) to generate detailed comparisons between user input and existing projects.
- **Web Interface** 💻:
  - Offers a user-friendly interface built with [Streamlit](https://streamlit.io/).

## Components 🧩

- **`HorizonScopeClient`**: Main client class interfacing with core functionalities.
- **`VectorSearchService`**: Manages vector-based similarity searches using Pinecone.
- **`ComparisonService`**: Handles AI-powered project comparisons using OpenAI.
- **Streamlit Web Application**: Interactive interface for project comparisons.

## Functionality ⚙️

1. **Input Project Descriptions** ✏️: Users input project descriptions via the web interface or Python client.
2. **Vector Similarity Search** 📈: The system searches for similar projects using Pinecone.
3. **AI-powered Comparisons** 🔗: Provides insights on similarities, differences, and overall analysis.
4. **Results and Metrics** 📊: Includes AI Similarity score, Cosine Similarity, and Confidence.

## Workflow 🛠️

```mermaid
---
config:
  theme: neo-dark
---

flowchart TD
    A(["User Input: <br> query='PROJECT DESCRIPTION' <br> k=3"]) --> B("Generate Embeddings")
    B <-- IN: query <br> OUT: embedding --> X_B[("OpenAI <br> text-embedding-3-small")]
    B --> C("Search similar Projects")
    C <-- IN: embedding, k <br> OUT: List[Project] --> X_C[("Pinecone <br> projects-text-embedding-3-small")]
    C --> D{"For each Project (k)"}
    D --> E["Generate ComparisonResult"]
    E <-- IN: query, existing_project <br> OUT: ComparisonResult --> X_E[("OpenAI <br> gpt-4o-mini")]
    E -- List[ComparisonResult] --> F(["Display ComparisonResult's"])
```

## Data Sources 📚

This tool uses project data embedded from the following sources:
- [CORDIS EU Research Projects under Horizon 2020](https://data.europa.eu/euodp/en/data/dataset/cordisH2020projects)
- [CORDIS EU Research Projects under Horizon Europe 2021-2027](https://data.europa.eu/data/datasets/cordis-eu-research-projects-under-horizon-europe-2021-2027)

## Acknowledgements 🙏

- [Pinecone](https://www.pinecone.io/) for vector similarity search.
- [OpenAI](https://openai.com/) for AI-powered project comparison models.
- [Streamlit](https://streamlit.io/) for the web interface framework.
