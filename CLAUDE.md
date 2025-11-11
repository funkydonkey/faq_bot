# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FAQ Bot is a document Q&A system with a Gradio chat interface. It uses a **three-layer agent architecture**: an OpenAI Agents SDK orchestrator, a clarification agent for entity extraction, and an AutoGen search agent for document retrieval. The system supports multiple document formats (DOCX, DOC, TXT) with cost-optimized indexing.

## Requirements

- **Python 3.12** (required for AutoGen compatibility)
- OpenAI API key

## Common Commands

```bash
# Setup
python3.12 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
echo "OPENAI_API_KEY=your-key-here" > .env

# Run the Gradio app
python app.py
# Access at http://localhost:8080

# Test MiniRAG knowledge graph query
python test.py

# Index all documents from docs/ (DOCX, DOC, TXT)
python indexing.py

# Preview files to be indexed
python demo_indexing.py

# Visualize knowledge graph
python graph.py
```

## Architecture

### Three-Layer Agent Design

**Flow**: User → Gradio UI → OpenAI Orchestrator → [Clarification Agent | AutoGen Search Agent] → Document

1. **OpenAI Orchestrator** (`openai_agent.py`):
   - Entry point for all queries (uses GPT-4o)
   - Wraps calls in `trace("document_qa_agent_call")` for observability
   - Exposes two tools: `search_document()` and `run_clarification_agent()` as `@function_tool`
   - Manages persistent conversation history via SQLite session
   - Handles async/await with proper event loop management (`openai_agent.py:149-162`)

2. **Clarification Agent** (`clarification_agent.py`):
   - Extracts entities from ambiguous user queries using MiniRAG (uses GPT-4o)
   - Called by orchestrator when user query needs context clarification
   - **Hybrid search strategy**:
     - Primary: "mini" mode with LLM-based entity extraction (`clarification_agent.py:88-97`)
     - Fallback: Direct vector search on entity descriptions when mini mode returns empty (`clarification_agent.py:113-116`)
   - Configured with `cosine_better_than_threshold=0.0` for maximum recall (`clarification_agent.py:43`)
   - Returns structured `ClarificationContext` with entity list, scores, and descriptions

3. **AutoGen Search Agent** (`autogen_agent.py`):
   - Called as a tool by the OpenAI orchestrator
   - Uses AutoGen v0.6 API with `AssistantAgent` and `OpenAIChatCompletionClient`
   - Receives `doc_content` as parameter (no duplicate loading)
   - No explicit `max_consecutive_auto_reply` in v0.6 API (agent responds once via `on_messages`)
   - Returns direct answers from document content via `response.chat_message.content` (`autogen_agent.py:74-77`)

### Key Components

**Core Application:**
- **app.py**: Gradio interface with chat UI, auto-loads first DOCX from `docs/` on startup
- **openai_agent.py**: `OpenAIAgentRunner` class - manages orchestrator, SQLite session, and conversation history
- **clarification_agent.py**: Entity extraction agent with hybrid search (mini mode + fallback)
- **autogen_agent.py**: `DocumentSearchAgent` class - focused document search tool using AutoGen v0.6

**Document Processing:**
- **docx_reader.py**: `DocxReader` class - extracts text from DOCX including tables
- **indexing.py**: Multi-format document indexing (DOCX, DOC, TXT) with cost-efficient gpt-4o-mini

**Utilities & Testing:**
- **demo_indexing.py**: Preview files to be indexed without running full indexing
- **graph.py**: Knowledge graph visualization using NetworkX
- **test.py**: Standalone MiniRAG query test
- **test_hybrid.py**: Hybrid search strategy testing
- **test_threshold.py**: Vector similarity threshold testing
- **debug_mini.py**: Debug tool for mini mode entity extraction
- **setup_fix.sh**: Setup helper script for environment configuration

**Data Storage:**
- **conversation_history.db**: SQLite database for persistent conversation sessions
- **kb/**: MiniRAG knowledge base storage directory (auto-generated)
- **docs/**: Document source directory (DOCX, DOC, TXT files)

### MiniRAG Integration

- **Location**: `MiniRAG/` subdirectory (vendored dependency)
- **Storage**: Knowledge base persisted in `kb/` directory
- **Indexing**: Documents split into chunks using `RecursiveCharacterTextSplitter` (500 chars, 200 overlap)
- **Embedding**: OpenAI `text-embedding-3-small` (1536 dimensions, most cost-efficient)
- **LLM Models**:
  - **Indexing**: `gpt-4o-mini` for cost efficiency (15x cheaper than gpt-4o)
  - **Runtime**: `gpt-4o` for clarification and document search (best quality)
- **Supported Formats**: DOCX, DOC, TXT with automatic format detection
- **Vector Search**: Threshold set to 0.0 for maximum recall with fallback strategy

## Important Implementation Details

### SQLite Conversation Persistence
- **Feature**: Persistent conversation history across sessions using SQLite (`conversation_history.db`)
- **Implementation**: `openai_agent.py:107-110` creates `SQLiteSession` with session_id="faq_conversation"
- **Usage**: Session passed to `Runner.run()` at `openai_agent.py:128` to maintain context
- **Clear History**: `clear_history()` method clears both in-memory and SQLite session (`openai_agent.py:210-197`)

### Warning Suppression
`app.py:10-12` suppresses FLAML and AutoGen warnings at module level before imports:
```python
warnings.filterwarnings('ignore', message='.*flaml.automl.*')
logging.getLogger('autogen.oai.client').setLevel(logging.ERROR)
```

### Event Loop Handling
`openai_agent.py:149-162` handles event loop creation/reuse for async operations in sync context (required for Gradio callbacks).

### Document Loading
- Documents load from `docs/` directory automatically (DOCX, DOC, TXT supported)
- First DOCX file found is used (`app.py:30-36`)
- Single document loading - no duplicate `get_document_summary()` methods
- Multi-format support: DOCX/DOC via python-docx, TXT with UTF-8/Latin-1 fallback

### AutoGen v0.6 API
- **New API**: Uses `AssistantAgent` with `on_messages()` method instead of legacy `generate_reply()`
- **Model Client**: `OpenAIChatCompletionClient` replaces old configuration format
- **Single Response**: Agent responds once per `on_messages()` call, no need for `max_consecutive_auto_reply`
- **Response Format**: Extract content via `response.chat_message.content` (`autogen_agent.py:74-77`)

## Cost Optimization

- **Indexing** uses `gpt-4o-mini` (94% cost savings vs gpt-4o)
- **Runtime** uses `gpt-4o` for best quality on user-facing queries
- **Embeddings** use `text-embedding-3-small` (6.5x cheaper than large)
- **Token limits**: `entity_extract_max_gleaning=1`, `entity_summary_to_max_tokens=500`
- **Cost estimate**: ~$0.11 per 2MB document indexing, ~$0.02 per runtime query
- See `MODEL_OPTIMIZATION.md` for detailed cost analysis

## Port Configuration

- **Current**: Port 8080 (see `app.py:197`)
- Server binds to `0.0.0.0` for external access

## Documentation

- **INDEXING_GUIDE.md**: Complete guide to multi-format document indexing
- **MODEL_OPTIMIZATION.md**: Cost analysis and model selection recommendations

## Key Dependencies

**Core Frameworks:**
- `gradio>=4.0.0` - Web UI framework
- `openai>=1.0.0` - OpenAI API client
- `openai-agents==0.4.2` - OpenAI Agents SDK for orchestration
- `autogen-agentchat==0.6.1`, `autogen-core==0.6.1`, `autogen-ext==0.6.1` - AutoGen v0.6 multi-agent framework

**Document Processing:**
- `python-docx>=1.0.0` - DOCX/DOC file parsing
- `langchain==1.0.3`, `langchain-text-splitters==1.0.0` - Text chunking for RAG

**RAG & NLP:**
- `lightrag-hku==1.4.9.7` - MiniRAG knowledge graph retrieval
- `sentence-transformers>=2.2.0` - Embeddings support
- `torch>=2.0.0` - PyTorch backend for transformers
- `nltk==3.9.2` - Natural language processing
- `rouge==1.0.1` - Text similarity metrics

**Utilities:**
- `python-dotenv==1.1.0` - Environment variable management
- `numpy<2.0.0` - Numerical operations (version pinned for compatibility)

## File References

When debugging or modifying:
- **Orchestrator agent**: `openai_agent.py:17-67` (creates agent with both tools)
- **Clarification agent tool**: `openai_agent.py:10-14` (function_tool wrapper)
- **Clarification logic**: `clarification_agent.py:76-118` (hybrid search with fallback)
- **Document search tool**: `openai_agent.py:30-41` (function_tool wrapper for AutoGen)
- **AutoGen search logic**: `autogen_agent.py:56-82` (on_messages method)
- **SQLite session**: `openai_agent.py:107-110` (conversation persistence)
- **Event loop handling**: `openai_agent.py:149-162` (sync wrapper for async operations)
- **Gradio chat interface**: `app.py:88-181` (UI components and callbacks)
- **Document loading**: `app.py:24-49` (initialize_agent function)
- **Trace context**: `openai_agent.py:124` (observability wrapper)
- **Vector threshold**: `clarification_agent.py:43` (cosine_better_than_threshold=0.0)
- **Hybrid fallback**: `clarification_agent.py:113-116` (direct entity search)
- **Multi-format indexing**: `indexing.py:13-46` (DOCX, DOC, TXT support)
