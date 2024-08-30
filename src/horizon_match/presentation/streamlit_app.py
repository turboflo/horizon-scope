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


def start_comparison():
    st.session_state.comparing = True
    st.session_state.results = None


def main():
    st.set_page_config(
        page_title="Horizon Match", layout="wide", initial_sidebar_state="expanded"
    )
    initialize_session_state()

    # Sidebar
    with st.sidebar:
        st.markdown("### ℹ️ About")
        st.markdown("🌐 [GitHub Repository](https://github.com/turboflo/horizon-match)")
        st.markdown("👤 Created by: Florian Hegenbarth")
        st.markdown(
            "📧 Contact: [florian@hegenbarth.dev](mailto:florian@hegenbarth.dev)"
        )

    st.title("✨ Horizon Match")
    st.subheader("Discover similar projects and gain insights")

    # Initialize client
    config_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "config.yml"
    )
    client = HorizonMatchClient.from_config(config_path)

    # User input form
    with st.form(key="input_form"):
        project_description = st.text_area(
            "✏️ Enter your project description:",
            value=st.session_state.project_description,
            height=150,
            max_chars=500,
        )

        k = st.number_input(
            "🔢 Number of projects to compare:",
            min_value=1,
            max_value=5,
            value=st.session_state.k,
            step=1,
        )

        submit_button = st.form_submit_button("🔍 Compare Projects")

    if submit_button:
        st.session_state.project_description = project_description
        st.session_state.k = k
        start_comparison()

    if st.session_state.comparing:
        if st.session_state.project_description:
            if st.session_state.results is None:
                with st.spinner("Analyzing your project..."):
                    st.session_state.results = client.match(
                        query=st.session_state.project_description, k=st.session_state.k
                    )

            st.header("📊 Comparison Results")
            for i, result in enumerate(st.session_state.results, 1):
                with st.expander(
                    f"#{i}: {result.project.title or 'Untitled Project'}", expanded=True
                ):
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.metric(
                            "🤖 AI Similarity", f"{result.comaprison.score*100:.1f}%"
                        )
                    with col2:
                        st.metric(
                            "📐 Cosine Similarity",
                            (
                                f"{result.project.similarity*100:.1f}%"
                                if result.project.similarity is not None
                                else "N/A"
                            ),
                        )

                    if f"show_desc_{i}" not in st.session_state:
                        st.session_state[f"show_desc_{i}"] = False

                    # Dynamic button text based on current state
                    button_text = (
                        "Hide Original Description"
                        if st.session_state[f"show_desc_{i}"]
                        else "View Original Description"
                    )

                    if st.button(button_text, key=f"toggle_{i}"):
                        st.session_state[f"show_desc_{i}"] = not st.session_state[
                            f"show_desc_{i}"
                        ]

                    if st.session_state[f"show_desc_{i}"]:
                        st.write(result.project.description)

                    if st.session_state.get(f"show_desc_{i}", False):
                        st.write(result.project.description)

                    st.subheader("📝 Summary")
                    st.write(result.comaprison.summary)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("✅ Similarities")
                        st.write(result.comaprison.similarity)
                    with col2:
                        st.subheader("❌ Differences")
                        st.write(result.comaprison.difference)

                    st.subheader("🧐 Analysis")
                    st.write(result.comaprison.reason)

                    # Project ID and creation date in small text
                    st.caption(
                        f"Project ID: {result.project.id} | Created: {result.project.created_at or 'Date not available'}"
                    )
        else:
            st.warning("⚠️ Please enter a project description.")
            st.session_state.comparing = False


if __name__ == "__main__":
    main()
