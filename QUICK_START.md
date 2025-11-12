# FAQ Bot - Quick Start Guide

Quick reference for running and managing the FAQ Bot.

## Prerequisites

- Python 3.12
- OpenAI API key
- Virtual environment activated

## First Time Setup

```bash
# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
echo "OPENAI_API_KEY=your-key-here" > .env

# Add documents
mkdir -p docs
cp your-document.docx docs/

# Index documents (optional)
python -m src.indexing
```

## Running the Applications

### Chat Application (Users - Port 8080)

```bash
source venv/bin/activate
python run_app.py
```

Access at: **http://localhost:8080**

### Config Application (Admins - Port 8081)

```bash
source venv/bin/activate
python run_config.py
```

Access at: **http://localhost:8081**

### Both Applications

```bash
source venv/bin/activate
./scripts/start_both.sh

# To stop:
./scripts/stop_both.sh
```

## Common Tasks

### Add New Documents

**Option 1: Using Config GUI (Recommended)**
1. Open http://localhost:8081
2. Upload documents
3. Click "Run Indexing"

**Option 2: Manual**
```bash
# Add files to docs/
cp your-document.docx docs/
cp another-doc.txt docs/

# Run indexing
python -m src.indexing
```

### Preview What Would Be Indexed

```bash
python scripts/demo_indexing.py
```

### Test MiniRAG Knowledge Graph

```bash
python tests/test.py
```

### Visualize Knowledge Graph

```bash
python scripts/graph.py
# Creates graph_visualization.png
```

### Clear Conversation History

Restart the chat application or use the "Clear Chat" button in the UI.

### Rebuild Knowledge Base

Edit `src/indexing.py` and set `clear_existing=True`, then run:
```bash
python -m src.indexing
```

## Project Structure

```
faq_bot/
├── run_app.py           # Run chat app
├── run_config.py        # Run config app
├── src/                 # Source code
├── scripts/             # Utility scripts
├── tests/               # Test scripts
├── docs/                # Your documents
├── kb/                  # Knowledge base (auto-generated)
└── .env                 # API keys
```

## Supported Document Formats

- ✅ DOCX (Microsoft Word)
- ✅ DOC (Legacy Word)
- ✅ TXT (Plain text)

## Ports

- **8080** - Chat application (users)
- **8081** - Config application (admins only)

## Cost Estimates

- **Indexing**: ~$0.11 per 2MB document (using gpt-4o-mini)
- **Runtime**: ~$0.02 per query (using gpt-4o)

## Troubleshooting

### "Module not found" errors
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### No documents found
```bash
# Check docs directory
ls docs/

# Add documents
cp your-file.docx docs/
```

### API key errors
```bash
# Check .env file exists
cat .env

# Set API key
echo "OPENAI_API_KEY=sk-your-key" > .env
```

### Port already in use
```bash
# Kill process on port 8080
lsof -ti:8080 | xargs kill

# Or use different port by editing src/app.py
```

## Getting Help

- See `README.md` for detailed documentation
- See `CLAUDE.md` for architecture details
- See `INDEXING_GUIDE.md` for indexing help
- Check logs in `logs/` directory

## Security Notes

⚠️ **IMPORTANT**: Restrict access to port 8081 (config interface) to administrators only.

Use firewall rules, VPN, or reverse proxy with authentication in production.

---

For more details, see the full `README.md` documentation.
