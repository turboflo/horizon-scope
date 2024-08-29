import os

def create_jupyter_notebook():
    notebook_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Horizon Match - Basic Usage\n",
                    "\n",
                    "This notebook demonstrates how to use the Horizon Match project for comparing project ideas using vector search and GPT-4-mini."
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Setup\n",
                    "\n",
                    "First, let's import the necessary modules and initialize the client."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import asyncio\n",
                    "from horizon_match.presentation.horizon_match_client import HorizonMatchClient\n",
                    "\n",
                    "# Initialize the client\n",
                    "client = HorizonMatchClient.from_config(\"config.yml\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Comparing Projects\n",
                    "\n",
                    "Now, let's use the client to compare a project idea with existing projects in the database."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "async def compare_projects(query: str, k: int = 5):\n",
                    "    results = await client.match(query, k)\n",
                    "    for i, result in enumerate(results, 1):\n",
                    "        print(f\"Result {i}:\")\n",
                    "        print(f\"Summary: {result.summary}\")\n",
                    "        print(f\"Similarity: {result.similarity}\")\n",
                    "        print(f\"Difference: {result.difference}\")\n",
                    "        print(f\"Score: {result.score}\")\n",
                    "        print(f\"Reason: {result.reason}\")\n",
                    "        print(\"---\")\n",
                    "\n",
                    "# Example usage\n",
                    "query = \"A mobile app that uses AI to recommend personalized workout routines\"\n",
                    "await compare_projects(query)"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Analyzing Results\n",
                    "\n",
                    "After running the comparison, you can analyze the results to understand how your project idea relates to existing projects in the database. Consider the following:\n",
                    "\n",
                    "1. Look at the similarity scores to gauge how close your idea is to existing projects.\n",
                    "2. Pay attention to the similarities and differences to understand what aspects of your idea are unique or common.\n",
                    "3. Use the summaries to get a quick overview of related projects.\n",
                    "4. Read the reasons provided for each comparison to understand the rationale behind the scores."
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Next Steps\n",
                    "\n",
                    "Based on the results, you might want to:\n",
                    "\n",
                    "1. Refine your project idea to differentiate it from similar existing projects.\n",
                    "2. Explore collaboration opportunities with related projects.\n",
                    "3. Conduct more detailed research on the most similar projects.\n",
                    "4. Use the insights gained to improve your project proposal or pitch."
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.10"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    import json
    
    # Create the notebook in the src directory
    notebook_path = os.path.join('src', 'horizon_match_basic_usage.ipynb')
    with open(notebook_path, 'w') as f:
        json.dump(notebook_content, f, indent=2)

    print(f"Jupyter notebook created successfully at {notebook_path}")

# Run the function to create the notebook
create_jupyter_notebook()
