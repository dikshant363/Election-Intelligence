# Retrieval-Augmented Generation (RAG) & Hybrid Retrieval Guide

## Overview

The RAG platform combines PostgreSQL full-text lexical search (`PostgresFTSIndex`) with semantic vector search (`VectorStore`) using **Reciprocal Rank Fusion (RRF)**.

---

## Hybrid Retrieval Pipeline

```text
User Question
    │
    ├──> 1. Lexical Search (Postgres FTS via SearchService SAL) ──> Lexical Rank List
    │
    └──> 2. Semantic Search (Embeddings + Cosine VectorStore) ───> Semantic Rank List
                                                                        │
                                                                        ▼
                                                       3. Reciprocal Rank Fusion (RRF)
                                                                        │
                                                                        ▼
                                                       4. Top-K Context Assembly
```

---

## Reciprocal Rank Fusion (RRF) Formula

For document $d$ appearing in rank lists $R$:

$$RRF\_Score(d) = \sum_{r \in R} \frac{1}{k + rank(r)}$$

where $k = 60.0$ is the smoothing constant.

---

## Explainability & Citation Attribution

Every RAG answer returned by `AIService` includes structured source citations and explainability traces:

```json
{
  "answer": "Based on official election data...",
  "provider": "mock",
  "citations": [
    {
      "document_id": "elec_123",
      "entity_type": "election",
      "title": "Lok Sabha Election 2024",
      "snippet": "General Election for 18th Lok Sabha...",
      "relevance_score": 0.0322
    }
  ],
  "reasoning": {
    "retrieved_entities": ["election"],
    "retrieval_strategy": "hybrid_rrf",
    "confidence_score": 0.95,
    "evidence_references": ["Lok Sabha Election 2024 (elec_123)"]
  }
}
```
