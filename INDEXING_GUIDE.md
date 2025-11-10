# Document Indexing Guide

## Overview

The `indexing.py` script indexes documents from the `docs/` directory into a MiniRAG knowledge base for semantic search and question answering.

## Supported File Formats

- **DOCX** - Microsoft Word documents (.docx)
- **DOC** - Legacy Word documents (.doc)
- **TXT** - Plain text files (.txt)

## Usage

### Basic Indexing

Index all supported files in the `docs/` directory:

```bash
python indexing.py
```

This will:
- Scan the `docs/` folder for supported files
- Extract text content from each file
- Split content into chunks (500 chars with 200 overlap)
- Create embeddings and build knowledge graph
- Store in `kb/` directory

### Rebuild Knowledge Base

To clear the existing knowledge base and rebuild from scratch:

1. Edit `indexing.py`
2. Change `clear_existing=False` to `clear_existing=True` (line 119)
3. Run `python indexing.py`

**⚠️ Warning**: This will delete all existing indexed data!

### Preview Files to Index

See what files would be indexed without running the full process:

```bash
python demo_indexing.py
```

## Configuration

### Text Splitting Settings

Located in `indexing.py` (lines 57-61):

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,        # Size of each chunk
    chunk_overlap=200,     # Overlap between chunks
    length_function=len,
    separators=["\n\n", "\n", ".", " ", ""]
)
```

### Vector Search Threshold

The indexing script uses a threshold of `0.0` for maximum recall (line 75):

```python
vector_db_storage_cls_kwargs={
    "cosine_better_than_threshold": 0.0  # Accept all results
}
```

## Adding New Documents

1. Place your DOCX, DOC, or TXT files in the `docs/` folder
2. Run `python indexing.py`
3. New documents will be added to the existing knowledge base

## How It Works

### 1. Text Extraction

**DOCX/DOC files**:
- Extracts all paragraphs using `python-docx`
- Filters out empty paragraphs
- Joins with double newlines

**TXT files**:
- Reads file with UTF-8 encoding
- Falls back to Latin-1 if UTF-8 fails

### 2. Chunking

Text is split using `RecursiveCharacterTextSplitter`:
- Tries to split on paragraph boundaries (`\n\n`)
- Falls back to sentences (`.`), then words (` `)
- Maintains 200-character overlap for context

### 3. Knowledge Graph

MiniRAG creates:
- **Entities**: Key concepts extracted via LLM
- **Relationships**: Connections between entities
- **Chunks**: Original text segments
- **Embeddings**: Vector representations for semantic search

### 4. Storage Structure

```
kb/
├── vdb_entities.json           # Entity embeddings
├── vdb_entities_name.json      # Entity name embeddings
├── vdb_relationships.json      # Relationship embeddings
├── vdb_chunks.json            # Text chunk embeddings
├── chunk_entity_relation.json  # Knowledge graph
└── minirag.log                # Indexing logs
```

## Troubleshooting

### No files found

```
❌ No supported files found in ./docs
   Supported formats: DOCX, DOC, TXT
```

**Solution**: Add DOCX, DOC, or TXT files to the `docs/` folder

### Encoding errors (TXT files)

The script automatically tries UTF-8 first, then falls back to Latin-1. If you have files with other encodings, convert them to UTF-8:

```bash
iconv -f WINDOWS-1251 -t UTF-8 input.txt > output.txt
```

### Out of memory

For very large documents, you may need to:
1. Increase `chunk_size` to reduce total chunks
2. Process files one at a time
3. Increase available RAM

## Example Output

```
📚 Found 2 document(s) to index:
  - OneStream_Guide.docx (DOCX)
  - FAQ.txt (TXT)

📄 Processing: OneStream_Guide.docx
  ✂️  Split into 42 chunks

  --- Sample chunk from OneStream_Guide.docx ---
  This error contains a prevention of P&L MPC report...

  ⏳ Indexed 10/42 chunks...
  ⏳ Indexed 20/42 chunks...
  ⏳ Indexed 30/42 chunks...
  ⏳ Indexed 40/42 chunks...
  ✅ Successfully indexed 42 chunks from OneStream_Guide.docx

📄 Processing: FAQ.txt
  ✂️  Split into 3 chunks
  ✅ Successfully indexed 3 chunks from FAQ.txt

============================================================
✨ Indexing complete!
📊 Total documents processed: 2
📊 Total chunks indexed: 45
📂 Knowledge base location: ./kb
============================================================
```

## Integration with FAQ Bot

After indexing, the FAQ bot (`app.py`) automatically loads the knowledge base from `kb/` and uses it for:

1. **Document Q&A**: Answering questions about indexed content
2. **Clarification Agent**: Finding relevant entities for ambiguous queries
3. **Semantic Search**: Finding similar content across all documents

## Advanced Configuration

### Custom Directories

```python
index_all_documents(
    docs_dir="./my_documents",  # Custom input folder
    kb_dir="./my_kb",           # Custom KB location
    clear_existing=True
)
```

### Different Chunk Sizes

For technical documents with long sections:

```python
chunk_size=1000,      # Larger chunks
chunk_overlap=300,    # More overlap
```

For short FAQs:

```python
chunk_size=200,       # Smaller chunks
chunk_overlap=50,     # Less overlap
```
