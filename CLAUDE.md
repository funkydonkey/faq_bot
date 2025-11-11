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
   - Wraps calls in `trace("document_qa_agent_call")` for observability (see line 124)
   - Exposes two `@function_tool` decorators:
     - `run_clarification_agent()` (lines 10-14) - calls clarification agent
     - `search_document()` (lines 30-41) - calls AutoGen search agent
   - Handles async/await with proper event loop management (lines 149-162)
   - **SQLite conversation persistence**: Uses `SQLiteSession` to persist conversation history across sessions (lines 107-110)
   - Database: `conversation_history.db` stores all conversations with session ID "faq_conversation"

2. **Clarification Agent** (`clarification_agent.py`):
   - Extracts entities from ambiguous user queries using MiniRAG (uses GPT-4o)
   - **Hybrid search strategy**:
     - Primary: "mini" mode with LLM-based entity extraction (lines 89-96)
     - Fallback: Direct vector search on entity descriptions when mini mode returns empty (lines 49-74, 114-116)
   - Configured with `cosine_better_than_threshold=0.0` for maximum recall (line 43)
   - Returns structured `ClarificationContext` with entity list, scores, and descriptions (lines 13-21)
   - Exposed as `@function_tool` `retrieve_clarification_context()` (lines 76-118)

3. **AutoGen Search Agent** (`autogen_agent.py`):
   - Called as a tool by the OpenAI orchestrator
   - Uses AutoGen v0.6 API with `AssistantAgent` and `OpenAIChatCompletionClient` (lines 33-54)
   - Receives `doc_content` as parameter during initialization (no duplicate loading)
   - Returns direct answers from document content using `on_messages()` method (lines 68-71)
   - **Note**: AutoGen v0.6 API does not have `max_consecutive_auto_reply` parameter (this was in older versions)

### Key Components

**Core Application Files:**
- **app.py**: Gradio interface, auto-loads first DOCX from `docs/` on startup (line 30-36), port 8080 (line 197)
- **openai_agent.py**: `OpenAIAgentRunner` class - manages orchestrator, SQLite session, and conversation history
- **clarification_agent.py**: Entity extraction agent with hybrid search (mini mode + fallback)
- **autogen_agent.py**: `DocumentSearchAgent` class - focused document search tool using AutoGen v0.6
- **docx_reader.py**: `DocxReader` class - extracts text from DOCX including tables

**Indexing & Knowledge Graph:**
- **indexing.py**: Multi-format document indexing (DOCX, DOC, TXT) with cost-efficient gpt-4o-mini
- **demo_indexing.py**: Preview files to be indexed without running full indexing
- **graph.py**: Knowledge graph visualization using NetworkX

**Testing & Debugging:**
- **test.py**: Standalone MiniRAG query test
- **test_hybrid.py**: Test hybrid search strategy (mini mode + fallback)
- **test_threshold.py**: Test vector similarity threshold behavior
- **debug_mini.py**: Debug MiniRAG "mini" mode entity extraction

**Data & Storage:**
- **conversation_history.db**: SQLite database for persistent conversation history
- **kb/**: MiniRAG knowledge base directory (auto-generated during indexing)
- **docs/**: Document storage (DOCX, DOC, TXT files)

### MiniRAG Integration

- **Location**: `MiniRAG/` subdirectory (vendored dependency)
- **Storage**: Knowledge base persisted in `kb/` directory
- **Indexing**: Documents split into chunks using `RecursiveCharacterTextSplitter` (500 chars, 200 overlap)
- **Embedding**: OpenAI `text-embedding-3-small` (1536 dimensions, most cost-efficient)
- **LLM Models**:
  - **Indexing**: `gpt-4o-mini` for cost efficiency (15x cheaper than gpt-4o)
  - **Runtime**: `gpt-4o` for clarification and document search (best quality)
- **Supported Formats**: DOCX, DOC, TXT with automatic format detection
- **Vector Search**: Threshold set to 0.0 (`cosine_better_than_threshold=0.0`) for maximum recall with fallback strategy
- **Dependencies**:
  - `lightrag-hku==1.4.9.7` - Core RAG functionality
  - `torch>=2.0.0` - PyTorch for embeddings
  - `sentence-transformers>=2.2.0` - Sentence embeddings
  - `langchain==1.0.3` + `langchain-text-splitters==1.0.0` - Text chunking
  - `nltk==3.9.2` + `rouge==1.0.1` - NLP utilities

## Important Implementation Details

### Warning Suppression
`app.py:11-12` suppresses FLAML and AutoGen warnings at module level before imports:
```python
warnings.filterwarnings('ignore', message='.*flaml.automl.*')
logging.getLogger('autogen.oai.client').setLevel(logging.ERROR)
```

### Event Loop Handling
`openai_agent.py:149-162` handles event loop creation/reuse for async operations in sync context (required for Gradio callbacks).

### SQLite Session Management
- `openai_agent.py:107-110` creates `SQLiteSession` for persistent conversation history
- Session ID: "faq_conversation" (shared across app restarts)
- Database file: `conversation_history.db` in project root
- `clear_history()` method clears both in-memory and SQLite history (lines 184-197)

### Document Loading
- Documents load from `docs/` directory automatically (DOCX, DOC, TXT supported)
- First DOCX file found is used (see `app.py:30-36`)
- Single document loading - no duplicate `get_document_summary()` methods
- Multi-format support: DOCX/DOC via python-docx, TXT with UTF-8/Latin-1 fallback

### Agent Configuration
**AutoGen v0.6 API Changes**: The `max_consecutive_auto_reply` parameter from older AutoGen versions is **not present** in v0.6. The new API uses `AssistantAgent.on_messages()` method which processes a single message and returns, preventing infinite loops by design.

## Cost Optimization

- **Indexing** uses `gpt-4o-mini` (94% cost savings vs gpt-4o)
- **Runtime** uses `gpt-4o` for best quality on user-facing queries
- **Embeddings** use `text-embedding-3-small` (6.5x cheaper than large)
- **Token limits**: `entity_extract_max_gleaning=1`, `entity_summary_to_max_tokens=500`
- **Cost estimate**: ~$0.11 per 2MB document indexing, ~$0.02 per runtime query
- See `MODEL_OPTIMIZATION.md` for detailed cost analysis

## Port Configuration

- **Current**: Port 8080 (see `app.py:197`)
- Server binds to `0.0.0.0` for external access (line 196)

## Documentation

- **INDEXING_GUIDE.md**: Complete guide to multi-format document indexing
- **MODEL_OPTIMIZATION.md**: Cost analysis and model selection recommendations
- **README.md**: User-facing documentation with setup and usage instructions

## File References

When debugging or modifying:
- **Agent Orchestration**:
  - OpenAI orchestrator setup: `openai_agent.py:17-67`
  - Function tools registration: `openai_agent.py:10-14` (clarification), `30-41` (search)
  - SQLite session creation: `openai_agent.py:107-110`
  - Trace context wrapper: `openai_agent.py:124`

- **Clarification Agent**:
  - Hybrid search implementation: `clarification_agent.py:49-118`
  - Mini mode query: `clarification_agent.py:89-96`
  - Fallback direct search: `clarification_agent.py:49-74, 114-116`
  - Vector threshold config: `clarification_agent.py:42-44`
  - Agent definition: `clarification_agent.py:120-126`

- **AutoGen Search**:
  - AutoGen v0.6 client setup: `autogen_agent.py:33-54`
  - Search method: `autogen_agent.py:56-82`
  - Message processing: `autogen_agent.py:68-71`

- **Gradio Interface**:
  - Chat callback: `app.py:52-77`
  - Document initialization: `app.py:24-49`
  - Message handler: `app.py:129-142`
  - Server launch config: `app.py:195-198`

- **Indexing**:
  - Multi-format document loading: `indexing.py:13-46`
  - MiniRAG initialization: `indexing.py:49-71`

## Requirements

**Core Dependencies** (see `requirements.txt`):
- `gradio>=4.0.0` - Web UI
- `openai>=1.0.0` - OpenAI API client
- `openai-agents==0.4.2` - OpenAI Agents SDK
- `autogen-agentchat==0.6.1` + `autogen-core==0.6.1` + `autogen-ext==0.6.1` - AutoGen framework
- `python-docx>=1.0.0` - DOCX parsing
- `python-dotenv>=1.0.0` - Environment variables
- `lightrag-hku==1.4.9.7` - MiniRAG implementation
- `torch>=2.0.0` + `sentence-transformers>=2.2.0` - Embeddings
- `langchain==1.0.3` + `langchain-text-splitters==1.0.0` - Text processing
- `nltk==3.9.2` + `rouge==1.0.1` - NLP utilities
- `numpy<2.0.0` - Numerical operations (version constraint for compatibility)
