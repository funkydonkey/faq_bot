import os
from dotenv import load_dotenv
from agents import Agent, Runner, trace, function_tool, set_default_openai_key
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
# from indexing import rag
from MiniRAG.minirag import QueryParam, MiniRAG
from MiniRAG.minirag.utils import EmbeddingFunc
from lightrag.llm.openai import gpt_4o_complete, openai_embed
# import asyncio
load_dotenv(override=True)

class ContextUnit(BaseModel):
    """ A unit of context information from database. """
    entity: str = Field(..., description="The entity this context unit is about")
    score: str = Field(..., description="Score of relevance to the user's question")
    description: str = Field(..., description="The relevant text chunk from the database")

class ClarificationContext(BaseModel):
    """ Context retrieved that may be relevant for user's question. """
    context_units: List[ContextUnit] = Field(..., description="List of context units relevant to the user's question")

INSTRUCTIONS = """
You are a clarification agent designed to help support-agent that chattingwith clients. 
You will provide relevant context from database to support-agent and then he can make a follow-up questions to user.
Your task is to:    
1. Define potential terms from the given input.
2. For each term, search the database for relevant context units.
3. Return the context units in a structured format.
"""

# MiniRAG definition
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
        "cosine_better_than_threshold": 0.0  # Set to 0 to accept all results regardless of similarity score
    }
)



async def _direct_entity_search(user_input: str) -> str:
    """
    Fallback: Direct search in entities vector DB when mini mode returns empty results.
    Searches by entity descriptions rather than names.
    """
    entity_results = await rag.entities_vdb.query(user_input, top_k=10)

    # Format results as CSV
    entities_csv_lines = ["entity,score,description"]
    for result in entity_results:
        entity_name = result.get("entity_name", "unknown")
        score = result.get("distance", 0.0)
        description = result.get("description", "")[:200]  # Truncate long descriptions
        # Escape commas and quotes in CSV
        description = description.replace('"', '""').replace('\n', ' ')
        entities_csv_lines.append(f'"{entity_name}",{score:.3f},"{description}"')

    entities_csv = "\n".join(entities_csv_lines)

    formatted_result = f"""-----Entities-----
```csv
{entities_csv}
```"""

    print(f"\n--- Fallback: Retrieved {len(entity_results)} Entities via Direct Search ---")
    return formatted_result

@function_tool
async def retrieve_clarification_context(user_input: str) -> str:
    """
    Retrieve clarification context from database based on user input.
    Uses mini mode first, falls back to direct entity search if no entities found.

    Args:
        user_input: The input from the user that may need clarification

    Returns:
        List of relevant entities from database with descriptions and relevance scores.
    """
    # Try mini mode first (LLM-based entity extraction + reasoning)
    query_params = QueryParam(
        top_k=10,
        mode="mini",
        only_need_context=True,
        response_type="json"
    )

    results = await rag.aquery(user_input, query_params)
    print(f"\n--- Mini Mode Results ---\n{results[:500] if results else 'None'}")

    # Check if entities section is empty
    has_entities = False
    if results and "-----Entities-----" in results:
        # Extract entities section
        try:
            entities_section = results.split("-----Entities-----")[1].split("```")[1]
            # Check if there's more than just the header line
            lines = entities_section.strip().split('\n')
            if len(lines) > 1:  # More than just "entity,score,description" header
                has_entities = True
                print(f"✓ Mini mode found {len(lines)-2} entities")
        except (IndexError, AttributeError):
            pass

    # If mini mode didn't find entities, use fallback direct search
    if not has_entities:
        print("\n⚠ Mini mode returned no entities, using fallback direct search...")
        results = await _direct_entity_search(user_input)

    return results

clarification_agent = Agent(
    name="clarification_agent",
    model="gpt-4o",
    instructions=INSTRUCTIONS,
    tools=[retrieve_clarification_context],   
    output_type=ClarificationContext
    )

async def run_clarification_agent(user_input: str) -> ClarificationContext:
    """ Run the clarification agent to get relevant context for user input. """
    response = await Runner.run(clarification_agent, user_input)
    print(f"\n--- Clarification Agent Response ---\n{response.final_output}")
    return response.final_output


# test_input = "I can't login to OS"
# # test_results = retrieve_clarification_context(test_input)
# test_results = asyncio.run(run_clarification_agent(test_input))
# print(f"\n--- Test Results for input: '{test_input}' ---")
# print(test_results)