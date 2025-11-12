# 👋 Welcome to FAQ Bot!

**A smart document Q&A system powered by AI**

This guide will help you get started, whether you're a beginner or an experienced developer.

---

## 🚀 Quick Navigation

### New Users (Never Used This Before)
👉 **Start here**: [Installation Guide](INSTALLATION_GUIDE.md)

This comprehensive guide walks you through:
- Installing Python 3.12
- Setting up the project
- Getting your OpenAI API key
- Running your first query

**Time required**: ~30 minutes

---

### Experienced Users (Already Set Up)
👉 **Start here**: [Quick Start](QUICK_START.md)

Quick commands for:
- Running the applications
- Adding documents
- Common tasks

**Time required**: ~2 minutes

---

### Troubleshooting (Something Broke)
👉 **Start here**: [Troubleshooting Guide](TROUBLESHOOTING.md)

Solutions for:
- Installation errors
- Runtime problems
- API issues
- Performance problems

---

### Understanding the System (How It Works)
👉 **Start here**: [Architecture Guide](ARCHITECTURE.md)

Visual explanations of:
- System components
- Data flow
- Technology stack
- Scalability

---

## 📋 What is FAQ Bot?

FAQ Bot is an AI-powered system that:

✅ **Reads your documents** (DOCX, DOC, TXT)
✅ **Builds a knowledge graph** using AI
✅ **Answers questions** about document content
✅ **Provides context** through intelligent search

### Example Use Cases

| Industry | Use Case |
|----------|----------|
| **Customer Support** | Answer common questions from help docs |
| **HR** | Query employee handbooks and policies |
| **Legal** | Search contract templates and guides |
| **Education** | Interactive course material Q&A |
| **Healthcare** | Query medical protocols and procedures |

---

## 🎯 What You Can Do

### For End Users (Port 8080)

1. **Ask questions** about your documents
2. **Get instant answers** powered by AI
3. **See relevant context** from source material
4. **Natural conversation** - ask follow-up questions

### For Administrators (Port 8081)

1. **Upload documents** (DOCX, DOC, TXT)
2. **Index documents** to build knowledge base
3. **Manage documents** (view, delete)
4. **Monitor indexing** progress

---

## 💰 Cost Overview

### One-Time Setup
- Software: **FREE** (open source)
- OpenAI account: **FREE** (requires payment method)

### Usage Costs (OpenAI API)
- **Indexing**: ~$0.11 per 2MB document (one time)
- **Queries**: ~$0.02 per question

### Example Monthly Cost

**Small Team** (10 documents, 100 questions/day):
- Indexing: $1.10 (one time)
- Queries: $2/day × 30 days = $60/month
- **Total first month**: ~$61

**Light Usage** (5 documents, 20 questions/day):
- Indexing: $0.55 (one time)
- Queries: $0.40/day × 30 days = $12/month
- **Total first month**: ~$13

💡 **Tip**: Start small! Index 1-2 documents and test with a few questions before scaling up.

---

## ⚡ Quick Setup (5 Steps)

If you're comfortable with command line:

```bash
# 1. Create virtual environment
python3.12 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API key
echo "OPENAI_API_KEY=your-key-here" > .env

# 4. Add documents
cp your-document.docx docs/

# 5. Run!
python run_app.py
# Open http://localhost:8080
```

For detailed instructions, see [Installation Guide](INSTALLATION_GUIDE.md).

---

## 📁 Project Structure at a Glance

```
faq_bot/
│
├── 🚀 RUN THESE
│   ├── run_app.py          # Chat application (users)
│   └── run_config.py       # Config application (admins)
│
├── 📦 Source Code
│   └── src/                # All Python modules
│
├── 📄 Your Content
│   └── docs/               # Put your DOCX/DOC/TXT files here
│
├── 📚 Documentation
│   ├── START_HERE.md       # This file!
│   ├── INSTALLATION_GUIDE.md
│   ├── QUICK_START.md
│   ├── TROUBLESHOOTING.md
│   └── ARCHITECTURE.md
│
└── ⚙️ Configuration
    └── .env                # Your API key (create this)
```

---

## 🎓 Learning Path

### Day 1: Get It Running
1. Read [Installation Guide](INSTALLATION_GUIDE.md)
2. Complete setup steps
3. Test with a simple document
4. Ask a few questions

**Goal**: See your first AI-powered answer!

### Day 2: Understand the System
1. Read [Architecture Guide](ARCHITECTURE.md)
2. Understand data flow
3. Explore the three-layer agent system
4. Learn about MiniRAG knowledge graph

**Goal**: Understand how it works under the hood

### Day 3: Customize and Scale
1. Add more documents
2. Experiment with different questions
3. Monitor costs and performance
4. Explore advanced features

**Goal**: Make it work for your use case

---

## 🛠️ Common Tasks

### I want to...

**...run the chat application**
```bash
python run_app.py
# Open http://localhost:8080
```

**...add new documents**
```bash
# Copy files to docs/
cp my-doc.docx docs/

# Run config app
python run_config.py
# Open http://localhost:8081
# Click "Run Indexing"
```

**...test if it's working**
```bash
# Create test file
echo "Test FAQ: How do I test? You're testing now!" > docs/test.txt

# Run app
python run_app.py

# Ask: "How do I test?"
```

**...check my costs**
- Visit [platform.openai.com/usage](https://platform.openai.com/usage)

**...stop the application**
```bash
# Press Ctrl+C in terminal
```

---

## ⚠️ Important Notes

### Security

**Port 8081 (Config App) is ADMIN ONLY**
- Can upload/delete documents
- Can trigger expensive indexing operations
- Should be restricted via firewall/VPN in production

**Your .env file contains secrets**
- Never commit to Git
- Never share publicly
- Keep it secure

### Privacy

**Data sent to OpenAI**:
- ⚠️ Document chunks (during indexing)
- ⚠️ User questions (during queries)

**Data kept local**:
- ✅ Full documents (in `docs/`)
- ✅ Knowledge graph (in `kb/`)
- ✅ Chat history (in `conversation_history.db`)

### Performance

**Suitable for**:
- ✅ Small teams (1-50 users)
- ✅ Internal tools
- ✅ Document sets up to 100MB
- ✅ 100-1000 queries/day

**Not suitable for**:
- ❌ High-traffic public websites
- ❌ Real-time chat (response time: 2-10s)
- ❌ Massive datasets (100GB+)

---

## 🆘 Need Help?

### Step 1: Check Documentation
- [Installation Guide](INSTALLATION_GUIDE.md) - Setup issues
- [Troubleshooting](TROUBLESHOOTING.md) - Error solutions
- [Quick Start](QUICK_START.md) - Common commands

### Step 2: Check Logs
```bash
# If using start_both.sh
tail -f logs/chat.log
tail -f logs/config.log
```

### Step 3: Verify Checklist
- [ ] Python 3.12 installed
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] .env file with valid API key
- [ ] Documents in docs/ folder
- [ ] Internet connection working

### Step 4: Read Error Messages
Error messages usually tell you exactly what's wrong:
- "Module not found" → Install dependencies
- "API key not found" → Check .env file
- "Port already in use" → Kill other processes

---

## 🎉 Success Criteria

You'll know it's working when:

✅ Application starts without errors
✅ Browser shows Gradio interface
✅ Document loads (green checkmark)
✅ Questions get answered
✅ Responses reference your documents

---

## 📖 Document Guide Index

| Document | When to Read | Time Required |
|----------|-------------|---------------|
| **START_HERE.md** | First time visiting (this file!) | 5 min |
| **[INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)** | Setting up from scratch | 30 min |
| **[QUICK_START.md](QUICK_START.md)** | Daily use reference | 2 min |
| **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** | When errors occur | 5-15 min |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | Understanding system design | 15 min |
| **README.md** | Complete project overview | 10 min |
| **CLAUDE.md** | Developer documentation | 20 min |

---

## 🚦 Next Steps

### For First-Time Users
👉 Go to [Installation Guide](INSTALLATION_GUIDE.md)

### For Returning Users
👉 Go to [Quick Start](QUICK_START.md)

### For Developers
👉 Go to [Architecture Guide](ARCHITECTURE.md)

---

**Ready to get started? Let's go!** 🚀

Choose your path above and begin your FAQ Bot journey!

---

*Made with Claude Code - An AI-powered document Q&A system*
