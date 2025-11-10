"""Test MiniRAG threshold configuration"""
import asyncio
from MiniRAG.minirag import QueryParam, MiniRAG
from MiniRAG.minirag.utils import EmbeddingFunc
from lightrag.llm.openai import gpt_4o_complete, openai_embed
from dotenv import load_dotenv

load_dotenv(override=True)

# MiniRAG with lowered threshold
rag = MiniRAG(
    working_dir="./kb",
    llm_model_func=gpt_4o_complete,
    llm_model_name="gpt-4o",
    embedding_func=EmbeddingFunc(
        embedding_dim=1536,
        max_token_size=8191,
        func=lambda texts: openai_embed(texts, model="text-embedding-3-small")
    ),
    vector_db_storage_cls_kwargs={
        "cosine_better_than_threshold": 0.1  # Lowered from default 0.2
    }
)

async def test_query(query_text):
    """Test query with configured threshold"""
    print(f"\n{'='*60}")
    print(f"Testing query: '{query_text}'")
    print(f"{'='*60}")

    query_params = QueryParam(
        top_k=10,
        mode="mini",
        only_need_context=True,
        response_type="json"
    )

    results = await rag.aquery(query_text, query_params)
    print(f"\nResults:\n{results}")
    return results

async def main():
    # Test queries
    test_queries = [
        "No Access in PL MPC dashboard",
        "PL MPC dashboard",
        "I can't login to OS"
    ]

    for query in test_queries:
        await test_query(query)
        await asyncio.sleep(1)  # Small delay between queries

if __name__ == "__main__":
    asyncio.run(main())
