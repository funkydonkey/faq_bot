"""Main application file with Gradio chat interface."""
import os
import glob
import gradio as gr
from dotenv import load_dotenv
from openai_agent import OpenAIAgentRunner

# Load environment variables
load_dotenv()

# Global agent runner instance
agent_runner = None
current_docx_path = None


def initialize_agent():
    """Initialize the agent with the DOCX file from docs folder."""
    global agent_runner, current_docx_path

    try:
        # Look for DOCX files in the docs directory
        docx_files = glob.glob("docs/*.docx")

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
        gr.Markdown(
            """
            # 📄 Document Q&A Bot
            Ask questions about your document!

            **Features:**
            - Auto-loads document from `docs/` folder
            - Uses OpenAI Agents SDK for query processing
            - Intelligent question answering based on document content
            """
        )

        # Document status display
        status_box = gr.Textbox(
            label="📋 Document Status",
            lines=5,
            interactive=False,
            value="Loading document..."
        )

        # Chat interface
        gr.Markdown("### 💬 Chat")
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

        clear_btn.click(
            fn=lambda: ([], clear_chat()),
            outputs=[chatbot]
        )

        gr.Markdown(
            """
            ---
            **Note:**
            - Place your DOCX file in the `docs/` folder
            - Make sure `OPENAI_API_KEY` is set in the `.env` file
            """
        )

        # Load document on startup
        demo.load(
            fn=lambda: initialize_agent()[1],
            outputs=status_box
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

    # Create and launch the interface
    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )


if __name__ == "__main__":
    main()
