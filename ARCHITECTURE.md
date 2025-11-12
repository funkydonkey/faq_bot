# FAQ Bot Architecture

A visual guide to understanding how the FAQ Bot works.

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         FAQ Bot System                          │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────┐              ┌──────────────────────┐
│   End Users          │              │   Administrators     │
│   (Ask Questions)    │              │   (Manage Docs)      │
└──────────┬───────────┘              └──────────┬───────────┘
           │                                     │
           │ http://localhost:8080               │ http://localhost:8081
           │                                     │
           ▼                                     ▼
┌──────────────────────┐              ┌──────────────────────┐
│  Chat Application    │              │  Config Application  │
│  (run_app.py)        │              │  (run_config.py)     │
│  Port 8080           │              │  Port 8081           │
└──────────┬───────────┘              └──────────┬───────────┘
           │                                     │
           │                                     │ Upload & Index
           ▼                                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Core Processing Engine                        │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │            Three-Layer Agent Architecture                  │ │
│  │                                                            │ │
│  │  ┌──────────────────────────────────────────────────┐    │ │
│  │  │  Layer 1: OpenAI Orchestrator (GPT-4o)          │    │ │
│  │  │  - Evaluates user questions                      │    │ │
│  │  │  - Decides which tool to use                     │    │ │
│  │  │  - Manages conversation flow                     │    │ │
│  │  └──────────────┬───────────────────────────────────┘    │ │
│  │                 │                                         │ │
│  │      ┌──────────┴──────────┐                             │ │
│  │      ▼                     ▼                             │ │
│  │  ┌─────────────────┐  ┌─────────────────────────────┐  │ │
│  │  │ Layer 2A:       │  │ Layer 2B:                   │  │ │
│  │  │ Clarification   │  │ Document Search             │  │ │
│  │  │ Agent (GPT-4o)  │  │ Agent (GPT-4o + AutoGen)    │  │ │
│  │  │                 │  │                             │  │ │
│  │  │ - Extract       │  │ - Search documents          │  │ │
│  │  │   entities      │  │ - Find answers              │  │ │
│  │  │ - Hybrid search │  │ - Return results            │  │ │
│  │  └─────┬───────────┘  └─────┬───────────────────────┘  │ │
│  │        │                    │                           │ │
│  │        └────────┬───────────┘                           │ │
│  │                 ▼                                       │ │
│  │         ┌───────────────┐                              │ │
│  │         │  Layer 3:     │                              │ │
│  │         │  MiniRAG KB   │                              │ │
│  │         │  (Vector DB)  │                              │ │
│  │         └───────────────┘                              │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Data Storage                             │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │   docs/      │  │     kb/      │  │ conversation_        │ │
│  │              │  │              │  │ history.db           │ │
│  │ - DOCX files │  │ - Entities   │  │                      │ │
│  │ - DOC files  │  │ - Relations  │  │ - Chat history       │ │
│  │ - TXT files  │  │ - Embeddings │  │ - Session state      │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow: Asking a Question

```
1. User enters question
   │
   ▼
2. Chat UI (Gradio) receives input
   │
   ▼
3. OpenAI Orchestrator Agent evaluates question
   │
   ├─── Question is clear? ───► 4. Call Document Search Agent
   │                                │
   │                                ▼
   │                             5. AutoGen searches documents
   │                                │
   │                                ▼
   │                             6. MiniRAG retrieves relevant chunks
   │                                │
   └─── Question is ambiguous? ─►  7. Call Clarification Agent
                                     │
                                     ▼
                                  8. Extract entities (hybrid search)
                                     │
                                     ▼
                                  9. Ask user for clarification
                                     │
                                     ▼
                                  10. User provides more context
                                      │
                                      └──► Back to step 3

11. Orchestrator receives results
    │
    ▼
12. Generate final answer
    │
    ▼
13. Display to user in chat UI
```

## Data Flow: Adding Documents

```
1. Admin opens Config UI (port 8081)
   │
   ▼
2. Upload DOCX/DOC/TXT files
   │
   ▼
3. Files saved to docs/ folder
   │
   ▼
4. Admin clicks "Run Indexing"
   │
   ▼
5. Indexing script reads all files
   │
   ├─── DOCX files ───► python-docx extracts text
   │                    │
   ├─── DOC files ────► python-docx extracts text
   │                    │
   └─── TXT files ────► read as plain text
                        │
                        ▼
6. Text chunked into 500-char pieces (200 overlap)
   │
   ▼
7. Each chunk sent to GPT-4o-mini for entity extraction
   │
   ▼
8. Entities and relationships stored in MiniRAG
   │
   ▼
9. Vector embeddings created (text-embedding-3-small)
   │
   ▼
10. Knowledge graph built in kb/ folder
    │
    ▼
11. Indexing complete - ready for queries!
```

## Component Breakdown

### 1. Entry Points (`run_app.py`, `run_config.py`)

**Purpose**: Launch the applications

**What they do**:
- Import the main functions from `src/`
- Call `main()` to start the Gradio servers
- Nothing else - all logic is in `src/`

```python
# run_app.py
from src.app import main

if __name__ == "__main__":
    main()
```

### 2. Chat Application (`src/app.py`)

**Purpose**: User interface for asking questions

**Key functions**:
- `initialize_agent()` - Loads document on startup
- `chat_callback()` - Processes user questions
- `create_interface()` - Builds Gradio UI

**Port**: 8080

**Tech**: Gradio web framework

### 3. Config Application (`src/config_app.py` + `src/config_ui.py`)

**Purpose**: Admin interface for document management

**Features**:
- Upload documents
- View existing documents
- Trigger indexing
- Monitor indexing progress

**Port**: 8081

**Tech**: Gradio web framework

### 4. OpenAI Orchestrator (`src/openai_agent.py`)

**Purpose**: Main decision-making agent

**Model**: GPT-4o

**Responsibilities**:
- Evaluate incoming questions
- Decide if clarification is needed
- Call appropriate sub-agents
- Maintain conversation history
- Return final answers

**Key class**: `OpenAIAgentRunner`

**Session storage**: SQLite (`conversation_history.db`)

### 5. Clarification Agent (`src/clarification_agent.py`)

**Purpose**: Extract entities from ambiguous questions

**Model**: GPT-4o

**Strategy**: Hybrid search
- Primary: LLM-based entity extraction ("mini" mode)
- Fallback: Direct vector search if mini mode returns empty

**Threshold**: 0.0 (accept all results for maximum recall)

**Example**:
```
User: "I can't access my account"
↓
Clarification Agent extracts:
- Entity: "account"
- Related concepts: "login", "password", "access"
↓
Returns context to Orchestrator
```

### 6. Document Search Agent (`src/autogen_agent.py`)

**Purpose**: Search documents and find answers

**Framework**: AutoGen v0.6

**Model**: GPT-4o

**How it works**:
1. Receives question from Orchestrator
2. Uses MiniRAG to find relevant document chunks
3. Reads those chunks
4. Generates answer based on content
5. Returns answer to Orchestrator

**Key class**: `DocumentSearchAgent`

### 7. Document Reader (`src/docx_reader.py`)

**Purpose**: Extract text from documents

**Supports**:
- DOCX (Microsoft Word)
- DOC (legacy Word)
- Tables and paragraphs

**Library**: python-docx

**Key class**: `DocxReader`

### 8. Indexing Engine (`src/indexing.py`)

**Purpose**: Build knowledge graph from documents

**Process**:
1. Read all files from `docs/`
2. Extract text (DOCX/DOC/TXT)
3. Split into chunks (500 chars, 200 overlap)
4. Extract entities and relationships (GPT-4o-mini)
5. Create vector embeddings (text-embedding-3-small)
6. Build knowledge graph in `kb/`

**Models**:
- Entity extraction: GPT-4o-mini (cost-efficient)
- Embeddings: text-embedding-3-small (1536 dimensions)

**Cost**: ~$0.11 per 2MB document

### 9. MiniRAG Knowledge Graph (`MiniRAG/`)

**Purpose**: Vector database and graph storage

**What it stores**:
- Entities (people, places, concepts)
- Relationships (how entities connect)
- Text chunks (actual document content)
- Vector embeddings (for semantic search)

**Storage**: `kb/` directory

**Files**:
- `graph_chunk_entity_relation.graphml` - Graph structure
- `vdb_chunks.json` - Vector database
- `kv_store_*.json` - Key-value stores

### 10. Conversation Database (`conversation_history.db`)

**Purpose**: Persistent chat history

**Type**: SQLite database

**What it stores**:
- User messages
- Assistant responses
- Session metadata
- Timestamps

**Why**: Maintains context across app restarts

## File Organization

```
faq_bot/
│
├── 🚀 Entry Points (run these)
│   ├── run_app.py              # Start chat (port 8080)
│   └── run_config.py           # Start config (port 8081)
│
├── 📦 Source Code (src/)
│   ├── __init__.py             # Package marker
│   ├── app.py                  # Chat UI
│   ├── config_app.py           # Config app entry
│   ├── config_ui.py            # Config UI components
│   ├── openai_agent.py         # Orchestrator agent
│   ├── clarification_agent.py  # Entity extraction
│   ├── autogen_agent.py        # Document search
│   ├── docx_reader.py          # Document parsing
│   └── indexing.py             # Build knowledge graph
│
├── 🛠️  Scripts (scripts/)
│   ├── demo_indexing.py        # Preview indexing
│   ├── graph.py                # Visualize graph
│   ├── start_both.sh           # Start both apps
│   └── stop_both.sh            # Stop both apps
│
├── 🧪 Tests (tests/)
│   ├── test.py                 # MiniRAG test
│   ├── test_hybrid.py          # Hybrid search test
│   └── test_threshold.py       # Vector threshold test
│
├── 📁 Data Directories
│   ├── docs/                   # Your documents (input)
│   ├── kb/                     # Knowledge base (generated)
│   └── logs/                   # Application logs
│
├── 📄 Documentation
│   ├── README.md               # Main documentation
│   ├── INSTALLATION_GUIDE.md   # This guide!
│   ├── QUICK_START.md          # Quick reference
│   ├── CLAUDE.md               # Developer docs
│   └── ARCHITECTURE.md         # Architecture (this file)
│
└── ⚙️  Configuration
    ├── .env                    # API keys (you create)
    ├── requirements.txt        # Dependencies
    └── conversation_history.db # Chat history
```

## Technology Stack

### Frontend
- **Gradio 4.x** - Web UI framework
  - Creates chat interface
  - Handles file uploads
  - Provides real-time updates

### Backend - Agents
- **OpenAI Agents SDK 0.4.2** - Orchestrator
- **AutoGen 0.6** - Multi-agent framework
- **OpenAI GPT-4o** - Language model (runtime)
- **OpenAI GPT-4o-mini** - Language model (indexing)

### Backend - RAG
- **MiniRAG 1.4.9** - Knowledge graph RAG
- **LangChain** - Text splitting
- **python-docx** - Document parsing

### Backend - Embeddings
- **OpenAI text-embedding-3-small** - Vector embeddings
- **sentence-transformers** - Embedding support

### Storage
- **SQLite** - Conversation history
- **JSON** - Knowledge graph storage

### Infrastructure
- **Python 3.12** - Required runtime
- **python-dotenv** - Environment variables
- **asyncio** - Asynchronous operations

## Security Architecture

### API Key Protection
```
.env file (never committed to Git)
    ↓
Environment variables
    ↓
Loaded by python-dotenv
    ↓
Used by OpenAI SDK
```

### Port Security

| Port | Application | Accessibility | Security Level |
|------|-------------|---------------|----------------|
| 8080 | Chat | End users | Low risk - read only |
| 8081 | Config | Admins only | ⚠️ HIGH RISK - can modify system |

**Recommended security for port 8081**:
- Firewall rules (allow only specific IPs)
- VPN access only
- Reverse proxy with authentication
- SSH tunnel for remote access

### Data Privacy

**What's stored locally**:
- ✅ Your documents (in `docs/`)
- ✅ Knowledge graph (in `kb/`)
- ✅ Conversation history (in `conversation_history.db`)

**What's sent to OpenAI**:
- ⚠️ Document chunks (during indexing)
- ⚠️ User questions (during queries)
- ⚠️ Retrieved context (for answer generation)

**What's NOT sent to OpenAI**:
- ✅ Full documents (only chunks)
- ✅ User credentials
- ✅ System information

## Performance Characteristics

### Indexing Speed
- Small doc (500KB): ~30 seconds
- Medium doc (2MB): ~2 minutes
- Large doc (10MB): ~10 minutes

**Factors**:
- Document size
- Number of chunks (doc_size / 500 chars)
- OpenAI API latency
- Internet speed

### Query Response Time
- Simple question: 2-5 seconds
- Complex question: 5-10 seconds
- Clarification needed: 10-20 seconds

**Factors**:
- Question complexity
- Number of relevant chunks
- Whether clarification is needed
- OpenAI API latency

### Resource Usage

**Memory**:
- Base application: ~200MB
- Small knowledge base: +50MB
- Large knowledge base: +500MB

**CPU**:
- Idle: <5%
- During query: 10-30%
- During indexing: 20-50%

**Disk**:
- Application: ~500MB
- Dependencies: ~1GB
- Knowledge base: ~10MB per 2MB document

**Network**:
- Indexing: High (uploading chunks to OpenAI)
- Queries: Medium (API calls)
- Idle: Minimal

## Scalability Considerations

### Current Limitations
- Single-threaded (one query at a time)
- In-memory knowledge graph
- Local SQLite database
- No load balancing

### Suitable For
- ✅ Small teams (1-50 users)
- ✅ Document sets up to 100MB
- ✅ 100-1000 queries per day
- ✅ Internal company use

### Not Suitable For
- ❌ High-traffic public websites
- ❌ Real-time chat support (too slow)
- ❌ Massive document sets (100GB+)
- ❌ Thousands of concurrent users

### Future Improvements
- Add caching layer
- Implement queue system
- Use distributed database
- Add Redis for sessions
- Deploy with multiple workers

---

This architecture is designed for **clarity** and **ease of use** rather than maximum performance. It's perfect for internal tools, small teams, and learning how AI agents work!
