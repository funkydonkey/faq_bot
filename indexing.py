from MiniRAG.minirag import MiniRAG
from MiniRAG.minirag.utils import EmbeddingFunc
from lightrag.llm.openai import gpt_4o_complete, gpt_4o_mini_complete, openai_embed
from langchain_text_splitters import RecursiveCharacterTextSplitter
from docx_reader import Document
import os
import glob
from dotenv import load_dotenv

load_dotenv()

# Function to extract text from different file types
def extract_text_from_file(path):
    """
    Extract text content from a file (DOCX, DOC, or TXT).

    Args:
        path: Path to the file

    Returns:
        Extracted text content as string
    """
    file_ext = os.path.splitext(path)[1].lower()

    if file_ext in ['.docx', '.doc']:
        # Extract from Word documents
        doc = Document(path)
        paragraphs = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():  # only add non-empty paragraphs
                paragraphs.append(paragraph.text)
        return '\n\n'.join(paragraphs)

    elif file_ext == '.txt':
        # Extract from plain text files
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encoding if UTF-8 fails
            with open(path, 'r', encoding='latin-1') as f:
                return f.read()

    else:
        raise ValueError(f"Unsupported file type: {file_ext}")


def index_all_documents(docs_dir="./docs", kb_dir="./kb", clear_existing=False):
    """
    Index all documents (DOCX, DOC, TXT) from docs_dir into the knowledge base.

    Args:
        docs_dir: Directory containing documents to index
        kb_dir: Knowledge base directory
        clear_existing: If True, clear existing knowledge base before indexing
    """
    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    # Initialize MiniRAG with cost-efficient models
    rag = MiniRAG(
        working_dir=kb_dir,
        llm_model_func=gpt_4o_mini_complete,  # Using gpt-4o-mini for cost efficiency
        llm_model_name="gpt-4o-mini",
        llm_model_max_token_size=16384,  # gpt-4o-mini context window
        embedding_func=EmbeddingFunc(
            embedding_dim=1536,
            max_token_size=8191,
            func=lambda texts: openai_embed(texts, model="text-embedding-3-small")
        ),
        vector_db_storage_cls_kwargs={
            "cosine_better_than_threshold": 0.0  # Accept all results for better recall
        },
        # Entity extraction settings - conservative to reduce token usage
        entity_extract_max_gleaning=1,  # Default, reduces multiple extraction passes
        entity_summary_to_max_tokens=500,  # Limit entity summary length
    )

    # Clear existing knowledge base if requested
    if clear_existing and os.path.exists(kb_dir):
        import shutil
        print(f"🗑️  Clearing existing knowledge base at {kb_dir}")
        shutil.rmtree(kb_dir)

    # Find all supported document files in docs directory
    supported_extensions = ['*.docx', '*.doc', '*.txt']
    doc_files = []
    for ext in supported_extensions:
        doc_files.extend(glob.glob(os.path.join(docs_dir, ext)))

    if not doc_files:
        print(f"❌ No supported files found in {docs_dir}")
        print(f"   Supported formats: DOCX, DOC, TXT")
        return

    print(f"\n📚 Found {len(doc_files)} document(s) to index:")
    for doc_path in doc_files:
        file_ext = os.path.splitext(doc_path)[1].upper()
        print(f"  - {os.path.basename(doc_path)} ({file_ext})")

    # Process each document
    total_chunks = 0
    for doc_path in doc_files:
        doc_name = os.path.basename(doc_path)
        print(f"\n📄 Processing: {doc_name}")

        try:
            # Extract text from document
            knowledge_base = extract_text_from_file(doc_path)

            # Split into chunks
            chunks = text_splitter.split_text(knowledge_base)
            print(f"  ✂️  Split into {len(chunks)} chunks")

            # Show sample chunks
            if chunks:
                print(f"\n  --- Sample chunk from {doc_name} ---")
                print(f"  {chunks[0][:150]}...")

            # Insert chunks into RAG
            for i, chunk in enumerate(chunks, 1):
                rag.insert(chunk)
                if i % 10 == 0:  # Progress indicator every 10 chunks
                    print(f"  ⏳ Indexed {i}/{len(chunks)} chunks...")

            total_chunks += len(chunks)
            print(f"  ✅ Successfully indexed {len(chunks)} chunks from {doc_name}")

        except Exception as e:
            print(f"  ❌ Error processing {doc_name}: {str(e)}")

    print(f"\n{'='*60}")
    print(f"✨ Indexing complete!")
    print(f"📊 Total documents processed: {len(doc_files)}")
    print(f"📊 Total chunks indexed: {total_chunks}")
    print(f"📂 Knowledge base location: {kb_dir}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    # Index all documents from docs/ directory
    # Set clear_existing=True to rebuild the entire knowledge base from scratch
    index_all_documents(
        docs_dir="./docs",
        kb_dir="./kb",
        clear_existing=False  # Change to True to clear and rebuild KB
    )
