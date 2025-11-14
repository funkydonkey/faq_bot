# UI Comparison: Gradio vs Streamlit

## Quick Reference

| Feature | Gradio | Streamlit |
|---------|--------|-----------|
| **Port** | 8080 | 8082 |
| **Launch** | `python run_app.py` | `python run_streamlit.py` |
| **Document Switching** | ❌ Requires restart | ✅ Live reload in sidebar |
| **Document Preview** | ❌ Not available | ✅ Expandable in sidebar |
| **Auto-load on Start** | ✅ First DOCX | ✅ First DOCX |
| **Chat Statistics** | ❌ Not shown | ✅ Message count |
| **State Management** | Global variables | Session state |
| **Mobile Support** | ⚠️ Good | ✅ Better |
| **Deployment** | Hugging Face Spaces | Streamlit Cloud |
| **Customization** | ✅ Themes & CSS | ⚠️ Limited theming |

## When to Use Each

### Use Gradio (`run_app.py`) When:
- ✅ You want the **simplest, fastest** deployment
- ✅ You're deploying to **Hugging Face Spaces**
- ✅ You prefer **theme customization** (dark/light modes)
- ✅ You work with a **single fixed document**
- ✅ You want **minimal configuration**

### Use Streamlit (`run_streamlit.py`) When:
- ✅ You need to **switch between documents frequently**
- ✅ You want **document preview without leaving UI**
- ✅ You prefer **modern, polished design**
- ✅ You want **better mobile experience**
- ✅ You're deploying to **Streamlit Cloud**
- ✅ You need **chat statistics and analytics**

## Feature Details

### Document Management

**Gradio:**
```python
# Fixed document loaded on startup
docx_files = glob.glob(os.path.join(docs_dir, "*.docx"))
file_path = docx_files[0]  # Always first file
agent_runner = OpenAIAgentRunner(docx_path=file_path)
```

**Streamlit:**
```python
# Dynamic document selector
available_docs = get_available_documents()
selected_doc = st.selectbox("Select Document", doc_names)
if st.button("Load Document"):
    load_document(selected_doc_path)  # Live switch
```

### State Management

**Gradio:**
```python
# Global state
agent_runner = None
current_docx_path = None

def chat_callback(message, history):
    global agent_runner
    response = agent_runner.process_query(message)
    return response
```

**Streamlit:**
```python
# Session state (isolated per user)
if 'agent_runner' not in st.session_state:
    st.session_state.agent_runner = None

response = st.session_state.agent_runner.process_query(prompt)
```

### Chat History

**Gradio:**
```python
# Managed by Gradio component
chatbot = gr.Chatbot(type="messages")
chat_history.append({"role": "user", "content": message})
```

**Streamlit:**
```python
# Manual management with st.chat_message
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
```

## Architecture Differences

### Gradio Flow
```
User Input → gr.Chatbot → chat_callback() → agent_runner.process_query() → Response
                 ↓
           Global state (agent_runner)
```

### Streamlit Flow
```
User Input → st.chat_input → st.session_state.agent_runner.process_query() → Response
                 ↓
           Session state (isolated per browser tab)
```

## Performance Comparison

### Startup Time
- **Gradio**: ~3-5 seconds (loads first document)
- **Streamlit**: ~3-5 seconds (loads first document, caches session state)

### Memory Usage
- **Gradio**: Lower (single global agent)
- **Streamlit**: Higher (session state per user)

### Concurrent Users
- **Gradio**: Shared global state (potential conflicts)
- **Streamlit**: Isolated session state (better isolation)

## Deployment Comparison

### Gradio Deployment

**Hugging Face Spaces:**
```yaml
# spaces.yaml
sdk: gradio
sdk_version: 4.0.0
python_version: 3.12
```

**Pros:**
- Built-in authentication
- Easy public sharing
- GPU support available

**Cons:**
- Limited to Gradio apps
- Slower cold starts

### Streamlit Deployment

**Streamlit Cloud:**
```toml
# .streamlit/config.toml
[server]
port = 8082
headless = true
```

**Pros:**
- Free tier with GitHub integration
- Automatic redeployment on push
- Better caching mechanisms

**Cons:**
- No GPU support on free tier
- More restrictive resource limits

## Code Maintainability

### Gradio
- ✅ **Simpler**: Fewer abstractions, direct global state
- ✅ **Faster to prototype**: Less boilerplate
- ⚠️ **Callback-based**: Can get messy with complex flows
- ❌ **Global state**: Harder to test, debug concurrency issues

### Streamlit
- ✅ **Cleaner state management**: Session state is explicit
- ✅ **Better for complex apps**: Sidebar, tabs, expanders
- ⚠️ **Rerun model**: Can be confusing for beginners
- ⚠️ **More verbose**: Requires more code for same functionality

## UI Customization

### Gradio Themes
```python
demo = create_interface()
demo.launch(
    theme=gr.themes.Soft(),  # Built-in themes
    css=".custom { color: blue; }"  # Custom CSS
)
```

### Streamlit Themes
```toml
# .streamlit/config.toml
[theme]
primaryColor = "#F63366"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

## Migration Path

### From Gradio to Streamlit

1. **Replace global variables** with `st.session_state`
2. **Convert gr.Chatbot** to `st.chat_message` + `st.chat_input`
3. **Add document selector** with `st.selectbox`
4. **Replace gr.Button** callbacks with direct button checks

### From Streamlit to Gradio

1. **Replace st.session_state** with global variables
2. **Convert st.chat_message** to `gr.Chatbot(type="messages")`
3. **Remove document selector** (use fixed first document)
4. **Wrap logic** in callback functions for gr.Button

## Recommendations

### For Production
- **Large organizations**: Streamlit (better state isolation)
- **Public demos**: Gradio (easier sharing, better themes)
- **Internal tools**: Either (depends on team preference)

### For Development
- **Quick prototypes**: Gradio (less boilerplate)
- **Complex apps**: Streamlit (better component library)
- **Testing**: Streamlit (session state easier to mock)

### For Specific Use Cases
- **Single document FAQ**: Gradio
- **Multi-document search**: Streamlit
- **Mobile-first**: Streamlit
- **Custom styling**: Gradio

## Running Both Simultaneously

You can run both interfaces at the same time:

```bash
# Terminal 1
python run_app.py        # Gradio on 8080

# Terminal 2
python run_streamlit.py  # Streamlit on 8082
```

Or use the convenience script:

```bash
./scripts/start_all.sh   # Starts Gradio, Streamlit, and Config
./scripts/stop_all.sh    # Stops all
```

This allows users to choose their preferred interface while maintaining the same backend logic.

## Conclusion

Both interfaces share the same:
- ✅ **Agent architecture** (OpenAI orchestrator + clarification + search)
- ✅ **Document processing** (DOCX, DOC, TXT support)
- ✅ **Knowledge graph** (MiniRAG integration)
- ✅ **Cost optimization** (gpt-4o-mini for indexing)

Choose based on:
- **Deployment target** (Hugging Face vs Streamlit Cloud)
- **Feature needs** (document switching, preview)
- **Team preference** (callbacks vs reruns)

**Default recommendation**: Start with **Gradio** for simplicity, migrate to **Streamlit** if you need advanced features.
