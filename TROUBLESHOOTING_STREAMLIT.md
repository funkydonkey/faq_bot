# Streamlit Troubleshooting Guide

## Common Issues and Solutions

### 1. ImportError: attempted relative import with no known parent package

**Error:**
```
ImportError: attempted relative import with no known parent package
Traceback:
File "/path/to/faq_bot/src/streamlit_app.py", line 22, in <module>
    from openai_agent import OpenAIAgentRunner
```

**Cause:** Streamlit is running the app file directly, and Python can't resolve relative imports.

**Solution:** Always use the provided run script:

```bash
# ✅ Correct way
python run_streamlit.py

# ❌ Wrong way (may cause import errors)
streamlit run src/streamlit_app.py
```

**Why?** The `run_streamlit.py` script:
- Sets the correct working directory
- Ensures proper Python path configuration
- Uses absolute path to the Streamlit app

---

### 2. Module Not Found: sentence_transformers, openai, etc.

**Error:**
```
ModuleNotFoundError: No module named 'sentence_transformers'
```

**Cause:** Dependencies not installed or wrong Python environment.

**Solution:**

```bash
# 1. Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install all dependencies
pip install -r requirements.txt

# 3. Verify installation
pip list | grep -E "(streamlit|sentence-transformers|openai)"

# 4. Run the app
python run_streamlit.py
```

---

### 3. Port Already in Use

**Error:**
```
OSError: [Errno 48] Address already in use
```

**Cause:** Another application is using port 8082.

**Solution A - Change Port:**

Edit `run_streamlit.py` and change the port:

```python
subprocess.run([
    sys.executable, "-m", "streamlit", "run",
    streamlit_app,
    "--server.port=8083",  # Changed from 8082
    "--server.address=0.0.0.0"
])
```

**Solution B - Kill Existing Process:**

```bash
# Find process using port 8082
lsof -ti:8082

# Kill it
kill -9 $(lsof -ti:8082)

# Or on Windows
netstat -ano | findstr :8082
taskkill /PID <PID> /F
```

---

### 4. API Key Not Found

**Error:**
```
⚠️ OPENAI_API_KEY not found in environment variables.
```

**Cause:** Missing or incorrectly configured `.env` file.

**Solution:**

```bash
# 1. Create .env file in project root
cd /path/to/faq_bot
echo "OPENAI_API_KEY=sk-your-key-here" > .env

# 2. Verify file exists
cat .env

# 3. Restart the app
python run_streamlit.py
```

---

### 5. No Documents Found

**Error in UI:**
```
No DOCX files found in the 'docs' folder.
```

**Cause:** Empty or missing `docs/` directory.

**Solution:**

```bash
# 1. Create docs directory if missing
mkdir -p docs

# 2. Add DOCX files
cp your-document.docx docs/

# 3. Verify files
ls -la docs/

# 4. Refresh browser (F5)
```

---

### 6. Document Won't Load

**Symptoms:** Click "Load Document" but nothing happens or error appears.

**Possible Causes & Solutions:**

**A. Corrupted DOCX file:**
```bash
# Test file with python-docx
python -c "from docx import Document; doc = Document('docs/yourfile.docx'); print('OK')"
```

**B. File permissions:**
```bash
# Check permissions
ls -l docs/

# Fix if needed
chmod 644 docs/*.docx
```

**C. Large file:**
- Streamlit may timeout on very large files (>10MB)
- Try splitting the document or using a smaller test file first

---

### 7. Chat History Not Clearing

**Symptoms:** Click "Clear Chat" but messages remain.

**Solution:**

1. **Try hard refresh:**
   - Chrome/Edge: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
   - Firefox: `Ctrl+F5` or `Cmd+Shift+R`

2. **Clear browser cache:**
   - Go to browser settings
   - Clear cached images and files
   - Restart browser

3. **Clear Streamlit cache:**
   ```bash
   streamlit cache clear
   ```

4. **Restart the app:**
   ```bash
   # Stop the app (Ctrl+C)
   # Restart
   python run_streamlit.py
   ```

---

### 8. Session State Issues

**Symptoms:** App behaves unexpectedly, shows old data, or crashes randomly.

**Solution:**

```python
# Add this to streamlit_app.py (already included)
import streamlit as st

# Force rerun
st.rerun()

# Clear all session state
for key in list(st.session_state.keys()):
    del st.session_state[key]
```

**Or restart fresh:**
```bash
# Close browser tab
# Stop app (Ctrl+C)
# Clear cache
streamlit cache clear
# Restart
python run_streamlit.py
```

---

### 9. Slow Performance

**Symptoms:** App is sluggish, responses take long time.

**Causes & Solutions:**

**A. Large knowledge base:**
- MiniRAG loads entire KB into memory
- Check KB size: `du -sh kb/`
- Solution: Re-index with smaller chunks

**B. Many documents:**
- Each document selector refresh scans `docs/`
- Solution: Keep only active documents in `docs/`

**C. Browser cache:**
- Clear browser cache
- Disable browser extensions

**D. Network issues:**
- OpenAI API calls may be slow
- Check internet connection
- Use `--server.runOnSave=false` to reduce reloads

---

### 10. Blank Screen on Startup

**Symptoms:** Browser shows blank page at `localhost:8082`

**Solutions:**

1. **Check server is running:**
   ```bash
   # Look for this output:
   # You can now view your Streamlit app in your browser.
   # Local URL: http://localhost:8082
   ```

2. **Check firewall:**
   - Ensure port 8082 is not blocked
   - Try `http://127.0.0.1:8082` instead of `localhost`

3. **Check browser console:**
   - Press F12
   - Look for JavaScript errors
   - Try different browser

4. **Verify Python version:**
   ```bash
   python --version  # Should be 3.12.x
   ```

---

## Advanced Debugging

### Enable Debug Mode

Add this to the top of `src/streamlit_app.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check System Paths

```python
import sys
print("Python paths:")
for path in sys.path:
    print(f"  {path}")
```

### Test Import Chain

```bash
# Run the test script
python test_streamlit_import.py
```

### View Streamlit Logs

Streamlit logs to:
- **Mac/Linux:** `~/.streamlit/logs/`
- **Windows:** `%userprofile%\.streamlit\logs\`

```bash
# View latest log
tail -f ~/.streamlit/logs/streamlit.log
```

---

## Still Having Issues?

### Collect Debug Information

```bash
# 1. Python version
python --version

# 2. Streamlit version
streamlit --version

# 3. Installed packages
pip list > installed_packages.txt

# 4. System info
uname -a  # Mac/Linux
systeminfo  # Windows

# 5. Run test
python test_streamlit_import.py > test_output.txt 2>&1
```

### Create a Minimal Test

Create `test_minimal.py`:

```python
import streamlit as st

st.title("Minimal Test")
st.write("If you see this, Streamlit is working!")

if st.button("Test Button"):
    st.success("Button works!")
```

Run it:
```bash
streamlit run test_minimal.py
```

If this works but the main app doesn't, the issue is in the FAQ Bot code.

---

## Comparison: Gradio vs Streamlit Issues

If Streamlit doesn't work but you need the app running, use Gradio instead:

```bash
# Gradio is more straightforward
python run_app.py

# Access at http://localhost:8080
```

Both interfaces use the same backend, so functionality is identical!

---

## Quick Fixes Checklist

- [ ] Virtual environment activated?
- [ ] All dependencies installed? (`pip install -r requirements.txt`)
- [ ] `.env` file exists with `OPENAI_API_KEY`?
- [ ] Documents in `docs/` folder?
- [ ] Port 8082 available?
- [ ] Using `python run_streamlit.py` (not `streamlit run src/...`)?
- [ ] Python 3.12 installed?
- [ ] Tried browser hard refresh? (Ctrl+Shift+R)
- [ ] Tried clearing Streamlit cache? (`streamlit cache clear`)
- [ ] Checked terminal for error messages?

---

## Contact & Resources

- **Main README:** See [README.md](README.md) for general setup
- **Streamlit Docs:** https://docs.streamlit.io
- **FAQ Bot Issues:** Check project documentation
- **Alternative UI:** Use Gradio if Streamlit has persistent issues
