"""Autogen assistant agent for document search."""
import os
import warnings
import logging
from typing import Optional
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Suppress FLAML warning
warnings.filterwarnings('ignore', message='.*flaml.automl.*')

# Suppress AutoGen API key format warnings
logging.getLogger('autogen.oai.client').setLevel(logging.ERROR)


class DocumentSearchAgent:
    """Autogen-based assistant agent for searching documents."""

    def __init__(self, doc_content: str, api_key: Optional[str] = None):
        """
        Initialize the document search agent.

        Args:
            doc_content: The full document content to search in
            api_key: OpenAI API key (optional, reads from env if not provided)
        """
        self.doc_content = doc_content
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        # Create OpenAI model client (v0.6 API)
        self.model_client = OpenAIChatCompletionClient(
            model="gpt-4o",
            api_key=self.api_key,
            temperature=0.7,
        )

        # Create assistant agent with document content (v0.6 API)
        self.assistant = AssistantAgent(
            name="document_search_assistant",
            model_client=self.model_client,
            system_message=f"""You are a document search specialist. Your job is to search through document content and find relevant information to answer questions.

Document Content:
{self.doc_content}

Your task:
1. Carefully analyze the question
2. Search for relevant information in the document above
3. Return ONLY information found in the document
4. If information is not in the document, clearly state: "This information is not found in the document."
5. Be concise and cite specific parts when answering""",
        )

    async def search(self, question: str) -> str:
        """
        Search the document and return an answer.

        Args:
            question: The question to search for in the document

        Returns:
            Answer based on document content
        """
        try:
            # Use on_messages method (v0.6 API)
            response = await self.assistant.on_messages(
                [TextMessage(content=question, source="user")],
                CancellationToken()
            )

            # Extract response content
            if response.chat_message:
                content = response.chat_message.content
                if isinstance(content, str) and content.strip():
                    return content

            return "No response generated from document search."

        except Exception as e:
            return f"Error during document search: {str(e)}"
