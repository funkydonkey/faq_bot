"""Streamlit interface for FAQ Bot."""
import os
import sys
import warnings
import logging
import glob
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

# Add current directory (src) and parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)

# Suppress warnings before importing autogen-related modules
warnings.filterwarnings('ignore', message='.*flaml.automl.*')
logging.getLogger('autogen.oai.client').setLevel(logging.ERROR)

# Import from src package
from src.openai_agent import OpenAIAgentRunner

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'agent_runner' not in st.session_state:
        st.session_state.agent_runner = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'document_loaded' not in st.session_state:
        st.session_state.document_loaded = False


def get_docs_directory():
    """Get the docs directory path."""
    project_root = Path(__file__).parent.parent
    return project_root / "docs"


def get_available_documents():
    """Get list of available DOCX files in docs directory."""
    docs_dir = get_docs_directory()
    if not docs_dir.exists():
        return []
    return list(docs_dir.glob("*.docx"))


def load_all_documents():
    """Load all documents from docs directory and initialize the agent."""
    try:
        # Get docs directory
        docs_dir = get_docs_directory()

        # Initialize the agent runner with docs directory
        agent_runner = OpenAIAgentRunner(docs_dir=str(docs_dir))

        # Get document info
        doc_info = agent_runner.get_document_info()

        # Update session state
        st.session_state.agent_runner = agent_runner
        st.session_state.document_loaded = True
        st.session_state.messages = []  # Clear chat history on reload

        return True, doc_info
    except Exception as e:
        return False, str(e)


def clear_chat_history():
    """Clear the chat history."""
    st.session_state.messages = []
    if st.session_state.agent_runner:
        st.session_state.agent_runner.clear_history()


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="FAQ Bot",
        page_icon="💬",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for colors and layout
    st.markdown("""
        <style>
        /* Chat input - single blue border */
        .stChatInput > div {
            border: 1px solid #4A90E2 !important;
        }

        .stChatInput > div:hover,
        .stChatInput > div:focus-within {
            border: 1px solid #4A90E2 !important;
            box-shadow: 1px 1px 1px 1px #4A90E2 !important;
            outline: none !important;
        }

        /* User avatar background - bright blue */
        [data-testid="stChatMessageAvatarUser"] {
            background-color: #4A90E2 !important;
        }

        /* Assistant avatar background - bright purple */
        [data-testid="stChatMessageAvatarAssistant"] {
            background-color: #9B59B6 !important;
        }

        /* User messages - align right */
        div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
            flex-direction: row-reverse !important;
        }

        div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) .stMarkdown {
            text-align: right !important;
        }

        /* Assistant messages - align left (default) */
        div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
            flex-direction: row !important;
        }

        div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) .stMarkdown {
            text-align: left !important;
        }

        /* Primary buttons - bright blue */
        .stButton > button {
            background-color: #4A90E2 !important;
            border-color: #4A90E2 !important;
            color: white !important;
        }

        .stButton > button:hover {
            background-color: #357ABD !important;
            border-color: #357ABD !important;
        }

        /* Links - bright purple */
        a {
            color: #9B59B6 !important;
        }

        /* Spinner - blue */
        .stSpinner > div {
            border-top-color: #4A90E2 !important;
        }

        /* Clear button - fixed position aligned with chat input */
        [data-testid="column"]:last-child button {
            position: fixed !important;
            bottom: 20px !important;
            # right: 20px !important;
            z-index: 1001 !important;
            height: 50px !important;
            margin-left: 50px !important;
            width: 50px !important;
            padding: 0 !important;
            border-radius: 50% !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    initialize_session_state()

    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("⚠️ OPENAI_API_KEY not found in environment variables.")
        st.info("Please create a .env file with your OpenAI API key.\nExample: OPENAI_API_KEY=sk-...")
        st.stop()

    # Auto-load all documents if none loaded
    if not st.session_state.document_loaded:
        available_docs = get_available_documents()
        if available_docs:
            with st.spinner("Loading all documents..."):
                success, message = load_all_documents()
                if success:
                    st.rerun()
        else:
            st.warning("No DOCX files found in the 'docs' folder.")
            st.info("Please add .docx files to the docs directory.")
            st.stop()

    # Sidebar
    # with st.sidebar:
    #     st.title("💬 FAQ Bot")

    #     # Clear chat button
    #     if st.button("🗑️ Clear Chat", use_container_width=True):
    #         clear_chat_history()
    #         st.rerun()

    #     # Stats
    #     if st.session_state.messages:
    #         st.divider()
    #         st.caption(f"💬 Messages: {len(st.session_state.messages)}")

    # Main chat interface
    # st.markdown("<br>", unsafe_allow_html=True)
    st.title("💬 FAQ Bot")
    st.caption("Ask questions about your documents")
    # st.markdown("<br>", unsafe_allow_html=True)
    # st.markdown("<br>", unsafe_allow_html=True)

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input (always stays at bottom)
    if prompt := st.chat_input("Type your question here..."):
        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get assistant response
        try:
            response = st.session_state.agent_runner.process_query(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

        # Rerun to display new messages
        st.rerun()

    # Clear button - positioned with CSS
    _, col_button = st.columns([18, 1])
    with col_button:
        if st.button("🗑️", key="clear_btn", help="Clear chat history"):
            clear_chat_history()
            st.rerun()



if __name__ == "__main__":
    main()
