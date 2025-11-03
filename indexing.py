from MiniRAG.minirag import MiniRAG, QueryParam
from MiniRAG.minirag.utils import EmbeddingFunc
from lightrag.llm.openai import gpt_4o_complete, openai_embed
from langchain_text_splitters import RecursiveCharacterTextSplitter
from agents import Agent, Runner, trace
from docx_reader import Document
import os
import shutil
from dotenv import load_dotenv

load_dotenv()

# Function to create document objects from docx files
def create_documents_from_docx(path):
    # documents = []
    # for path in file_paths:
    doc = Document(path)
        # documents.append(doc)

    paragraphs = []
    for paragraph in doc.paragraphs:
        if paragraph.text.strip(): # only add non-empty paragraphs
            paragraphs.append(paragraph.text)

    return '\n\n'.join(paragraphs)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", ".", " ", ""]
)


rag = MiniRAG(
    working_dir="./kb",
    llm_model_func=gpt_4o_complete,
    llm_model_name="gpt-4o",
    embedding_func=EmbeddingFunc(
        embedding_dim=1536,
        max_token_size=8191,
        func=lambda texts: openai_embed(texts, model="text-embedding-3-small")
    )
)


docpath = "./docs/OneStream_Error_Handling_and_Mapping_Guide_inprogress.docx"

knowledge_base = create_documents_from_docx(docpath)

chunks = text_splitter.split_text(knowledge_base)
print(f"\n✂️ Получено чанков: {len(chunks)}")

print("\n--- Примеры чанков ---")
for i, chunk in enumerate(chunks[:3], 1):
    print(f"\nЧанк {i} (первые 150 символов):")
    print(chunk[:150] + "...")

# rag_storage_path = "./kb"
# if os.path.exists(rag_storage_path):
#     shutil.rmtree(rag_storage_path)

for chunk in chunks:
    rag.insert(chunk)