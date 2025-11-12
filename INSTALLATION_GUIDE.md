# FAQ Bot - Complete Installation Guide for Beginners

This guide will walk you through installing and running the FAQ Bot step-by-step, even if you're new to Python or command-line tools.

## Table of Contents

1. [What You'll Need](#what-youll-need)
2. [Step 1: Install Python 3.12](#step-1-install-python-312)
3. [Step 2: Download the Project](#step-2-download-the-project)
4. [Step 3: Set Up Virtual Environment](#step-3-set-up-virtual-environment)
5. [Step 4: Install Dependencies](#step-4-install-dependencies)
6. [Step 5: Get OpenAI API Key](#step-5-get-openai-api-key)
7. [Step 6: Configure the Application](#step-6-configure-the-application)
8. [Step 7: Add Your Documents](#step-7-add-your-documents)
9. [Step 8: Run the Application](#step-8-run-the-application)
10. [Troubleshooting](#troubleshooting)

---

## What You'll Need

- **A computer** running macOS, Windows, or Linux
- **Internet connection** for downloading software and API access
- **OpenAI API account** (costs money - around $0.11 per document + $0.02 per question)
- **Your documents** in DOCX, DOC, or TXT format
- **About 30 minutes** for first-time setup

---

## Step 1: Install Python 3.12

### Why Python 3.12?
This project requires **exactly Python 3.12** because it uses specific libraries that only work with this version.

### macOS Installation

1. **Open Terminal** (you can find it using Spotlight Search - press `⌘ + Space` and type "Terminal")

2. **Install Homebrew** (if you don't have it):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. **Install Python 3.12**:
   ```bash
   brew install python@3.12
   ```

4. **Verify installation**:
   ```bash
   python3.12 --version
   ```

   You should see: `Python 3.12.x`

### Windows Installation

1. **Download Python 3.12**:
   - Go to [python.org/downloads](https://www.python.org/downloads/)
   - Click "Download Python 3.12.x"

2. **Run the installer**:
   - ✅ **IMPORTANT**: Check the box "Add Python 3.12 to PATH"
   - Click "Install Now"

3. **Verify installation**:
   - Open Command Prompt (search for "cmd" in Start menu)
   - Type:
     ```cmd
     python --version
     ```
   - You should see: `Python 3.12.x`

### Linux Installation

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev

# Fedora
sudo dnf install python3.12

# Verify
python3.12 --version
```

---

## Step 2: Download the Project

### Option A: Using Git (Recommended)

1. **Install Git** (if not installed):
   - macOS: `brew install git`
   - Windows: Download from [git-scm.com](https://git-scm.com/)
   - Linux: `sudo apt install git`

2. **Clone the repository**:
   ```bash
   cd ~
   git clone <repository-url> faq_bot
   cd faq_bot
   ```

### Option B: Download ZIP

1. Download the project as a ZIP file
2. Extract it to a folder (e.g., `~/faq_bot` or `C:\Users\YourName\faq_bot`)
3. Open Terminal/Command Prompt and navigate to that folder:
   ```bash
   cd ~/faq_bot          # macOS/Linux
   cd C:\Users\YourName\faq_bot  # Windows
   ```

---

## Step 3: Set Up Virtual Environment

A virtual environment keeps this project's dependencies separate from other Python projects.

### What is a Virtual Environment?
Think of it as a separate "container" for this project's Python libraries, so they don't interfere with other projects.

### Create Virtual Environment

**macOS/Linux:**
```bash
# Make sure you're in the faq_bot folder
cd ~/faq_bot

# Create virtual environment
python3.12 -m venv venv

# Activate it
source venv/bin/activate
```

**Windows:**
```cmd
# Make sure you're in the faq_bot folder
cd C:\Users\YourName\faq_bot

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate
```

### How to Know It's Activated?

You should see `(venv)` at the beginning of your command prompt:
```
(venv) username@computer:~/faq_bot$
```

### Deactivating (when you're done)

Simply type:
```bash
deactivate
```

---

## Step 4: Install Dependencies

Dependencies are the libraries this project needs to work.

**Make sure your virtual environment is activated** (you see `(venv)` in the prompt), then run:

```bash
pip install -r requirements.txt
```

This will take **2-5 minutes** and install about 50+ packages. You'll see a lot of text scrolling - this is normal!

### What if you get errors?

**Error: "pip: command not found"**
```bash
# Try using pip3 instead
pip3 install -r requirements.txt
```

**Error: "Microsoft Visual C++ required" (Windows)**
- Download and install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

**Error: Permission denied**
```bash
# On macOS/Linux, add --user flag
pip install --user -r requirements.txt
```

---

## Step 5: Get OpenAI API Key

The FAQ Bot uses OpenAI's GPT models to answer questions.

### Create OpenAI Account

1. Go to [platform.openai.com/signup](https://platform.openai.com/signup)
2. Sign up with your email
3. Add payment method (required for API access)
   - ⚠️ **Note**: This will cost real money, but it's cheap:
     - Indexing a 2MB document: ~$0.11
     - Each question answered: ~$0.02

### Get Your API Key

1. Log in to [platform.openai.com](https://platform.openai.com/)
2. Click your profile icon (top right) → "API keys"
3. Click "Create new secret key"
4. Give it a name (e.g., "FAQ Bot")
5. **Copy the key** - it looks like: `sk-proj-abc123...`
   - ⚠️ **Save it somewhere safe** - you won't see it again!

---

## Step 6: Configure the Application

### Create .env File

This file stores your secret API key.

**macOS/Linux:**
```bash
# Make sure you're in the faq_bot folder
cd ~/faq_bot

# Create .env file
echo "OPENAI_API_KEY=your-key-here" > .env
```

**Windows:**
```cmd
# Make sure you're in the faq_bot folder
cd C:\Users\YourName\faq_bot

# Create .env file
echo OPENAI_API_KEY=your-key-here > .env
```

### Edit .env File

1. **Open the file** in a text editor:
   - macOS: `open .env` or use TextEdit
   - Windows: `notepad .env`
   - Linux: `nano .env`

2. **Replace `your-key-here` with your actual API key**:
   ```
   OPENAI_API_KEY=sk-proj-abc123xyz789...
   ```

3. **Save and close** the file

### Verify .env File

```bash
cat .env
```

You should see:
```
OPENAI_API_KEY=sk-proj-...
```

⚠️ **Security Note**: Never share this file or commit it to Git!

---

## Step 7: Add Your Documents

### Create docs Folder

If it doesn't exist already:

```bash
mkdir -p docs
```

### Add Your Documents

Copy your documents into the `docs/` folder:

**macOS/Linux:**
```bash
cp /path/to/your/document.docx docs/
cp /path/to/your/faq.txt docs/
```

**Windows:**
```cmd
copy C:\path\to\your\document.docx docs\
copy C:\path\to\your\faq.txt docs\
```

**Or use GUI:**
- Open the `docs/` folder in your file explorer
- Drag and drop your documents there

### Supported File Types

- ✅ `.docx` - Microsoft Word documents
- ✅ `.doc` - Legacy Word documents
- ✅ `.txt` - Plain text files

### How Many Documents?

You can add as many as you want, but keep in mind:
- Each document costs money to index (~$0.11 per 2MB)
- More documents = longer indexing time
- Start with 1-2 documents to test

---

## Step 8: Run the Application

### Option A: Chat Application Only (Recommended for First Time)

This is the main interface where users ask questions.

1. **Make sure virtual environment is activated**:
   ```bash
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

2. **Run the chat app**:
   ```bash
   python run_app.py
   ```

3. **Wait for it to start** - you'll see:
   ```
   Running on local URL:  http://0.0.0.0:8080
   ```

4. **Open your browser** and go to:
   ```
   http://localhost:8080
   ```

5. **Ask a question** about your document!

### Option B: Both Applications (Chat + Admin Config)

Run both the chat interface AND the admin configuration interface:

1. **Make sure virtual environment is activated**

2. **Make the script executable** (first time only):
   ```bash
   chmod +x scripts/start_both.sh  # macOS/Linux
   ```

3. **Run the script**:
   ```bash
   ./scripts/start_both.sh  # macOS/Linux
   ```

   **Windows users**: Run each app in separate command prompts:
   ```cmd
   # Command Prompt 1
   python run_app.py

   # Command Prompt 2 (open a new one)
   python run_config.py
   ```

4. **Access the applications**:
   - **Chat (Users)**: http://localhost:8080
   - **Config (Admin)**: http://localhost:8081

### Understanding the Two Applications

| Application | Port | Purpose | Who Uses It |
|-------------|------|---------|-------------|
| Chat | 8080 | Ask questions about documents | End users |
| Config | 8081 | Upload documents, run indexing | Administrators |

---

## Using the Applications

### Chat Application (Port 8080)

1. **Open** http://localhost:8080
2. **Wait** for document to load (you'll see a green checkmark)
3. **Type** your question in the text box
4. **Click** "Send" or press Enter
5. **Read** the AI's response

**Example questions**:
- "What is the main topic of this document?"
- "How do I reset my password?"
- "What are the requirements for..."

### Config Application (Port 8081)

#### Upload Documents

1. **Open** http://localhost:8081
2. **Click** "Browse Files"
3. **Select** your DOCX, DOC, or TXT files
4. **Click** "Upload Documents"
5. **Wait** for confirmation

#### Index Documents

After uploading new documents, you need to index them:

1. **Click** the "Indexing" tab
2. **Click** "Run Indexing"
3. **Wait** (this takes 1-5 minutes per document)
4. **See** the results showing how many chunks were indexed

⚠️ **Note**: You only need to index documents once. After that, they're in the knowledge base permanently.

---

## Stopping the Application

### If You Ran `run_app.py` or `run_config.py`

Press `Ctrl + C` in the terminal window

### If You Ran `start_both.sh`

```bash
./scripts/stop_both.sh
```

Or manually:
```bash
# Find the processes
ps aux | grep python

# Kill them (replace XXXX with process ID)
kill XXXX XXXX
```

---

## Troubleshooting

### "Module not found" errors

**Problem**: Missing dependencies

**Solution**:
```bash
# Make sure venv is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### "OPENAI_API_KEY not found"

**Problem**: .env file is missing or incorrect

**Solution**:
```bash
# Check if .env exists
ls -la .env

# View contents
cat .env

# Should show: OPENAI_API_KEY=sk-proj-...
```

If missing, go back to [Step 6](#step-6-configure-the-application)

### "No documents found"

**Problem**: No documents in docs/ folder

**Solution**:
```bash
# Check docs folder
ls docs/

# Add documents
cp /path/to/your/document.docx docs/
```

### "Port 8080 already in use"

**Problem**: Another application is using that port

**Solution 1 - Kill the process**:
```bash
# macOS/Linux
lsof -ti:8080 | xargs kill

# Windows
netstat -ano | findstr :8080
taskkill /PID <process_id> /F
```

**Solution 2 - Use different port**:
Edit `src/app.py`, find line ~205:
```python
server_port=8080,  # Change to 8090 or another port
```

### "OpenAI API rate limit"

**Problem**: Making too many requests too fast

**Solution**: Wait 1 minute and try again, or upgrade your OpenAI account tier

### Application is slow or freezing

**Problem**: Large documents or complex questions

**Solution**:
- Wait a bit longer (indexing can take time)
- Use smaller documents to test first
- Check your internet connection

### Can't access from another device

**Problem**: Application only accessible on localhost

**Solution**:
The apps are configured to bind to `0.0.0.0`, which should allow access from other devices on your network. Access using:
```
http://your-computer-ip:8080
```

To find your IP:
```bash
# macOS/Linux
ifconfig | grep "inet "

# Windows
ipconfig
```

---

## Next Steps After Installation

### 1. Test with a Simple Document

Start with a small test document (1-2 pages) to verify everything works:

```bash
echo "This is a test FAQ. Question: How do I test? Answer: You're testing right now!" > docs/test.txt
python run_app.py
```

Visit http://localhost:8080 and ask: "How do I test?"

### 2. Index Your Real Documents

Once testing works:
1. Add your real documents to `docs/`
2. Run the config app: `python run_config.py`
3. Open http://localhost:8081
4. Click "Run Indexing" tab and index all documents

### 3. Monitor Costs

Check your OpenAI usage:
1. Go to [platform.openai.com/usage](https://platform.openai.com/usage)
2. Monitor your API costs
3. Set up usage limits if needed

### 4. Read More Documentation

- `QUICK_START.md` - Quick reference guide
- `README.md` - Full project documentation
- `CLAUDE.md` - Architecture details

---

## Getting Help

### Check Logs

If something goes wrong, check the logs:

```bash
# If using start_both.sh
tail -f logs/chat.log
tail -f logs/config.log
```

### Common Issues

| Problem | File to Check | Solution |
|---------|--------------|----------|
| Import errors | Terminal output | Reinstall dependencies |
| API errors | .env file | Check API key |
| No documents | docs/ folder | Add documents |
| Port conflicts | Terminal output | Kill other processes |

### Still Stuck?

1. Read the error message carefully
2. Check the [Troubleshooting](#troubleshooting) section above
3. Search for the error message online
4. Check OpenAI's status page: [status.openai.com](https://status.openai.com)

---

## Summary Checklist

Before running the app, make sure you've completed:

- [ ] Installed Python 3.12
- [ ] Downloaded/cloned the project
- [ ] Created virtual environment (`python3.12 -m venv venv`)
- [ ] Activated virtual environment (`source venv/bin/activate`)
- [ ] Installed dependencies (`pip install -r requirements.txt`)
- [ ] Created .env file with OpenAI API key
- [ ] Added documents to docs/ folder
- [ ] Ready to run: `python run_app.py`

---

## Cost Estimate

Here's what it costs to run this application:

### Initial Setup (One Time)
- Python 3.12: **Free**
- Project download: **Free**
- OpenAI account: **Free** (requires payment method)

### Usage Costs (OpenAI API)

**Indexing** (one time per document):
- Small document (500KB): ~$0.03
- Medium document (2MB): ~$0.11
- Large document (10MB): ~$0.55

**Runtime** (each question):
- Simple question: ~$0.01
- Complex question: ~$0.03

**Example monthly cost**:
- 10 documents indexed (2MB each): $1.10 (one time)
- 100 questions per day: $2.00/day = $60/month
- **Total first month**: ~$61

💡 **Tip**: Start small! Index 1-2 documents and ask a few questions to test before scaling up.

---

Congratulations! You should now have a working FAQ Bot installation. Happy querying! 🎉
