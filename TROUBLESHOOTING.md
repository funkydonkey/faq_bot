# FAQ Bot - Troubleshooting Guide

Solutions to common problems when installing and running the FAQ Bot.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Configuration Issues](#configuration-issues)
3. [Runtime Errors](#runtime-errors)
4. [Performance Issues](#performance-issues)
5. [API and Network Issues](#api-and-network-issues)
6. [Document Processing Issues](#document-processing-issues)
7. [Advanced Debugging](#advanced-debugging)

---

## Installation Issues

### ❌ "python3.12: command not found"

**Problem**: Python 3.12 is not installed or not in PATH

**Solutions**:

**macOS**:
```bash
# Install via Homebrew
brew install python@3.12

# Add to PATH (add to ~/.zshrc or ~/.bash_profile)
export PATH="/usr/local/opt/python@3.12/bin:$PATH"
```

**Windows**:
1. Download from [python.org](https://www.python.org/downloads/)
2. Run installer with "Add Python to PATH" checked
3. Restart Command Prompt

**Linux**:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.12 python3.12-venv

# Verify
python3.12 --version
```

---

### ❌ "pip: command not found"

**Problem**: pip is not installed

**Solutions**:

```bash
# Use pip3 instead
pip3 install -r requirements.txt

# Or install pip
python3.12 -m ensurepip --upgrade
```

---

### ❌ "error: Microsoft Visual C++ 14.0 or greater is required" (Windows)

**Problem**: Missing C++ build tools

**Solution**:

1. Download [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Install "Desktop development with C++"
3. Restart Command Prompt
4. Retry: `pip install -r requirements.txt`

---

### ❌ "Permission denied" during pip install

**Problem**: Insufficient permissions

**Solutions**:

```bash
# Option 1: Install for user only
pip install --user -r requirements.txt

# Option 2: Use virtual environment (recommended)
python3.12 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

### ❌ Dependencies fail to install

**Problem**: Package conflicts or network issues

**Solutions**:

```bash
# Upgrade pip first
pip install --upgrade pip setuptools wheel

# Install with verbose output to see what fails
pip install -r requirements.txt -v

# Install problematic packages individually
pip install gradio
pip install openai
# etc.
```

---

## Configuration Issues

### ❌ "OPENAI_API_KEY not found in environment variables"

**Problem**: .env file is missing or incorrect

**Diagnosis**:
```bash
# Check if .env exists
ls -la .env

# View contents (be careful - contains secrets!)
cat .env
```

**Solutions**:

**Missing .env file**:
```bash
# Create it
echo "OPENAI_API_KEY=sk-proj-your-key-here" > .env
```

**Incorrect format**:
```bash
# Edit .env - should look like this:
OPENAI_API_KEY=sk-proj-abc123...

# NO quotes, NO spaces around =
# NOT: OPENAI_API_KEY = "sk-proj-..."
# NOT: export OPENAI_API_KEY=sk-proj-...
```

**Wrong location**:
```bash
# .env must be in project root
faq_bot/
├── .env          # HERE
├── run_app.py
└── src/
```

---

### ❌ ".env file exists but key still not found"

**Problem**: Environment not being loaded

**Solutions**:

1. **Restart the application** - changes to .env require restart

2. **Check file encoding**:
   ```bash
   # Should be plain text, not Word doc or PDF
   file .env
   # Output should be: .env: ASCII text
   ```

3. **Manually set environment variable** (temporary):
   ```bash
   # macOS/Linux
   export OPENAI_API_KEY="sk-proj-your-key"
   python run_app.py

   # Windows
   set OPENAI_API_KEY=sk-proj-your-key
   python run_app.py
   ```

---

## Runtime Errors

### ❌ "ModuleNotFoundError: No module named 'X'"

**Problem**: Missing dependency or wrong virtual environment

**Diagnosis**:
```bash
# Check if venv is activated
which python  # Should show path to venv/bin/python

# Check installed packages
pip list
```

**Solutions**:

```bash
# Make sure venv is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt

# If specific module missing
pip install module-name
```

---

### ❌ "ImportError: cannot import name 'X' from 'Y'"

**Problem**: Version conflict or incorrect import

**Solutions**:

```bash
# Check installed version
pip show package-name

# Reinstall with exact version
pip install --force-reinstall package-name==version

# Clear cache and reinstall all
pip cache purge
pip install -r requirements.txt --force-reinstall
```

---

### ❌ "Address already in use" / "Port 8080 already in use"

**Problem**: Another process is using the port

**Solutions**:

**macOS/Linux**:
```bash
# Find process using port 8080
lsof -ti:8080

# Kill it
lsof -ti:8080 | xargs kill

# Or kill both ports
lsof -ti:8080 | xargs kill
lsof -ti:8081 | xargs kill
```

**Windows**:
```cmd
# Find process
netstat -ano | findstr :8080

# Kill it (replace PID with actual process ID)
taskkill /PID 12345 /F
```

**Alternative**: Change the port:
```python
# Edit src/app.py, line ~205
server_port=8090,  # Changed from 8080
```

---

### ❌ Application starts but shows blank page

**Problem**: Browser cache or wrong URL

**Solutions**:

1. **Try hard refresh**:
   - Chrome/Firefox: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)

2. **Clear browser cache**

3. **Try different browser**

4. **Check URL**:
   - Should be `http://localhost:8080` (not `https://`)
   - Try `http://127.0.0.1:8080`

5. **Check console for errors**:
   - Right-click → Inspect → Console tab

---

### ❌ "No DOCX file found in the 'docs' folder"

**Problem**: No documents to query

**Solutions**:

```bash
# Check docs folder exists
ls docs/

# Create if missing
mkdir -p docs

# Add a test document
echo "This is a test FAQ. How do I test? You are testing now!" > docs/test.txt

# Or copy real documents
cp /path/to/your/file.docx docs/
```

---

## Performance Issues

### ⚠️ Application is slow to start

**Possible causes**:
- Large documents being loaded
- Slow disk I/O
- Network issues

**Solutions**:

1. **Check document size**:
   ```bash
   ls -lh docs/
   ```

2. **Start with smaller documents first**

3. **Check system resources**:
   ```bash
   # CPU and memory usage
   top  # macOS/Linux
   ```

---

### ⚠️ Queries take too long (>30 seconds)

**Possible causes**:
- Large knowledge base
- Complex question
- Slow OpenAI API response

**Solutions**:

1. **Check API status**: [status.openai.com](https://status.openai.com)

2. **Simplify question**: Try shorter, more direct questions

3. **Check internet speed**:
   ```bash
   ping 8.8.8.8
   ```

4. **Monitor API calls**: Check OpenAI dashboard for latency

---

### ⚠️ Indexing takes forever

**Normal times**:
- 500KB doc: ~30 seconds
- 2MB doc: ~2 minutes
- 10MB doc: ~10 minutes

**If much slower**:

1. **Check internet speed** - indexing uploads data to OpenAI

2. **Check system resources**:
   ```bash
   top  # Look for high CPU/memory usage
   ```

3. **Process in batches**: Index 1-2 documents at a time

---

## API and Network Issues

### ❌ "RateLimitError: Rate limit exceeded"

**Problem**: Too many requests to OpenAI API

**Solutions**:

1. **Wait 1 minute** and try again

2. **Check your tier**: [platform.openai.com/account/limits](https://platform.openai.com/account/limits)

3. **Upgrade OpenAI account** for higher limits

4. **Add delays** between requests (for batch processing):
   ```python
   import time
   time.sleep(1)  # Wait 1 second between calls
   ```

---

### ❌ "AuthenticationError: Incorrect API key"

**Problem**: Invalid or expired API key

**Solutions**:

1. **Check .env file**:
   ```bash
   cat .env
   # Key should start with sk-proj- or sk-
   ```

2. **Verify key is valid**:
   - Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - Check if key is listed and active

3. **Create new key** if expired or invalid

4. **Update .env** with new key:
   ```bash
   echo "OPENAI_API_KEY=sk-proj-new-key-here" > .env
   ```

5. **Restart application**

---

### ❌ "Connection timeout" / "Network unreachable"

**Problem**: Cannot reach OpenAI servers

**Solutions**:

1. **Check internet connection**:
   ```bash
   ping api.openai.com
   ```

2. **Check firewall**: Make sure Python can access internet

3. **Check proxy settings**: If behind corporate firewall

4. **Disable VPN** temporarily to test

5. **Check OpenAI status**: [status.openai.com](https://status.openai.com)

---

### ❌ "InsufficientQuotaError: You exceeded your quota"

**Problem**: No credits in OpenAI account

**Solutions**:

1. **Add payment method**: [platform.openai.com/account/billing](https://platform.openai.com/account/billing)

2. **Add credits** to account

3. **Check usage**: [platform.openai.com/usage](https://platform.openai.com/usage)

4. **Set usage limits** to avoid surprises

---

## Document Processing Issues

### ❌ "Error processing document: [Errno 2] No such file"

**Problem**: Document path is wrong

**Solutions**:

```bash
# Check exact file location
ls -la docs/

# Verify file permissions
ls -l docs/your-file.docx

# Make sure filename matches exactly (case-sensitive on macOS/Linux)
```

---

### ❌ "UnicodeDecodeError: 'utf-8' codec can't decode"

**Problem**: File encoding issues with TXT files

**Solutions**:

**Automatic** (already handled in code):
```python
# indexing.py automatically tries:
# 1. UTF-8
# 2. Latin-1 (fallback)
```

**Manual fix**:
```bash
# Convert file to UTF-8
iconv -f ISO-8859-1 -t UTF-8 oldfile.txt > newfile.txt
```

---

### ❌ "No text extracted from DOCX file"

**Problem**: DOCX might be corrupted or empty

**Solutions**:

1. **Open file manually** to verify it has content

2. **Try re-saving** the file in Word

3. **Convert to different format**:
   - Save as newer .docx format
   - Or save as .txt

4. **Check file size**:
   ```bash
   ls -lh docs/your-file.docx
   # Should be >1KB if it has content
   ```

---

### ❌ "Document indexed but queries return no results"

**Problem**: Knowledge graph might be empty or query doesn't match content

**Diagnosis**:
```bash
# Check knowledge base exists
ls -la kb/

# Should see files like:
# - graph_chunk_entity_relation.graphml
# - vdb_chunks.json
```

**Solutions**:

1. **Re-index with clear_existing=True**:
   ```python
   # Edit src/indexing.py, line ~165
   clear_existing=True  # Changed from False
   ```

2. **Try different questions**:
   - Use exact phrases from document
   - Try simpler questions first

3. **Check threshold setting** in `src/clarification_agent.py:43`:
   ```python
   "cosine_better_than_threshold": 0.0  # Should be 0.0
   ```

---

## Advanced Debugging

### Enable Verbose Logging

**For application**:
```python
# Edit src/app.py, add at top:
import logging
logging.basicConfig(level=logging.DEBUG)
```

**For indexing**:
```python
# Edit src/indexing.py, add print statements:
print(f"Processing chunk {i}: {chunk[:100]}...")
```

---

### Check Gradio Version

```bash
pip show gradio
# Should be >=4.0.0
```

If wrong version:
```bash
pip install --upgrade gradio
```

---

### Inspect Knowledge Base

```python
# Run in Python interpreter
python
>>> import json
>>> with open('kb/vdb_chunks.json', 'r') as f:
...     data = json.load(f)
>>> print(len(data))  # Number of chunks
>>> print(data[0])    # First chunk
```

---

### Test OpenAI Connection Directly

```python
# test_openai.py
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

Run:
```bash
python test_openai.py
```

---

### Check Virtual Environment

```bash
# Are you in venv?
which python
# Should show: /path/to/faq_bot/venv/bin/python

# What packages are installed?
pip list

# Where is Python looking for modules?
python -c "import sys; print('\n'.join(sys.path))"
```

---

### Verify File Structure

```bash
# Run structure test
python test_structure.py

# Should show 23/23 passed
```

---

### Reset Everything

If all else fails:

```bash
# 1. Deactivate venv
deactivate

# 2. Delete venv
rm -rf venv/

# 3. Delete knowledge base
rm -rf kb/

# 4. Delete conversation history
rm -f conversation_history.db

# 5. Recreate venv
python3.12 -m venv venv
source venv/bin/activate

# 6. Reinstall dependencies
pip install -r requirements.txt

# 7. Re-index documents
python -m src.indexing

# 8. Restart application
python run_app.py
```

---

## Getting More Help

### Check Application Logs

If using `start_both.sh`:
```bash
tail -f logs/chat.log
tail -f logs/config.log
```

### Common Log Messages

**Normal**:
```
✅ Document loaded: your-file.docx
Running on local URL:  http://0.0.0.0:8080
```

**Warning** (can ignore):
```
WARNING: FLAML automl is not available
```

**Error** (needs fixing):
```
ERROR: OPENAI_API_KEY not found
ERROR: No DOCX file found
```

### Report Issues

When asking for help, include:

1. **Python version**: `python --version`
2. **Operating system**: macOS/Windows/Linux
3. **Error message**: Full traceback
4. **Steps to reproduce**: What you did before error
5. **Environment**: `pip list`

---

## Quick Checklist

When something doesn't work, verify:

- [ ] Python 3.12 is installed
- [ ] Virtual environment is activated (`(venv)` shows in prompt)
- [ ] All dependencies installed (`pip list` shows gradio, openai, etc.)
- [ ] .env file exists with valid API key
- [ ] Documents are in `docs/` folder
- [ ] No other process using ports 8080/8081
- [ ] Internet connection is working
- [ ] OpenAI API is operational (check status.openai.com)

---

Still stuck? Review the [Installation Guide](INSTALLATION_GUIDE.md) for step-by-step setup instructions.
