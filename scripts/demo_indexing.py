"""Demo script to show indexing capabilities without actually running full indexing"""
import os
import glob

def show_indexing_info(docs_dir="./docs"):
    """Show what files would be indexed"""
    supported_extensions = ['*.docx', '*.doc', '*.txt']
    doc_files = []
    for ext in supported_extensions:
        doc_files.extend(glob.glob(os.path.join(docs_dir, ext)))

    if not doc_files:
        print(f"❌ No supported files found in {docs_dir}")
        print(f"   Supported formats: DOCX, DOC, TXT")
        return

    print(f"\n{'='*60}")
    print(f"📚 Indexing Script - Supported Files")
    print(f"{'='*60}\n")

    print(f"Found {len(doc_files)} document(s) to index:\n")

    for doc_path in doc_files:
        file_ext = os.path.splitext(doc_path)[1].upper()
        file_size = os.path.getsize(doc_path)
        size_str = f"{file_size / 1024:.1f} KB" if file_size > 1024 else f"{file_size} bytes"
        print(f"  ✓ {os.path.basename(doc_path)}")
        print(f"    - Type: {file_ext[1:]} file")
        print(f"    - Size: {size_str}")
        print()

    print(f"{'='*60}")
    print(f"📋 Usage Instructions:")
    print(f"{'='*60}\n")
    print("To index all documents:")
    print("  python -m src.indexing")
    print()
    print("To rebuild knowledge base from scratch:")
    print("  # Edit src/indexing.py and set clear_existing=True")
    print()
    print("Supported file formats:")
    print("  • DOCX - Microsoft Word documents")
    print("  • DOC  - Legacy Word documents")
    print("  • TXT  - Plain text files")
    print()

if __name__ == "__main__":
    show_indexing_info()
