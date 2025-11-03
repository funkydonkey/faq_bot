# FAQ Bot - Document Q&A System

A Gradio-based chat application that answers questions about documents using OpenAI and AutoGen agents with MiniRAG knowledge graph retrieval.

## Features

- 📄 Auto-loads DOCX documents from `docs/` folder
- 🤖 Uses OpenAI GPT-4o for intelligent question answering
- 🔍 MiniRAG knowledge graph for enhanced retrieval
- 💬 Clean Gradio chat interface
- 🚀 No manual upload needed - just drop files in `docs/`

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

5. Add your DOCX file to the `docs/` folder:
```bash
mkdir -p docs
cp your-document.docx docs/
```

## Usage

### Run the Gradio App

```bash
source venv/bin/activate
python app.py
```

The app will start at http://localhost:7860

### Run MiniRAG Test

To test the MiniRAG knowledge graph query:

```bash
python test.py
```

## Project Structure

```
faq_bot/
├── app.py                 # Main Gradio application
├── autogen_agent.py       # AutoGen document search agent
├── openai_agent.py        # OpenAI agent runner
├── docx_reader.py         # DOCX file reader
├── test.py                # MiniRAG test script
├── requirements.txt       # Python dependencies
├── docs/                  # Place your DOCX files here
├── kb/                    # MiniRAG knowledge base (auto-generated)
└── .env                   # API keys (not in git)
```

## Configuration

- **Model**: GPT-4o (configurable in `app.py`)
- **Port**: 7860 (configurable in `app.py`)
- **Document folder**: `docs/` (first .docx file is loaded)

## Technologies Used

- **Gradio**: Web UI framework
- **OpenAI GPT-4o**: Language model
- **AutoGen**: Multi-agent conversation framework
- **MiniRAG**: Knowledge graph retrieval system
- **python-docx**: Document parsing

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

## License

MIT

## Author

Created with Claude Code
