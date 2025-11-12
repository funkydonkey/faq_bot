"""Main application file with Gradio chat interface."""
import os
import sys
import warnings
import logging
import glob
import gradio as gr
from dotenv import load_dotenv
from agents import trace

# Add parent directory to path to import from src
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Suppress warnings before importing autogen-related modules
warnings.filterwarnings('ignore', message='.*flaml.automl.*')
logging.getLogger('autogen.oai.client').setLevel(logging.ERROR)

from .openai_agent import OpenAIAgentRunner

# Load environment variables from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Global agent runner instance
agent_runner = None
current_docx_path = None


def initialize_agent():
    """Initialize the agent with the DOCX file from docs folder."""
    global agent_runner, current_docx_path

    try:
        # Get project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        docs_dir = os.path.join(project_root, "docs")

        # Look for DOCX files in the docs directory
        docx_files = glob.glob(os.path.join(docs_dir, "*.docx"))

        if not docx_files:
            return None, "❌ No DOCX file found in the 'docs' folder. Please add a .docx file to the docs directory."

        # Use the first DOCX file found
        file_path = docx_files[0]

        # Initialize the agent runner
        agent_runner = OpenAIAgentRunner(docx_path=file_path)
        current_docx_path = file_path

        # Get document info
        doc_info = agent_runner.get_document_info()

        doc_name = os.path.basename(file_path)
        return agent_runner, f"✅ **Document loaded:** {doc_name}\n\n**Preview:**\n{doc_info}"

    except Exception as e:
        return None, f"❌ Error loading document: {str(e)}"


def chat_callback(message, history):
    """
    Chat callback function that processes user messages.

    Args:
        message: The user's message
        history: The chat history

    Returns:
        The assistant's response
    """
    global agent_runner

    if agent_runner is None:
        return "❌ Document not loaded. Please make sure there's a .docx file in the 'docs' folder and restart the app."

    if not message or message.strip() == "":
        return "Please enter a question."

    try:
        # Process the query using the OpenAI agent runner
        response = agent_runner.process_query(message)
        return response

    except Exception as e:
        return f"❌ Error processing your question: {str(e)}"


def clear_chat():
    """Clear the chat history."""
    global agent_runner
    if agent_runner:
        agent_runner.clear_history()
    return None


def create_interface():
    """Create the Gradio interface."""

    with gr.Blocks(title="Document Q&A Bot", theme=gr.themes.Soft()) as demo:
        # Clean chat interface
        chatbot = gr.Chatbot(
            label="Conversation",
            height=500,
            type="messages"
        )
        msg = gr.Textbox(
            label="Your Question",
            placeholder="Type your question here...",
            lines=2
        )
        with gr.Row():
            submit_btn = gr.Button("Send", variant="primary")
            clear_btn = gr.Button("Clear Chat")

        # Handle message submission
        def respond(message, chat_history):
            if not message:
                return chat_history, ""

            # Add user message to history
            chat_history.append({"role": "user", "content": message})

            # Get bot response
            bot_response = chat_callback(message, chat_history)

            # Add bot response to history
            chat_history.append({"role": "assistant", "content": bot_response})

            return chat_history, ""

        submit_btn.click(
            fn=respond,
            inputs=[msg, chatbot],
            outputs=[chatbot, msg]
        )

        msg.submit(
            fn=respond,
            inputs=[msg, chatbot],
            outputs=[chatbot, msg]
        )

        def clear_chat_handler():
            """Clear chat and return empty message list."""
            clear_chat()
            return []

        clear_btn.click(
            fn=clear_chat_handler,
            outputs=[chatbot]
        )

    return demo


def main():
    """Main function to run the application."""
    # Check if API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("WARNING: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key.")
        print("Example: OPENAI_API_KEY=sk-...")

    # Initialize agent on startup
    print("\n" + "="*60)
    print("Initializing FAQ Bot...")
    print("="*60)
    agent, status = initialize_agent()
    if agent:
        print("✅ Agent initialized successfully")
    else:
        print(f"⚠️  {status}")
    print("="*60 + "\n")

    # Create and launch the interface
    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=8080,
        share=False
    )


if __name__ == "__main__":
    main()
