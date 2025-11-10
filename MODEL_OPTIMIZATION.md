# Model Optimization Guide

## Overview

This document explains the model choices across the FAQ bot system and how they balance cost vs. quality.

## Model Usage by Component

| Component | Model | Purpose | Token Usage | Why This Model? |
|-----------|-------|---------|-------------|-----------------|
| **indexing.py** | `gpt-4o-mini` | Entity extraction during indexing | High (once) | Cost-efficient for batch processing |
| **clarification_agent.py** | `gpt-4o` | Entity search (mini mode) | Medium | Quality needed for ambiguous queries |
| **openai_agent.py** | `gpt-4o` | Query orchestration | Low | User-facing, needs best quality |
| **autogen_agent.py** | `gpt-4o` | Document search | Medium | Precision needed for exact answers |
| **Embeddings** | `text-embedding-3-small` | Vector embeddings | Low | Most cost-efficient embedding model |

## Cost Comparison

### GPT Models (as of 2024)

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Relative Cost | Use Case |
|-------|----------------------|------------------------|---------------|----------|
| `gpt-4o` | $2.50 | $10.00 | 1x | Production queries |
| `gpt-4o-mini` | $0.15 | $0.60 | **16x cheaper** | Indexing, batch |
| `gpt-3.5-turbo` | $0.50 | $1.50 | 5x cheaper | Alternative |

### Embedding Models

| Model | Cost (per 1M tokens) | Dimensions | Use Case |
|-------|---------------------|------------|----------|
| `text-embedding-3-small` | $0.02 | 1536 | **Recommended** |
| `text-embedding-3-large` | $0.13 | 3072 | Higher precision |
| `text-embedding-ada-002` | $0.10 | 1536 | Legacy |

## Indexing Cost Calculation

### Example: 2MB DOCX Document

```
Document size: 2 MB ≈ 500,000 chars ≈ 125,000 tokens
Number of chunks: 125,000 / 500 = 250 chunks

Token usage per chunk:
- Input: ~1,500 tokens (chunk + system prompt)
- Output: ~300 tokens (entities + relationships)

Total tokens for indexing:
- Input: 250 × 1,500 = 375,000 tokens
- Output: 250 × 300 = 75,000 tokens

Cost with gpt-4o-mini:
- Input: 375,000 / 1,000,000 × $0.15 = $0.06
- Output: 75,000 / 1,000,000 × $0.60 = $0.05
- Total: $0.11 per document

Cost with gpt-4o (old):
- Input: 375,000 / 1,000,000 × $2.50 = $0.94
- Output: 75,000 / 1,000,000 × $10.00 = $0.75
- Total: $1.69 per document

Savings: 94% (15x cheaper!)
```

### Embeddings Cost

```
Embedding tokens: 125,000 tokens (same as document)

Cost with text-embedding-3-small:
125,000 / 1,000,000 × $0.02 = $0.0025

Total indexing cost per document:
$0.11 (LLM) + $0.0025 (embeddings) = ~$0.11
```

## Runtime Query Costs

### Typical User Query

```
Query: "How do I fix the PL MPC dashboard error?"

1. Clarification Agent (mini mode):
   - Input: ~2,000 tokens (query + entities)
   - Output: ~500 tokens (entity extraction)
   - Cost: $0.006 with gpt-4o

2. Orchestrator Agent:
   - Input: ~1,000 tokens (query + context)
   - Output: ~200 tokens (decision)
   - Cost: $0.004 with gpt-4o

3. Document Search Agent:
   - Input: ~3,000 tokens (query + document)
   - Output: ~300 tokens (answer)
   - Cost: $0.01 with gpt-4o

Total per query: ~$0.02
```

### Cost Reduction Strategies

**✅ Already Implemented:**
1. Using `gpt-4o-mini` for indexing (15x cheaper)
2. Using `text-embedding-3-small` for embeddings (6.5x cheaper than large)
3. Conservative chunking (500 chars) to reduce redundancy
4. Fallback direct search (no LLM for simple entity lookups)

**🔧 Optional Optimizations:**

#### 1. Use gpt-4o-mini for Clarification Agent

```python
# In clarification_agent.py
clarification_agent = Agent(
    name="clarification_agent",
    model="gpt-4o-mini",  # Change from gpt-4o
    instructions=INSTRUCTIONS,
    tools=[retrieve_clarification_context],
    output_type=ClarificationContext
)
```

**Savings**: 60% on clarification queries
**Trade-off**: Slightly lower entity extraction quality

#### 2. Cache Frequent Queries

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_entities(query: str):
    # Cache frequent entity lookups
    pass
```

**Savings**: 100% on repeated queries
**Trade-off**: Memory usage, stale results

#### 3. Batch Processing During Indexing

```python
# Process multiple chunks in one LLM call
batch_size = 5
for i in range(0, len(chunks), batch_size):
    batch = chunks[i:i+batch_size]
    rag.insert_batch(batch)  # Hypothetical batch API
```

**Savings**: ~30-40% on indexing
**Trade-off**: More complex error handling

## Current Configuration

### indexing.py

```python
rag = MiniRAG(
    llm_model_func=gpt_4o_mini_complete,  # ✓ Cost-efficient
    llm_model_name="gpt-4o-mini",
    llm_model_max_token_size=16384,
    entity_extract_max_gleaning=1,  # ✓ Single pass only
    entity_summary_to_max_tokens=500,  # ✓ Limit summary length
)
```

### clarification_agent.py

```python
rag = MiniRAG(
    llm_model_func=gpt_4o_complete,  # Quality over cost
    llm_model_name="gpt-4o",
    vector_db_storage_cls_kwargs={
        "cosine_better_than_threshold": 0.0  # ✓ Direct search fallback
    }
)

clarification_agent = Agent(
    model="gpt-4o",  # User-facing, needs quality
)
```

### openai_agent.py & autogen_agent.py

```python
model="gpt-4o"  # User-facing, needs best quality
```

## Recommendations by Use Case

### Development/Testing
- **Indexing**: `gpt-4o-mini` ✓ (already set)
- **Runtime**: `gpt-4o-mini` for faster testing
- **Embeddings**: `text-embedding-3-small` ✓ (already set)

### Production (Low Volume)
- **Indexing**: `gpt-4o-mini` ✓ (already set)
- **Runtime**: `gpt-4o` ✓ (already set) - best quality
- **Embeddings**: `text-embedding-3-small` ✓ (already set)

### Production (High Volume)
- **Indexing**: `gpt-4o-mini` ✓ (already set)
- **Runtime**: `gpt-4o-mini` for cost savings
- **Embeddings**: `text-embedding-3-small` ✓ (already set)
- **Cache**: Implement query caching

### Enterprise (Quality Critical)
- **Indexing**: `gpt-4o` for maximum entity extraction quality
- **Runtime**: `gpt-4o` ✓ (already set)
- **Embeddings**: `text-embedding-3-large` for better precision

## Monitoring Token Usage

### Using OpenAI Dashboard
1. Go to https://platform.openai.com/usage
2. Filter by date range
3. Check usage by model

### Programmatic Tracking

```python
import tiktoken

def estimate_tokens(text, model="gpt-4o"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# Before indexing
total_tokens = sum(estimate_tokens(chunk) for chunk in chunks)
estimated_cost = (total_tokens / 1_000_000) * 0.15  # gpt-4o-mini input
print(f"Estimated indexing cost: ${estimated_cost:.4f}")
```

## Summary

**✅ Current Optimization Level: Good**

- Indexing uses cost-efficient `gpt-4o-mini` (94% savings vs gpt-4o)
- Embeddings use cheapest viable model (`text-embedding-3-small`)
- Runtime uses quality models (`gpt-4o`) for best user experience
- Fallback mechanisms reduce unnecessary LLM calls

**💰 Monthly Cost Estimate (Example Workload):**

```
Indexing (one-time): 10 documents × $0.11 = $1.10
Runtime queries: 1,000 queries/month × $0.02 = $20
Total: ~$21/month
```

**📊 With Further Optimization (gpt-4o-mini everywhere):**

```
Indexing: $1.10 (same)
Runtime: 1,000 × $0.008 = $8
Total: ~$9/month (60% savings)
Trade-off: Slightly lower answer quality
```
