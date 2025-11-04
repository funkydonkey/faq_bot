"""OpenAI Agents SDK integration for the FAQ bot."""
import os
from typing import Optional, List, Dict
import asyncio
from agents import Agent, Runner, trace, function_tool
from docx_reader import DocxReader
from autogen_agent import DocumentSearchAgent


def create_orchestrator_agent(search_agent: DocumentSearchAgent) -> Agent:
    """
    Create an OpenAI Agents SDK orchestrator agent.

    This agent evaluates questions and decides when to search the document.

    Args:
        search_agent: The AutoGen document search agent to use as a tool

    Returns:
        Configured Agent instance
    """
    # Define the document search tool
    @function_tool
    def search_document(question: str) -> str:
        """
        Search the document for information to answer a question.

        Args:
            question: The question to search for in the document

        Returns:
            Answer from the document
        """
        return search_agent.search(question)

    # Create orchestrator agent with tool
    instructions = """You are a helpful assistant that answers questions about a document.

Your task is to:
1. Evaluate the user's question
2. When you need to find information in the document, use the search_document tool
3. Provide clear and helpful answers based on what you find
4. If the document doesn't contain the information, politely inform the user

Always be concise and accurate."""

    agent = Agent(
        name="document_orchestrator",
        model="gpt-4o",
        instructions=instructions,
        tools=[search_document]
    )

    return agent


class OpenAIAgentRunner:
    """Runner that orchestrates the OpenAI Agents SDK agent with tracing."""

    def __init__(self, docx_path: str, api_key: Optional[str] = None):
        """
        Initialize the agent runner.

        Args:
            docx_path: Path to the DOCX file
            api_key: OpenAI API key (optional, reads from env if not provided)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.docx_path = docx_path

        # Set OpenAI API key for agents SDK
        if self.api_key:
            from agents import set_default_openai_key
            set_default_openai_key(self.api_key)

        # Load document content
        self.doc_reader = DocxReader(docx_path)
        if self.doc_reader.load():
            self.doc_content = self.doc_reader.get_content()
        else:
            self.doc_content = ""

        # Create the AutoGen document search agent
        self.search_agent = DocumentSearchAgent(
            doc_content=self.doc_content,
            api_key=self.api_key
        )

        # Create the OpenAI orchestrator agent with search tool
        self.agent = create_orchestrator_agent(self.search_agent)

        # Conversation history (for compatibility with existing interface)
        self.conversation_history: List[Dict[str, str]] = []

    async def _process_query_async(self, user_question: str) -> str:
        """
        Process a user query asynchronously using the OpenAI Agents SDK.

        Uses trace context manager for observability.
        """
        try:
            # Run the agent with the user's question wrapped in trace
            with trace("document_qa_agent_call"):
                result = await Runner.run(self.agent, user_question)

            return result.final_output

        except Exception as e:
            return f"Error processing question: {str(e)}"

    def process_query(self, user_question: str) -> str:
        """
        Process a user query using the OpenAI Agents SDK (sync wrapper).

        Uses trace context manager for observability.
        """
        try:
            # Add to history
            self.conversation_history.append({
                "role": "user",
                "content": user_question
            })

            # Get or create event loop
            try:
                loop = asyncio.get_event_loop()
                if loop.is_closed():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            # Run the async query (trace is already inside _process_query_async)
            response = loop.run_until_complete(
                self._process_query_async(user_question)
            )

            # Add response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })

            return response

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
        if not self.doc_content:
            return "No document loaded."

        # Return first 500 characters as preview
        preview = self.doc_content[:500]
        total_chars = len(self.doc_content)
        return f"{preview}...\n\n[Total document length: {total_chars} characters]"
