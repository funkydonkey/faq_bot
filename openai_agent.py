"""OpenAI Agents SDK integration for the FAQ bot."""
import os
from typing import Optional, List, Dict
from openai import OpenAI
from autogen_agent import DocumentSearchAgent


class OpenAIAgentRunner:
    """OpenAI Agents SDK runner that orchestrates the document search."""

    def __init__(self, docx_path: str, api_key: Optional[str] = None):
        """Initialize the OpenAI agent runner."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.docx_path = docx_path

        # Initialize the Autogen document search agent
        self.doc_agent = DocumentSearchAgent(docx_path, api_key)

        # Conversation history
        self.conversation_history: List[Dict[str, str]] = []

    def process_query(self, user_question: str) -> str:
        """
        Process a user query using the OpenAI agent.

        This method:
        1. Takes the user question
        2. Uses the Autogen assistant to search the document
        3. Returns the answer
        """
        try:
            # Add user question to history
            self.conversation_history.append({
                "role": "user",
                "content": user_question
            })

            # Use Autogen agent to search and answer
            answer = self.doc_agent.search_and_answer(user_question)

            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": answer
            })

            return answer

        except Exception as e:
            error_msg = f"Error processing query: {str(e)}"
            self.conversation_history.append({
                "role": "assistant",
                "content": error_msg
            })
            return error_msg

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the conversation history."""
        return self.conversation_history

    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def get_document_info(self) -> str:
        """Get information about the loaded document."""
        return self.doc_agent.get_document_summary()
