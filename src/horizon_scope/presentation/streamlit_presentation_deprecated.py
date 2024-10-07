from horizon_scope.infrastructure.config.config_manager import ConfigManager
import streamlit as st
from horizon_scope.presentation.horizon_scope_client import HorizonScopeClient
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


def toggle_description(i):
    st.session_state[f"show_desc_{i}"] = not st.session_state.get(
        f"show_desc_{i}", False
    )


def main():
    st.set_page_config(
        page_title="Horizon Scope", layout="wide", initial_sidebar_state="collapsed"
    )
    initialize_session_state()

    # Initialize config
    config_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "config.yml"
    )
    config_manager = ConfigManager(config_path)

    # Check if OpenAI API key is set
    if not config_manager.is_openai_api_key_set():
        st.warning("OpenAI API key not found. Please enter it below.")
        api_key = st.text_input("OpenAI API key:", type="password")
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            st.success("API key set. Please reload the page.")

            st.rerun()
        else:
            # st.error("Please enter an API key.")
            st.stop()

    # Initialize client
    client = HorizonScopeClient.from_config(config_path)

    # Sidebar
    with st.sidebar:
        st.markdown("### ℹ️ About")
        st.markdown("🌐 [GitHub Repository](https://github.com/turboflo/horizon-scope)")
        st.markdown(
            "📧 Contact: [florian@hegenbarth.dev](mailto:florian@hegenbarth.dev)"
        )
        st.markdown("👤 Created by: Florian Hegenbarth")

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
        st.rerun()

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
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col1:
                        st.metric(
                            "🤖 AI Similarity", f"{result.comparison.score*100:.1f}%"
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
                    with col3:
                        st.metric(
                            "🔒 Confidence", f"{result.comparison.confidence*100:.1f}%"
                        )

                    # Dynamic button text based on current state
                    button_text = (
                        "Hide Original Description"
                        if st.session_state.get(f"show_desc_{i}", False)
                        else "View Original Description"
                    )

                    if st.button(
                        button_text,
                        key=f"toggle_{i}",
                        on_click=toggle_description,
                        args=(i,),
                    ):
                        pass

                    if st.session_state.get(f"show_desc_{i}", False):
                        st.write(result.project.description)

                    st.subheader("📝 Summary")
                    st.write(result.comparison.summary)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("✅ Similarities")
                        st.write(result.comparison.similarity)
                    with col2:
                        st.subheader("❌ Differences")
                        st.write(result.comparison.difference)

                    st.subheader("🧐 Analysis")
                    st.write(result.comparison.reason)

                    # Project ID and creation date in small text
                    st.caption(
                        f"Project ID: {result.project.id} | Content Update: {result.project.content_update_date or 'Date not available'}"
                    )
        else:
            st.warning("⚠️ Please enter a project description.")
            st.session_state.comparing = False


if __name__ == "__main__":
    main()
