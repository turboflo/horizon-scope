import streamlit as st
from horizon_match.presentation.horizon_match_client import HorizonMatchClient
import os


def initialize_session_state():
    if "comparing" not in st.session_state:
        st.session_state.comparing = False
    if "results" not in st.session_state:
        st.session_state.results = None
    if "project_description" not in st.session_state:
        st.session_state.project_description = ""
    if "k" not in st.session_state:
        st.session_state.k = 3
    if "model" not in st.session_state:
        st.session_state.model = "gpt-4o-mini"


def start_comparison():
    st.session_state.comparing = True
    st.session_state.results = None


def main():
    st.set_page_config(
        page_title="Horizon Match", layout="wide", initial_sidebar_state="collapsed"
    )
    initialize_session_state()

    st.title("Horizon Match")
    st.subheader("Discover similar projects and gain insights")

    # Initialize client
    config_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "config.yml"
    )
    client = HorizonMatchClient.from_config(config_path)

    # User input form
    with st.form(key="input_form"):
        project_description = st.text_area(
            "Enter your project description:",
            value=st.session_state.project_description,
            height=150,
            max_chars=500,
        )

        col1, col2 = st.columns(2)
        with col1:
            k = st.slider(
                "Number of projects to compare:",
                min_value=1,
                max_value=5,
                value=st.session_state.k,
            )

        with col2:
            model = st.selectbox(
                "Select model:",
                options=["gpt-4o-mini", "gpt-4o"],
                index=0,  # Default to gpt-4o-mini
                key="model_select",
                disabled=True,  # Make the dropdown non-editable
            )

        submit_button = st.form_submit_button("Compare Projects")

    if submit_button:
        st.session_state.project_description = project_description
        st.session_state.k = k
        st.session_state.model = model
        start_comparison()

    if st.session_state.comparing:
        if st.session_state.project_description:
            if st.session_state.results is None:
                with st.spinner("Analyzing your project..."):
                    # Update client configuration with selected model
                    client.config.config["horizon-match"]["comparison-service"][
                        "model"
                    ] = st.session_state.model
                    st.session_state.results = client.match(
                        query=st.session_state.project_description, k=st.session_state.k
                    )

            st.header("Comparison Results")
            for i, result in enumerate(st.session_state.results, 1):
                with st.expander(
                    f"#{i}: {result.project.title or 'Untitled Project'}", expanded=True
                ):
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.metric(
                            "AI Similarity", f"{result.comaprison.score*100:.1f}%"
                        )
                    with col2:
                        st.metric(
                            "Cosine Similarity",
                            (
                                f"{result.project.similarity*100:.1f}%"
                                if result.project.similarity is not None
                                else "N/A"
                            ),
                        )

                    if st.checkbox(
                        "Show Project Description", key=f"desc_{i}", value=False
                    ):
                        st.write(result.project.description)

                    st.subheader("Summary")
                    st.write(result.comaprison.summary)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("Similarities")
                        st.write(result.comaprison.similarity)
                    with col2:
                        st.subheader("Differences")
                        st.write(result.comaprison.difference)

                    st.subheader("Analysis")
                    st.write(result.comaprison.reason)

                    # Project ID and creation date in small text
                    st.caption(
                        f"Project ID: {result.project.id} | Created: {result.project.created_at or 'Date not available'}"
                    )
        else:
            st.warning("Please enter a project description.")
            st.session_state.comparing = False


if __name__ == "__main__":
    main()
