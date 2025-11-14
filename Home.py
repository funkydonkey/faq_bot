"""Home page for FAQ Bot multi-page Streamlit application."""
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="FAQ Bot - Home",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    /* Buttons */
    .stButton > button {
        background-color: #4A90E2 !important;
        border-color: #4A90E2 !important;
        color: white !important;
    }

    .stButton > button:hover {
        background-color: #357ABD !important;
        border-color: #357ABD !important;
    }

    /* Feature cards */
    .feature-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin-bottom: 1rem;
        border-left: 4px solid #4A90E2;
    }

    .feature-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #2C3E50;
        margin-bottom: 0.5rem;
    }

    .feature-desc {
        color: #7F8C8D;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    """Main home page."""

    # Header
    st.title("💬 FAQ Bot")
    st.markdown("### AI-Powered Document Q&A with Knowledge Graph Visualization")

    st.divider()

    # Introduction
    st.markdown("""
    Welcome to **FAQ Bot** - an intelligent document assistant that uses advanced AI agents
    to answer questions about your documents and visualize the knowledge they contain.
    """)

    st.markdown("<br>", unsafe_allow_html=True)

    # Features
    st.header("🚀 Features")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">💬 Intelligent Chat</div>
            <div class="feature-desc">
                Ask questions in natural language and get accurate answers extracted from your documents.
                Powered by OpenAI GPT-4o with multi-agent orchestration.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🧠 Multi-Agent Architecture</div>
            <div class="feature-desc">
                Uses three specialized agents: an orchestrator, a clarification agent for entity extraction,
                and a document search agent with hybrid retrieval strategies.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🕸️ Knowledge Graph</div>
            <div class="feature-desc">
                Interactive visualization of entities and relationships extracted from your documents.
                Explore concepts, people, organizations, and their connections.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">💾 Persistent Memory</div>
            <div class="feature-desc">
                Conversation history is saved in SQLite, allowing you to continue conversations
                across sessions while maintaining context.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick Start
    st.header("🎯 Quick Start")

    st.markdown("""
    1. **📁 Add Documents**: Place your `.docx` files in the `docs/` folder
    2. **🔄 Index Documents**: Run `python -m src.indexing` to create the knowledge base
    3. **💬 Start Chatting**: Navigate to the **Chat** page to ask questions
    4. **🕸️ Explore Graph**: Visit the **Knowledge Graph** page to visualize relationships
    """)

    st.divider()

    # Navigation
    st.header("📍 Navigation")

    nav_col1, nav_col2 = st.columns(2)

    with nav_col1:
        if st.button("💬 Go to Chat", use_container_width=True):
            st.switch_page("pages/1_💬_Chat.py")

    with nav_col2:
        if st.button("🕸️ Go to Knowledge Graph", use_container_width=True):
            st.switch_page("pages/2_🕸️_Knowledge_Graph.py")

    st.markdown("<br>", unsafe_allow_html=True)

    # Technology Stack
    with st.expander("⚙️ Technology Stack"):
        st.markdown("""
        **AI & ML:**
        - OpenAI GPT-4o (orchestration, search)
        - OpenAI GPT-4o-mini (cost-efficient indexing)
        - OpenAI Agents SDK (agent framework)
        - AutoGen v0.6 (multi-agent coordination)
        - MiniRAG (knowledge graph RAG)

        **Data & Storage:**
        - SQLite (conversation history)
        - Vector embeddings (semantic search)
        - GraphML (knowledge graph storage)

        **UI & Visualization:**
        - Streamlit (web interface)
        - streamlit-agraph (interactive graph visualization)
        - Custom CSS styling
        """)

    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.caption("Built with ❤️ using OpenAI, AutoGen, MiniRAG, and Streamlit")


if __name__ == "__main__":
    main()
