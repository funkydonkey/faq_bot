# Streamlit Interface Guide

## Overview

The Streamlit interface provides a modern, alternative UI for the FAQ Bot with enhanced features for document management and chat interaction.

## Features

### 🎯 Key Advantages Over Gradio

1. **Document Selector**: Switch between documents without restarting the app
2. **Live Preview**: View document content directly in the sidebar
3. **Auto-load**: First document loads automatically on startup
4. **Statistics**: Track message count in real-time
5. **Modern UI**: Clean, responsive design with better mobile support

## Quick Start

### 1. Install Dependencies

```bash
pip install streamlit>=1.28.0
```

Or install all dependencies:

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
python run_streamlit.py
```

The app will start at: **http://localhost:8082**

### 3. Alternative Launch Method

You can also run directly with Streamlit:

```bash
streamlit run src/streamlit_app.py --server.port=8082 --server.address=0.0.0.0
```

## User Interface

### Sidebar Components

**📚 Document Manager**
- **Select Document**: Dropdown to choose from available DOCX files in `docs/`
- **📂 Load Document**: Button to load the selected document
- **📄 Current Document**: Shows currently loaded document name
- **Preview**: Expandable section showing document content preview
- **🗑️ Clear Chat**: Clears conversation history
- **💬 Messages**: Shows total message count

### Main Chat Area

**💬 FAQ Bot**
- Message history displayed with user/assistant roles
- Chat input at the bottom
- Thinking indicator while processing
- Error messages displayed inline

## Session State Management

The Streamlit app uses session state to maintain:
- `agent_runner`: OpenAI agent instance
- `current_docx_path`: Path to currently loaded document
- `messages`: Chat conversation history
- `document_loaded`: Boolean flag for initialization status

**Why Session State?**
Unlike global variables in Gradio, Streamlit's session state persists across reruns and provides better isolation for concurrent users.

## Comparison: Streamlit vs Gradio

| Feature | Streamlit | Gradio |
|---------|-----------|--------|
| **Port** | 8082 | 8080 |
| **Document Switching** | ✅ Live reload | ❌ Requires restart |
| **Preview** | ✅ In sidebar | ❌ Not available |
| **Auto-load** | ✅ Yes | ✅ Yes |
| **Mobile Support** | ✅ Better | ⚠️ Good |
| **Custom Styling** | ⚠️ Limited | ✅ Themes |
| **Deployment** | Easy (Streamlit Cloud) | Easy (Hugging Face) |

## Tips & Best Practices

### Performance
- First document auto-loads on startup
- Document switching resets chat history (preserves SQLite session)
- Use `Clear Chat` to reset conversation without reloading document

### Document Management
1. Add DOCX files to `docs/` directory
2. Refresh the app (F5) to see new documents in dropdown
3. Select and click "Load Document" to switch

### Error Handling
- Missing API key shows error message at startup
- Document load failures display error in sidebar
- Chat errors show in assistant message

## Troubleshooting

### Port Already in Use

If port 8082 is taken, edit `run_streamlit.py` and change the port:

```python
os.system("streamlit run src/streamlit_app.py --server.port=8083 --server.address=0.0.0.0")
```

### Document Not Loading

1. Check that DOCX file exists in `docs/` directory
2. Verify file is not corrupted (open in Word/LibreOffice)
3. Check console for detailed error messages

### Session State Issues

If the app behaves unexpectedly:
1. Click "Clear Chat" button
2. Refresh browser (F5)
3. Restart the Streamlit server

## Advanced Configuration

### Custom Port and Host

Edit `run_streamlit.py`:

```python
os.system("streamlit run src/streamlit_app.py --server.port=YOUR_PORT --server.address=YOUR_HOST")
```

### Streamlit Configuration File

Create `.streamlit/config.toml`:

```toml
[server]
port = 8082
address = "0.0.0.0"
headless = true

[theme]
primaryColor = "#F63366"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### Development Mode

For auto-reload during development:

```bash
streamlit run src/streamlit_app.py --server.runOnSave=true
```

## Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Connect repository at [streamlit.io/cloud](https://streamlit.io/cloud)
3. Add `OPENAI_API_KEY` to secrets in dashboard

### Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8082

CMD ["streamlit", "run", "src/streamlit_app.py", "--server.port=8082", "--server.address=0.0.0.0"]
```

## Support

For issues specific to:
- **Streamlit UI**: Check [TROUBLESHOOTING_STREAMLIT.md](TROUBLESHOOTING_STREAMLIT.md) ⭐
- **Streamlit framework**: [Streamlit docs](https://docs.streamlit.io)
- **FAQ Bot logic**: See main `README.md` and `TROUBLESHOOTING.md`
- **Agent behavior**: See `ARCHITECTURE.md`

## Important: Always Use run_streamlit.py

**✅ Correct way to launch:**
```bash
python run_streamlit.py
```

**❌ Avoid (may cause import errors):**
```bash
streamlit run src/streamlit_app.py  # May fail with import errors
```

The `run_streamlit.py` script ensures proper path configuration and working directory setup.
