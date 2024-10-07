"""
This module contains the Streamlit presentation layer for the Horizon Scope application.

It provides functions to create the user interface, handle user interactions,
and display search results and project comparisons.
"""

import os
from typing import List

import streamlit as st

from horizon_scope.infrastructure.config.config_manager import ConfigManager
from horizon_scope.presentation.horizon_scope_client import HorizonScopeClient
from horizon_scope.domain.entities.project import Project
from horizon_scope.domain.entities.comparison import Comparison


def initialize_session_state() -> None:
    """Initialize the Streamlit session state with default values."""
    if "comparing" not in st.session_state:
        st.session_state.comparing = False
    if "results" not in st.session_state:
        st.session_state.results = None
    if "project_description" not in st.session_state:
        st.session_state.project_description = ""
    if "k" not in st.session_state:
        st.session_state.k = 3


def start_comparison():
    st.session_state.comparing = True
    st.session_state.results = None


def toggle_description(i):
    st.session_state[f"show_desc_{i}"] = not st.session_state.get(
        f"show_desc_{i}", False
    )


def create_project_card(
    project: Project,
    index: int,
    client: HorizonScopeClient,
    user_project_description: str,
) -> None:
    """
    Create and display a card for a single project.

    Args:
        project: The project to display.
        index: The index of the project in the search results.
        client: The HorizonScopeClient instance.
        user_project_description: The user's project description.
    """
    col1, col2, col3 = st.columns([1, 4, 1])

    with col1:
        st.metric("Similarity", f"{project.similarity:.1%}")

    with col2:
        st.subheader(project.title or "Untitled Project")
        #
        st.caption(f"Project ID: {project.id}")
        st.caption(f"Updated: {project.content_update_date or 'Date not available'}")

    with col3:
        st.link_button(
            "🔗 View on CORDIS", f"https://cordis.europa.eu/project/id/{project.id}"
        )
        if st.button("🤖 AI Compare", key=f"compare_button_{index}"):
            st.session_state[f"show_comparison_{index}"] = True

    if st.session_state.get(f"show_comparison_{index}", False):
        with st.expander("Comparison Results", expanded=True):
            comparison = get_or_compute_comparison(
                index, client, user_project_description, project.description
            )
            display_comparison_results(comparison)


def get_or_compute_comparison(
    index: int,
    client: HorizonScopeClient,
    user_project_description: str,
    project_description: str,
) -> Comparison:
    """
    Get the existing comparison or compute a new one if it doesn't exist.

    Args:
        index: The index of the project in the search results.
        client: The HorizonScopeClient instance.
        user_project_description: The user's project description.
        project_description: The description of the project to compare.

    Returns:
        The comparison result.
    """
    if f"comparison_{index}" not in st.session_state:
        with st.spinner("Analyzing projects..."):
            comparison = client.compare_projects(
                user_project_description,
                project_description,
            )
        st.session_state[f"comparison_{index}"] = comparison
    else:
        comparison = st.session_state[f"comparison_{index}"]
    return comparison


def display_comparison_results(comparison: Comparison) -> None:
    """
    Display the comparison results in the Streamlit UI.

    Args:
        comparison: The comparison result to display.
    """
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🤖 AI Similarity", f"{comparison.score:.1%}")
    with col2:
        st.metric("🔒 Confidence", f"{comparison.confidence:.1%}")

    st.subheader("Summary")
    st.write(comparison.summary)

    subcol1, subcol2 = st.columns(2)
    with subcol1:
        st.subheader("✅ Similarities")
        st.write(comparison.similarity)
    with subcol2:
        st.subheader("❌ Differences")
        st.write(comparison.difference)

    st.subheader("🧐 Analysis")
    st.write(comparison.reason)


def clear_comparison_data() -> None:
    """Clear all comparison-related data from the session state."""
    keys_to_remove = [
        key
        for key in st.session_state.keys()
        if key.startswith("comparison_") or key.startswith("show_comparison_")
    ]
    for key in keys_to_remove:
        del st.session_state[key]


def main() -> None:
    """Main function to run the Streamlit application."""
    st.set_page_config(
        page_title="Horizon Scope", layout="wide", initial_sidebar_state="collapsed"
    )
    initialize_session_state()

    config_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "config.yml"
    )
    config_manager = ConfigManager(config_path)

    if not config_manager.is_openai_api_key_set():
        handle_missing_api_key()

    client = HorizonScopeClient.from_config(config_path)

    display_sidebar()
    display_main_content(client)


def handle_missing_api_key() -> None:
    """Handle the case when the OpenAI API key is not set."""
    st.warning("OpenAI API key not found. Please enter it below.")
    api_key = st.text_input("OpenAI API key:", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        st.success("API key set. Please reload the page.")
        st.rerun()
    else:
        st.stop()


def display_sidebar() -> None:
    """Display the sidebar content."""
    with st.sidebar:
        st.markdown("### ℹ️ About")
        st.markdown("🌐 [GitHub Repository](https://github.com/turboflo/horizon-scope)")
        st.markdown(
            "📧 Contact: [florian@hegenbarth.dev](mailto:florian@hegenbarth.dev)"
        )
        st.markdown("👤 Created by: Florian Hegenbarth")


def display_main_content(client: HorizonScopeClient) -> None:
    """Display the main content of the Streamlit application."""
    st.title("✨📑 Horizon Scope")
    st.subheader("Discover similar projects and gain insights")

    # User input form
    with st.form(key="input_form"):
        project_description = st.text_area(
            "✏️ Enter your project description:",
            value=st.session_state.project_description,
            height=150,
            max_chars=1000,
        )

        submit_button = st.form_submit_button("🔍 Search Similar Projects")

    if submit_button:
        clear_comparison_data()  # Clear old comparison data
        st.session_state.project_description = project_description
        st.session_state.searching = True
        st.rerun()

    if st.session_state.get("searching", False):
        if st.session_state.project_description:
            with st.spinner("Searching for similar projects..."):
                search_results = client.search_projects(
                    query=st.session_state.project_description, k=20
                )

            st.header("📊 Search Results")
            for i, project in enumerate(search_results, 1):
                st.divider()
                create_project_card(
                    project, i, client, st.session_state.project_description
                )

        else:
            st.warning("⚠️ Please enter a project description.")
            st.session_state.searching = False


if __name__ == "__main__":
    main()
