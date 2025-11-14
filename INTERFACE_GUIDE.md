# Interface Guide: Visual Walkthrough

## Gradio Interface (Port 8080)

```
┌────────────────────────────────────────────────────────────┐
│                    Document Q&A Bot                        │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Conversation                                         │ │
│  │                                                      │ │
│  │  👤 User: What is the main topic?                   │ │
│  │                                                      │ │
│  │  🤖 Assistant: Based on the document...             │ │
│  │                                                      │ │
│  │  👤 User: Tell me more about section 3              │ │
│  │                                                      │ │
│  │  🤖 Assistant: Section 3 discusses...               │ │
│  │                                                      │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Your Question                                        │ │
│  │ Type your question here...                           │ │
│  │                                                      │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│     [  Send  ]              [ Clear Chat ]                │
│                                                            │
└────────────────────────────────────────────────────────────┘

Key Features:
✅ Simple, focused chat interface
✅ Auto-loads first document on startup
❌ No document switching (requires restart)
❌ No document preview
```

## Streamlit Interface (Port 8082)

```
┌─────────────────┬──────────────────────────────────────────┐
│  📚 Document    │         💬 FAQ Bot                       │
│   Manager       │                                          │
├─────────────────┤  Ask questions about your documents      │
│                 ├──────────────────────────────────────────┤
│ Select Document │                                          │
│ ┌─────────────┐ │  ┌────────────────────────────────────┐ │
│ │ CV_eng.docx▼│ │  │ 👤 What is the main topic?        │ │
│ └─────────────┘ │  └────────────────────────────────────┘ │
│                 │                                          │
│ [📂 Load Doc]   │  ┌────────────────────────────────────┐ │
│                 │  │ 🤖 Based on the document...        │ │
├─────────────────┤  └────────────────────────────────────┘ │
│                 │                                          │
│ 📄 Current Doc  │  ┌────────────────────────────────────┐ │
│ CV_eng.docx     │  │ 👤 Tell me more about section 3    │ │
│                 │  └────────────────────────────────────┘ │
│ ▶ Preview       │                                          │
│ │ Document...   │  ┌────────────────────────────────────┐ │
│ │ content...    │  │ 🤖 Section 3 discusses...          │ │
│                 │  └────────────────────────────────────┘ │
├─────────────────┤                                          │
│                 │                                          │
│ [🗑️ Clear Chat] │  ┌────────────────────────────────────┐ │
│                 │  │ Type your question here...         │ │
├─────────────────┤  └────────────────────────────────────┘ │
│                 │                                          │
│ 💬 Messages: 4  │                                          │
│                 │                                          │
└─────────────────┴──────────────────────────────────────────┘

Key Features:
✅ Document selector dropdown
✅ Live document switching
✅ Document preview in sidebar
✅ Chat statistics
✅ Modern, responsive design
```

## Side-by-Side Comparison

### Document Management

**Gradio:**
```
Startup
   ↓
Auto-load first DOCX
   ↓
Fixed for entire session
   ↓
To change: Restart app
```

**Streamlit:**
```
Startup
   ↓
Auto-load first DOCX
   ↓
Select different doc from dropdown
   ↓
Click "Load Document"
   ↓
Chat history cleared
   ↓
New document ready
```

### Chat Flow

**Both interfaces use the same backend:**

```
User Query
   ↓
OpenAI Orchestrator (GPT-4o)
   ├──> Clarification Agent (entity extraction)
   │    └──> MiniRAG hybrid search
   │
   └──> AutoGen Search Agent
        └──> Document content retrieval
   ↓
Response displayed in chat
```

## Choosing an Interface

### Use Gradio if:
```
┌─────────────────────────────────────┐
│ ✅ You work with ONE document       │
│ ✅ You want simplest setup          │
│ ✅ You prefer clean, minimal UI     │
│ ✅ You're deploying to HF Spaces    │
│ ✅ You want custom themes           │
└─────────────────────────────────────┘
```

### Use Streamlit if:
```
┌─────────────────────────────────────┐
│ ✅ You need to switch documents     │
│ ✅ You want document preview        │
│ ✅ You prefer modern, polished UI   │
│ ✅ You're deploying to ST Cloud     │
│ ✅ You need chat analytics          │
└─────────────────────────────────────┘
```

## Launch Commands

### Gradio
```bash
# Simple launch
python run_app.py

# Access at:
http://localhost:8080
```

### Streamlit
```bash
# Simple launch
python run_streamlit.py

# Access at:
http://localhost:8082
```

### Both + Config
```bash
# Launch all applications
./scripts/start_all.sh

# Access at:
# Gradio:    http://localhost:8080
# Streamlit: http://localhost:8082
# Config:    http://localhost:8081

# Stop all
./scripts/stop_all.sh
```

## Mobile Experience

### Gradio Mobile
```
┌──────────────┐
│   Q&A Bot    │
├──────────────┤
│              │
│ [Chatbot]    │
│              │
│ 👤 Question  │
│              │
│ 🤖 Answer    │
│              │
├──────────────┤
│ [Input]      │
├──────────────┤
│ [Send] [Clr] │
└──────────────┘

Good, but basic
```

### Streamlit Mobile
```
┌──────────────┐
│ ☰ FAQ Bot    │
├──────────────┤
│              │
│ [Chatbot]    │
│              │
│ 👤 Question  │
│              │
│ 🤖 Answer    │
│              │
├──────────────┤
│ [Input ✏️]   │
└──────────────┘

Sidebar hidden,
better scrolling
```

## Developer Experience

### Gradio Code Structure
```python
# Global state
agent_runner = None

def chat_callback(message, history):
    global agent_runner
    response = agent_runner.process_query(message)
    return response

# Simple, direct
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    msg.submit(chat_callback, [msg, chatbot])
```

### Streamlit Code Structure
```python
# Session state
if 'agent_runner' not in st.session_state:
    st.session_state.agent_runner = None

# More structured
with st.sidebar:
    st.selectbox("Select Document", docs)

if prompt := st.chat_input():
    response = st.session_state.agent_runner.process_query(prompt)
    st.chat_message("assistant").markdown(response)
```

## Performance Characteristics

### Memory Usage
```
Gradio:    Lower    [▓▓▓░░░░░░░]  ~200MB
Streamlit: Higher   [▓▓▓▓▓░░░░░]  ~350MB
```

### Startup Time
```
Gradio:    Fast     [▓▓▓▓▓▓░░░░]  3-5s
Streamlit: Fast     [▓▓▓▓▓▓░░░░]  3-5s
```

### Concurrency
```
Gradio:    Shared   [▓▓▓░░░░░░░]  Global state
Streamlit: Isolated [▓▓▓▓▓▓▓▓▓▓]  Per-session
```

## Deployment Options

### Gradio → Hugging Face Spaces
```
1. Push code to GitHub
2. Create Space on huggingface.co
3. Select Gradio SDK
4. Add OPENAI_API_KEY to secrets
5. Deploy ✅
```

### Streamlit → Streamlit Cloud
```
1. Push code to GitHub
2. Connect repo at streamlit.io/cloud
3. Select src/streamlit_app.py
4. Add OPENAI_API_KEY to secrets
5. Deploy ✅
```

## Summary

Both interfaces provide the **same powerful AI capabilities**:
- ✅ Multi-agent architecture
- ✅ Hybrid search with MiniRAG
- ✅ Cost-optimized indexing
- ✅ DOCX/DOC/TXT support

The difference is in **user experience**:
- **Gradio**: Simpler, faster for single-document workflows
- **Streamlit**: Richer features for multi-document work

**Try both and choose what fits your workflow!**
