"""Configuration UI for document management and indexing."""
import os
import glob
import subprocess
import gradio as gr
from pathlib import Path


DOCS_DIR = "docs"


def get_existing_documents():
    """Get list of existing documents in docs folder."""
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR, exist_ok=True)
        return "No documents found."

    files = glob.glob(f"{DOCS_DIR}/*")
    if not files:
        return "No documents found."

    file_list = []
    for file_path in files:
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        size_mb = file_size / (1024 * 1024)
        file_list.append(f"📄 {file_name} ({size_mb:.2f} MB)")

    return "\n".join(file_list)


def upload_documents(files):
    """
    Upload documents to docs folder.

    Args:
        files: List of uploaded file objects from Gradio

    Returns:
        Status message
    """
    if not files:
        return "❌ No files selected.", get_existing_documents()

    # Ensure docs directory exists
    os.makedirs(DOCS_DIR, exist_ok=True)

    uploaded_files = []
    errors = []

    for file in files:
        try:
            # Get the file name
            file_name = os.path.basename(file.name)
            dest_path = os.path.join(DOCS_DIR, file_name)

            # Check file extension
            ext = Path(file_name).suffix.lower()
            if ext not in ['.docx', '.doc', '.txt']:
                errors.append(f"❌ {file_name}: Unsupported format (only DOCX, DOC, TXT)")
                continue

            # Copy file to docs folder
            with open(file.name, 'rb') as src:
                with open(dest_path, 'wb') as dst:
                    dst.write(src.read())

            uploaded_files.append(file_name)

        except Exception as e:
            errors.append(f"❌ {file_name}: {str(e)}")

    # Build status message
    status_parts = []

    if uploaded_files:
        status_parts.append(f"✅ Successfully uploaded {len(uploaded_files)} file(s):")
        for fname in uploaded_files:
            status_parts.append(f"  • {fname}")

    if errors:
        status_parts.append("\n⚠️ Errors:")
        status_parts.extend(f"  • {err}" for err in errors)

    status_message = "\n".join(status_parts) if status_parts else "❌ No files were uploaded."

    return status_message, get_existing_documents()


def run_indexing():
    """
    Run the indexing.py script to index all documents.

    Returns:
        Status message with indexing results
    """
    try:
        # Check if there are documents to index
        if not os.path.exists(DOCS_DIR):
            return "❌ No docs folder found. Please upload documents first."

        files = glob.glob(f"{DOCS_DIR}/*")
        if not files:
            return "❌ No documents found in docs folder. Please upload documents first."

        # Run indexing.py
        result = subprocess.run(
            ["python", "indexing.py"],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        if result.returncode == 0:
            # Success
            output_lines = result.stdout.strip().split('\n')
            # Get last few lines which usually contain the summary
            summary = '\n'.join(output_lines[-10:]) if len(output_lines) > 10 else result.stdout

            return f"✅ **Indexing completed successfully!**\n\n```\n{summary}\n```"
        else:
            # Error
            return f"❌ **Indexing failed:**\n\n```\n{result.stderr}\n```"

    except subprocess.TimeoutExpired:
        return "❌ Indexing timeout (>5 minutes). Try with smaller documents or check indexing.py for issues."
    except FileNotFoundError:
        return "❌ indexing.py not found. Make sure it exists in the project root."
    except Exception as e:
        return f"❌ Error running indexing: {str(e)}"


def delete_document(doc_name):
    """
    Delete a document from docs folder.

    Args:
        doc_name: Name of the document to delete

    Returns:
        Status message and updated document list
    """
    if not doc_name or doc_name.strip() == "":
        return "❌ Please enter a document name.", get_existing_documents()

    # Clean the name (remove emoji and size info if copied from list)
    doc_name = doc_name.strip()
    if doc_name.startswith("📄 "):
        doc_name = doc_name[2:].split(" (")[0].strip()

    file_path = os.path.join(DOCS_DIR, doc_name)

    if not os.path.exists(file_path):
        return f"❌ Document '{doc_name}' not found.", get_existing_documents()

    try:
        os.remove(file_path)
        return f"✅ Deleted '{doc_name}'", get_existing_documents()
    except Exception as e:
        return f"❌ Error deleting '{doc_name}': {str(e)}", get_existing_documents()


def create_config_interface():
    """Create the Gradio configuration interface."""

    with gr.Blocks(title="Document Management", theme=gr.themes.Soft()) as demo:
        gr.Markdown(
            """
            # ⚙️ Document Management & Indexing

            Upload documents and trigger indexing to update the knowledge base.
            """
        )

        with gr.Tab("📤 Upload Documents"):
            gr.Markdown("### Upload New Documents")
            gr.Markdown("Supported formats: **DOCX**, **DOC**, **TXT**")

            file_upload = gr.File(
                label="Select Documents",
                file_count="multiple",
                file_types=[".docx", ".doc", ".txt"]
            )

            upload_btn = gr.Button("Upload", variant="primary", size="lg")
            upload_status = gr.Textbox(
                label="Upload Status",
                lines=5,
                interactive=False
            )

        with gr.Tab("📚 Existing Documents"):
            gr.Markdown("### Current Documents in Library")

            doc_list = gr.Textbox(
                label="Documents",
                lines=10,
                interactive=False,
                value=get_existing_documents()
            )

            refresh_btn = gr.Button("🔄 Refresh List", size="sm")

            gr.Markdown("### Delete Document")
            with gr.Row():
                delete_input = gr.Textbox(
                    label="Document Name",
                    placeholder="Enter document name to delete...",
                    scale=3
                )
                delete_btn = gr.Button("🗑️ Delete", variant="stop", scale=1)

            delete_status = gr.Textbox(
                label="Delete Status",
                lines=2,
                interactive=False
            )

        with gr.Tab("🔄 Indexing"):
            gr.Markdown(
                """
                ### Run Indexing

                Indexing creates a knowledge graph from your documents using MiniRAG.

                **What happens during indexing:**
                - Documents are split into chunks
                - Entities and relationships are extracted
                - Vector embeddings are created
                - Knowledge base is stored in `kb/` folder

                **Note:** Indexing can take several minutes for large documents.
                """
            )

            index_btn = gr.Button("▶️ Run Indexing", variant="primary", size="lg")
            indexing_status = gr.Textbox(
                label="Indexing Status",
                lines=15,
                interactive=False,
                placeholder="Click 'Run Indexing' to start..."
            )

        # Event handlers
        upload_btn.click(
            fn=upload_documents,
            inputs=[file_upload],
            outputs=[upload_status, doc_list]
        )

        refresh_btn.click(
            fn=lambda: get_existing_documents(),
            outputs=[doc_list]
        )

        delete_btn.click(
            fn=delete_document,
            inputs=[delete_input],
            outputs=[delete_status, doc_list]
        )

        index_btn.click(
            fn=run_indexing,
            outputs=[indexing_status]
        )

    return demo


if __name__ == "__main__":
    # Run standalone for testing
    demo = create_config_interface()
    demo.launch(server_port=8081)
