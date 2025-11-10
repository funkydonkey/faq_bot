"""Debug script to understand why entities are empty in mini mode"""
import asyncio
from clarification_agent import retrieve_clarification_context

async def main():
    test_queries = [
        "I can see No Access in PL MPC dashboard",
        "PL MPC dashboard",
        "P&L MPC REPORT"  # Exact match with entity name
    ]

    for query in test_queries:
        print(f"\n{'='*80}")
        print(f"Testing query: '{query}'")
        print(f"{'='*80}")
        result = await retrieve_clarification_context(query)
        print("\n")

if __name__ == "__main__":
    asyncio.run(main())
