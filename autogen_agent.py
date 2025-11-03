"""Autogen assistant agent for document search."""
import os
from typing import Optional, Dict, Any
import autogen
from docx_reader import DocxReader


class DocumentSearchAgent:
    """Autogen-based assistant agent for searching documents."""

    def __init__(self, docx_path: str, api_key: Optional[str] = None):
        """Initialize the document search agent."""
        self.docx_path = docx_path
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.doc_reader = DocxReader(docx_path)
        self.doc_content = ""

        # Load the document
        if self.doc_reader.load():
            self.doc_content = self.doc_reader.get_content()

        # Configure Autogen
        self.config_list = [
            {
                "model": "gpt-4",
                "api_key": self.api_key,
            }
        ]

        self.llm_config = {
            "config_list": self.config_list,
            "temperature": 0.7,
        }

        # Create assistant agent
        self.assistant = autogen.AssistantAgent(
            name="document_assistant",
            system_message=f"""You are a helpful assistant that answers questions based on the content of a document.

Document Content:
{self.doc_content}

Your task is to:
1. Analyze the user's question
2. Search for relevant information in the document content provided above
3. Provide accurate answers based only on the document content
4. If the information is not in the document, clearly state that

Always cite specific parts of the document in your answers.""",
            llm_config=self.llm_config,
        )

        # Create user proxy agent (non-interactive)
        self.user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,
            code_execution_config=False,
        )

    def search_and_answer(self, question: str) -> str:
        """Search the document and answer the question."""
        try:
            # Initiate chat between user proxy and assistant
            chat_result = self.user_proxy.initiate_chat(
                self.assistant,
                message=question,
                clear_history=False,
                silent=True
            )

            # Get the chat history
            chat_history = self.user_proxy.chat_messages.get(self.assistant, [])

            # Find the last message from the assistant (by name)
            for message in reversed(chat_history):
                # Check if it's from the assistant by name or role
                if (message.get("name") == "document_assistant" or
                    message.get("role") == "assistant"):
                    content = message.get("content", "")
                    if content and content.strip():
                        # Clear history for next question
                        self.user_proxy.clear_history()
                        self.assistant.clear_history()
                        return content

            # If we couldn't find a response, try to get it from chat_result
            if hasattr(chat_result, 'summary') and chat_result.summary:
                return chat_result.summary

            # Clear history for next question
            self.user_proxy.clear_history()
            self.assistant.clear_history()
            return "No response generated."

        except Exception as e:
            # Clear history even on error
            try:
                self.user_proxy.clear_history()
                self.assistant.clear_history()
            except:
                pass
            return f"Error processing question: {str(e)}"

    def get_document_summary(self) -> str:
        """Get a brief summary of the document."""
        if not self.doc_content:
            return "No document loaded."

        # Return first 500 characters as preview
        preview = self.doc_content[:500]
        total_chars = len(self.doc_content)
        return f"{preview}...\n\n[Total document length: {total_chars} characters]"
