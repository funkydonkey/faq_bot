"""Autogen assistant agent for document search."""
import os
import glob
import warnings
import logging
from typing import Optional, List
from pathlib import Path
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

    def __init__(self, docs_dir: str, api_key: Optional[str] = None):
        """
        Initialize the document search agent.

        Args:
            docs_dir: Path to directory containing DOCX files
            api_key: OpenAI API key (optional, reads from env if not provided)
        """
        self.docs_dir = docs_dir
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        # Load all documents from directory
        self.all_documents_content = self._load_all_documents()

        # Create OpenAI model client (v0.6 API)
        self.model_client = OpenAIChatCompletionClient(
            model="gpt-4o",
            api_key=self.api_key,
            temperature=0.7,
        )

        # Create assistant agent with all documents content (v0.6 API)
        self.assistant = AssistantAgent(
            name="document_search_assistant",
            model_client=self.model_client,
            system_message=f"""You are a document search specialist. Your job is to search through multiple documents and find relevant information to answer questions.

Documents Content:
{self.all_documents_content}

Your task:
1. Carefully analyze the question
2. Search for relevant information across ALL documents above
3. When citing information, mention which document it came from
4. Return ONLY information found in the documents
5. If information is not in any document, clearly state: "This information is not found in any of the documents."
6. Be concise and cite specific parts when answering""",
        )

    def _load_all_documents(self) -> str:
        """Load all DOCX files from docs directory."""
        from .docx_reader import DocxReader

        docs_path = Path(self.docs_dir)
        if not docs_path.exists():
            return "No documents directory found."

        docx_files = list(docs_path.glob("*.docx"))
        if not docx_files:
            return "No DOCX files found."

        all_content = []
        for docx_file in docx_files:
            doc_reader = DocxReader(str(docx_file))
            if doc_reader.load():
                content = doc_reader.get_content()
                all_content.append(f"=== DOCUMENT: {docx_file.name} ===\n{content}\n")

        if not all_content:
            return "Failed to load any documents."

        return "\n".join(all_content)

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
