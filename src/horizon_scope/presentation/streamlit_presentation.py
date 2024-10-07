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


def create_project_card(project, index, client, user_project_description):
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.metric("Similarity", f"{project.similarity*100:.1f}%")

    with col2:
        st.subheader(project.title or "Untitled Project")
        st.caption(
            f"Project ID: {project.id} | Updated: {project.content_update_date or 'Date not available'}"
        )

    with col3:
        st.link_button(
            "🔗 View on CORDIS", f"https://cordis.europa.eu/project/id/{project.id}"
        )
        if st.button("🤖 AI Compare", key=f"compare_button_{index}"):
            st.session_state[f"show_comparison_{index}"] = True

    if st.session_state.get(f"show_comparison_{index}", False):
        with st.expander("Comparison Results", expanded=True):
            if f"comparison_{index}" not in st.session_state:
                with st.spinner("Analyzing projects..."):
                    comparison = client.compare_projects(
                        user_project_description,
                        project.description,
                    )
                st.session_state[f"comparison_{index}"] = comparison
            else:
                comparison = st.session_state[f"comparison_{index}"]

            col1, col2 = st.columns(2)
            with col1:
                st.metric("🤖 AI Similarity", f"{comparison.score*100:.1f}%")
            with col2:
                st.metric("🔒 Confidence", f"{comparison.confidence*100:.1f}%")

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

        submit_button = st.form_submit_button("🔍 Search Similar Projects")

    if submit_button:
        st.session_state.project_description = project_description
        st.session_state.k = k
        st.session_state.searching = True
        st.rerun()

    if st.session_state.get("searching", False):
        if st.session_state.project_description:
            with st.spinner("Searching for similar projects..."):
                search_results = client.search_projects(
                    query=st.session_state.project_description, k=st.session_state.k
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


if __name__ == "__main__":
    main()
