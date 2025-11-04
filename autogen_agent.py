"""Autogen assistant agent for document search."""
import os
import warnings
import logging
from typing import Optional
from autogen.agentchat import UserProxyAgent, AssistantAgent

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

        # Configure Autogen
        config_list = [
            {
                "model": "gpt-4",
                "api_key": self.api_key,
            }
        ]

        llm_config = {
            "config_list": config_list,
            "temperature": 0.7,
        }

        # Create assistant agent with document content
        self.assistant = AssistantAgent(
            name="document_search_assistant",
            system_message=f"""You are a document search specialist. Your job is to search through document content and find relevant information to answer questions.

Document Content:
{self.doc_content}

Your task:
1. Carefully analyze the question
2. Search for relevant information in the document above
3. Return ONLY information found in the document
4. If information is not in the document, clearly state: "This information is not found in the document."
5. Be concise and cite specific parts when answering""",
            llm_config=llm_config,
        )

        # Create user proxy agent (non-interactive)
        self.user_proxy = UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,
            code_execution_config=False,
        )

    def search(self, question: str) -> str:
        """
        Search the document and return an answer.

        Args:
            question: The question to search for in the document

        Returns:
            Answer based on document content
        """
        try:
            # Initiate chat to get answer
            self.user_proxy.initiate_chat(
                self.assistant,
                message=question,
                clear_history=False,
                silent=True
            )

            # Get the chat history
            chat_history = self.user_proxy.chat_messages.get(self.assistant, [])

            # Find the last assistant message
            for message in reversed(chat_history):
                if (message.get("name") == "document_search_assistant" or
                    message.get("role") == "assistant"):
                    content = message.get("content", "")
                    if content and content.strip():
                        # Clear history for next search
                        self.user_proxy.clear_history()
                        self.assistant.clear_history()
                        return content

            # Clear history
            self.user_proxy.clear_history()
            self.assistant.clear_history()
            return "No response generated from document search."

        except Exception as e:
            # Clear history even on error
            try:
                self.user_proxy.clear_history()
                self.assistant.clear_history()
            except:
                pass
            return f"Error during document search: {str(e)}"
