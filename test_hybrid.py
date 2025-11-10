"""Test hybrid approach: mini mode with fallback to direct search"""
import asyncio
from clarification_agent import retrieve_clarification_context

async def test_queries():
    test_cases = [
        "I can see No Access in PL MPC dashboard",  # Should trigger fallback
        "I can't login",  # Might work in mini mode
        "OKTA authentication error"  # Should work in mini mode
    ]

    for query in test_cases:
        print(f"\n{'='*80}")
        print(f"TESTING: '{query}'")
        print(f"{'='*80}")

        # Call the actual function_tool (this will be wrapped)
        # We need to import the internal function for testing
        from clarification_agent import rag, QueryParam, _direct_entity_search

        # Simulate what the function_tool does
        query_params = QueryParam(
            top_k=10,
            mode="mini",
            only_need_context=True,
            response_type="json"
        )

        results = await rag.aquery(query, query_params)
        print(f"\n--- Mini Mode Results (first 500 chars) ---")
        print(results[:500] if results else 'None')

        # Check if entities section is empty
        has_entities = False
        if results and "-----Entities-----" in results:
            try:
                entities_section = results.split("-----Entities-----")[1].split("```")[1]
                lines = entities_section.strip().split('\n')
                if len(lines) > 1:
                    has_entities = True
                    print(f"\n✓ Mini mode found {len(lines)-1} entities")
            except (IndexError, AttributeError):
                pass

        if not has_entities:
            print("\n⚠ Using fallback direct search...")
            fallback_result = await _direct_entity_search(query)
            print(f"\nFallback result (first 500 chars):\n{fallback_result[:500]}")

        print("\n")

if __name__ == "__main__":
    asyncio.run(test_queries())
