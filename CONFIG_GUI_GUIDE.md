# Configuration GUI Guide

## Overview

The FAQ Bot includes a **separate** web-based configuration interface for document management and indexing. This is a standalone application that runs independently from the main chat interface, allowing you to restrict access to administrators only.

## Features

### 1. **Upload Documents** Tab
- Upload multiple documents at once
- Supported formats: **DOCX**, **DOC**, **TXT**
- Files are automatically saved to the `docs/` folder
- Real-time upload status with file size information

### 2. **Existing Documents** Tab
- View all documents currently in the library
- See file names and sizes
- Refresh the document list
- Delete documents you no longer need

### 3. **Indexing** Tab
- Trigger document indexing with a single click
- Monitor indexing progress and results
- Indexing creates a knowledge graph for better Q&A performance
- Shows detailed output from the indexing process

## How to Use

### Starting the Applications

**Important:** The FAQ Bot consists of TWO separate applications:

1. **Chat Application** (for end users) - Port 8080
2. **Config Application** (for administrators only) - Port 8081

#### Start Chat Application (Main)
```bash
source venv/bin/activate
python app.py
```
The chat interface will start at: **http://localhost:8080**

#### Start Config Application (Admin Only)
```bash
source venv/bin/activate
python config_app.py
```
The configuration interface will start at: **http://localhost:8081**

**Security Note:** In production, restrict access to port 8081 using:
- Firewall rules (allow only admin IPs)
- Reverse proxy with authentication (nginx, Apache)
- VPN or internal network access only
- Authentication middleware (see Security section below)

### Uploading Documents

1. Open **http://localhost:8081** in your browser (Config Application)
2. Go to the **📤 Upload Documents** tab
4. Click **Select Documents** or drag files into the upload area
5. Select one or more documents (DOCX, DOC, or TXT)
6. Click the **Upload** button
7. Check the upload status message

### Managing Documents

1. Go to the **📚 Existing Documents** sub-tab
2. View the list of uploaded documents with their sizes
3. To delete a document:
   - Enter the document name in the text field
   - Click the **🗑️ Delete** button
4. Click **🔄 Refresh List** to update the document list

### Running Indexing

1. Go to the **🔄 Indexing** sub-tab
2. Read the information about what indexing does
3. Click the **▶️ Run Indexing** button
4. Wait for the indexing process to complete (can take several minutes)
5. Check the output for success confirmation

**Note:** Indexing should be run whenever you:
- Upload new documents
- Delete documents
- Want to update the knowledge graph

### Querying Documents

1. After indexing, open **http://localhost:8080** in your browser (Chat Application)
2. The application will automatically load the first DOCX file
3. Ask questions about your documents
4. The bot will use the indexed knowledge graph for better answers

**Note:** End users only need access to port 8080 (chat interface). They do not need access to port 8081 (config interface).

## Technical Details

### File Storage
- Documents: `docs/` folder
- Knowledge base: `kb/` folder (auto-generated during indexing)
- Conversation history: `conversation_history.db` (SQLite)

### Indexing Process
The indexing process:
1. Reads all documents from `docs/` folder
2. Splits documents into chunks (500 chars, 200 overlap)
3. Extracts entities and relationships using GPT-4o-mini
4. Creates vector embeddings using text-embedding-3-small
5. Stores the knowledge graph in `kb/` folder

### Architecture
- **Chat Application**: `app.py` (port 8080) - User-facing chat interface
- **Config Application**: `config_app.py` (port 8081) - Admin-only document management
- **Config UI Module**: `config_ui.py` - Document management and indexing GUI components
- **Indexing Logic**: `indexing.py` - Multi-format document indexing

### Deployment Architecture

```
┌─────────────────────────────────────────────────────┐
│                   End Users                          │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │   app.py (8080)     │  ← Public access
         │   Chat Interface    │
         └─────────────────────┘
                   │
                   │ (shared file access)
                   │
         ┌─────────┴─────────┐
         │   docs/ folder    │
         │   kb/ folder      │
         └─────────┬─────────┘
                   │
                   │ (shared file access)
                   │
         ┌─────────────────────┐
         │ config_app.py       │  ← Admin access only
         │ (8081)              │     (firewall/auth)
         │ Config Interface    │
         └─────────────────────┘
                   ▲
                   │
┌──────────────────┴──────────────────────────────────┐
│              Administrators                          │
└─────────────────────────────────────────────────────┘
```

## Security Considerations

### Restricting Access to Config Application

**CRITICAL:** The config application (port 8081) should **never** be exposed to end users. Use one of these methods:

#### 1. Firewall Rules (Recommended for Production)
```bash
# Allow only specific admin IP
sudo ufw allow from 192.168.1.100 to any port 8081

# Block all other IPs
sudo ufw deny 8081
```

#### 2. Reverse Proxy with Authentication (nginx)
```nginx
server {
    listen 443 ssl;
    server_name admin.yoursite.com;

    location / {
        auth_basic "Administrator Area";
        auth_basic_user_file /etc/nginx/.htpasswd;
        proxy_pass http://localhost:8081;
    }
}
```

#### 3. SSH Tunnel (Development/Testing)
```bash
# On your local machine
ssh -L 8081:localhost:8081 user@server

# Access at http://localhost:8081
```

#### 4. VPN/Internal Network Only
- Run config app on internal network interface only
- Use VPN to access the internal network

#### 5. Docker Network Isolation
```yaml
services:
  chat:
    ports:
      - "8080:8080"  # Public

  config:
    ports:
      - "127.0.0.1:8081:8081"  # Localhost only
```

### Authentication Middleware (Optional)

For additional security, you can add Gradio authentication to `config_app.py`:

```python
demo.launch(
    server_name="0.0.0.0",
    server_port=8081,
    share=False,
    auth=("admin", "your-secure-password"),  # Add this line
    auth_message="Admin access required"
)
```

**Note:** This provides basic HTTP authentication. For production, use reverse proxy with proper authentication.

## Troubleshooting

### Upload Issues
- **Unsupported format**: Only DOCX, DOC, and TXT files are accepted
- **Permission errors**: Ensure the application has write access to `docs/` folder

### Indexing Issues
- **No documents found**: Upload documents before running indexing
- **Timeout**: Large documents may take >5 minutes; try smaller files
- **Missing indexing.py**: Ensure `indexing.py` exists in the project root

### Application Not Starting
- **Port already in use**: Kill the process on port 8080:
  ```bash
  lsof -ti:8080 | xargs kill -9
  ```
- **Missing dependencies**: Reinstall requirements:
  ```bash
  pip install -r requirements.txt
  ```

## API Keys

Make sure your `.env` file contains:
```
OPENAI_API_KEY=your-api-key-here
```

Without a valid API key, indexing and chat functionality will not work.

## Cost Considerations

- **Indexing**: Uses gpt-4o-mini (~$0.11 per 2MB document)
- **Runtime queries**: Uses gpt-4o (~$0.02 per query)
- **Embeddings**: Uses text-embedding-3-small (cost-efficient)

See `MODEL_OPTIMIZATION.md` for detailed cost analysis.

## Screenshots

### Upload Tab
Upload multiple documents with file type validation and real-time status.

### Existing Documents Tab
View all documents with sizes, refresh the list, and delete unwanted files.

### Indexing Tab
Run indexing with detailed progress output and success confirmation.

### Chat Tab
Query your documents with AI-powered answers based on the knowledge graph.

---

**Created with Claude Code**
