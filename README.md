# FAQ Bot - Document Q&A System

A Gradio-based chat application that answers questions about documents using a three-layer agent architecture: OpenAI orchestrator, clarification agent with hybrid entity search, and AutoGen document search with MiniRAG knowledge graph retrieval.

## Features

- 📄 **Multi-format support**: DOCX, DOC, TXT files from `docs/` folder
- 🤖 **Three-layer agents**: OpenAI orchestrator → Clarification/Search agents → Documents
- 🔍 **Hybrid search**: LLM entity extraction with direct vector fallback
- 💰 **Cost-optimized**: gpt-4o-mini for indexing (15x cheaper), gpt-4o for runtime
- 💬 Clean Gradio chat interface
- ⚙️ **Separate admin interface**: Document management and indexing GUI on dedicated port
- 🔒 **Security-focused**: Admin interface isolated for restricted access

## Prerequisites

- Python 3.12 (required for pyautogen compatibility)
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd faq_bot
```

2. Create a virtual environment with Python 3.12:
```bash
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API key:
```bash
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

5. Add your documents to the `docs/` folder (supports DOCX, DOC, TXT):
```bash
mkdir -p docs
cp your-document.docx docs/
cp your-faq.txt docs/
```

6. Index your documents (optional - creates knowledge graph):
```bash
python indexing.py
```

## Usage

The FAQ Bot consists of **two separate applications**:

### 1. Chat Application (End Users) - Port 8080

```bash
source venv/bin/activate
python app.py
```

The chat interface will start at **http://localhost:8080**

This is the main user-facing interface for asking questions about documents.

### 2. Config Application (Administrators Only) - Port 8081

```bash
source venv/bin/activate
python config_app.py
```

The configuration interface will start at **http://localhost:8081**

This interface provides:
- Document upload and management
- Indexing trigger and monitoring
- Document deletion

**⚠️ SECURITY:** Restrict access to port 8081 using firewall rules, VPN, or reverse proxy with authentication. See `CONFIG_GUI_GUIDE.md` for details.

### Index Documents

**Option 1: Using Config GUI (Recommended)**
1. Open http://localhost:8081
2. Go to the **Indexing** tab
3. Click **Run Indexing**

**Option 2: Command Line**
```bash
python indexing.py
```

Supported formats: DOCX, DOC, TXT

### Preview Files to Index

See what files would be indexed without running full indexing:

```bash
python demo_indexing.py
```

### Run MiniRAG Test

To test the MiniRAG knowledge graph query:

```bash
python test.py
```

## Project Structure

```
faq_bot/
├── app.py                    # Main chat application (port 8080)
├── config_app.py             # Admin config application (port 8081)
├── config_ui.py              # Config UI components
├── openai_agent.py           # OpenAI orchestrator agent
├── clarification_agent.py    # Entity extraction agent (hybrid search)
├── autogen_agent.py          # AutoGen document search agent
├── docx_reader.py            # DOCX file reader
├── indexing.py               # Multi-format document indexing (DOCX, DOC, TXT)
├── demo_indexing.py          # Preview files to be indexed
├── graph.py                  # Knowledge graph visualization
├── test.py                   # MiniRAG test script
├── requirements.txt          # Python dependencies
├── docs/                     # Place your documents here (DOCX, DOC, TXT)
├── kb/                       # MiniRAG knowledge base (auto-generated)
├── CONFIG_GUI_GUIDE.md       # Configuration interface guide
├── INDEXING_GUIDE.md         # Complete indexing documentation
├── MODEL_OPTIMIZATION.md     # Cost analysis and recommendations
└── .env                      # API keys (not in git)
```

## Configuration

- **Models**:
  - Runtime: GPT-4o for orchestrator, clarification, and search (best quality)
  - Indexing: gpt-4o-mini (94% cost savings)
  - Embeddings: text-embedding-3-small (most cost-efficient)
- **Ports**:
  - Chat application: 8080 (user-facing)
  - Config application: 8081 (admin-only)
- **Document folder**: `docs/` (supports DOCX, DOC, TXT)
- **Vector threshold**: 0.0 for maximum recall with fallback strategy

## Technologies Used

- **Gradio**: Web UI framework
- **OpenAI GPT-4o**: Language model for runtime queries
- **OpenAI gpt-4o-mini**: Cost-efficient model for indexing
- **AutoGen**: Multi-agent conversation framework
- **MiniRAG**: Knowledge graph retrieval system with hybrid search
- **python-docx**: DOCX/DOC document parsing
- **LangChain**: Text splitting and chunking

## Troubleshooting

### Virtual Environment Issues
Make sure you're using Python 3.12:
```bash
python --version  # Should show 3.12.x
```

### AutoGen Agent Issues
If agents talk to themselves, check `autogen_agent.py:57`:
```python
max_consecutive_auto_reply=0  # Should be 0, not 1
```

### OpenAI API Errors
- Verify your API key in `.env`
- Check your OpenAI account has credits

### Empty Entity Results
If queries return no entities:
- Threshold is set to 0.0 in `clarification_agent.py:42-44`
- Hybrid fallback automatically engages when mini mode returns empty
- Check that documents are properly indexed in `kb/` directory

### Cost Optimization
- Indexing uses gpt-4o-mini (~$0.11 per 2MB document)
- Runtime queries use gpt-4o (~$0.02 per query)
- See `MODEL_OPTIMIZATION.md` for detailed cost analysis

## License

MIT

## Author

Created with Claude Code
