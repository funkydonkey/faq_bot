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
   - Exposes `search_document()` as a `@function_tool` for the orchestrator to call
   - Handles async/await with proper event loop management

2. **Clarification Agent** (`clarification_agent.py`):
   - Extracts entities from ambiguous user queries using MiniRAG (uses GPT-4o)
   - **Hybrid search strategy**:
     - Primary: "mini" mode with LLM-based entity extraction
     - Fallback: Direct vector search on entity descriptions when mini mode returns empty
   - Configured with `cosine_better_than_threshold=0.0` for maximum recall
   - Returns structured entity list with scores and descriptions

3. **AutoGen Search Agent** (`autogen_agent.py`):
   - Called as a tool by the OpenAI orchestrator
   - Receives `doc_content` as a parameter (no duplicate loading)
   - Configured with `max_consecutive_auto_reply=0` to prevent self-conversation
   - Returns direct answers from document content
   - Clears history after each search to prevent context bleed

### Key Components

- **app.py**: Gradio interface, auto-loads first document from `docs/` on startup
- **openai_agent.py**: `OpenAIAgentRunner` class - manages orchestrator and conversation history
- **clarification_agent.py**: Entity extraction agent with hybrid search (mini mode + fallback)
- **autogen_agent.py**: `DocumentSearchAgent` class - focused document search tool
- **docx_reader.py**: `DocxReader` class - extracts text from DOCX including tables
- **indexing.py**: Multi-format document indexing (DOCX, DOC, TXT) with cost-efficient gpt-4o-mini
- **demo_indexing.py**: Preview files to be indexed without running full indexing
- **graph.py**: Knowledge graph visualization using NetworkX
- **test.py**: Standalone MiniRAG query test

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

### Warning Suppression
`app.py` suppresses FLAML and AutoGen warnings at module level before imports:
```python
warnings.filterwarnings('ignore', message='.*flaml.automl.*')
logging.getLogger('autogen.oai.client').setLevel(logging.ERROR)
```

### Event Loop Handling
`openai_agent.py:111-137` handles event loop creation/reuse for async operations in sync context (required for Gradio callbacks).

### Document Loading
- Documents load from `docs/` directory automatically (DOCX, DOC, TXT supported)
- First document file found is used
- Single document loading - no duplicate `get_document_summary()` methods
- Multi-format support: DOCX/DOC via python-docx, TXT with UTF-8/Latin-1 fallback

### Agent Configuration
**Critical**: AutoGen agent MUST have `max_consecutive_auto_reply=0` (see `autogen_agent.py:63`) to prevent infinite agent-to-agent conversations.

## Cost Optimization

- **Indexing** uses `gpt-4o-mini` (94% cost savings vs gpt-4o)
- **Runtime** uses `gpt-4o` for best quality on user-facing queries
- **Embeddings** use `text-embedding-3-small` (6.5x cheaper than large)
- **Token limits**: `entity_extract_max_gleaning=1`, `entity_summary_to_max_tokens=500`
- **Cost estimate**: ~$0.11 per 2MB document indexing, ~$0.02 per runtime query
- See `MODEL_OPTIMIZATION.md` for detailed cost analysis

## Port Configuration

- **Current**: Port 8080 (see `app.py:191`)
- **Previous**: Port 7860 (mentioned in README, changed in latest code)

## Documentation

- **INDEXING_GUIDE.md**: Complete guide to multi-format document indexing
- **MODEL_OPTIMIZATION.md**: Cost analysis and model selection recommendations

## File References

When debugging or modifying:
- Agent orchestration: `openai_agent.py:10-54`
- Clarification agent: `clarification_agent.py:49-118` (hybrid search with fallback)
- Document search logic: `autogen_agent.py:67-112`
- Gradio callbacks: `app.py:51-76`
- Multi-format extraction: `indexing.py:13-46`
- Trace context: `openai_agent.py:103`
- Vector threshold: `clarification_agent.py:42-44`
