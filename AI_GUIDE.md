# AI Intelligence & Retrieval Platform Guide

## Overview

The **AI Intelligence Layer** (`backend/app/ai/`) provides vendor-independent Retrieval-Augmented Generation (RAG), hybrid retrieval, explainable responses with source citations, and provider orchestration across OpenAI, Google Gemini, Anthropic Claude, and local Ollama models.

---

## Architectural Principles

```text
User
 ↓
REST API (/api/v1/ai/)
 ↓
AIService
 ↓
├── AIGuardrails (Prompt injection, safety, length limits)
├── HybridRetriever (Reciprocal Rank Fusion over SAL & VectorStore)
├── PromptOrchestrator (Token budgeting & versioned system prompts)
├── LLMProvider (OpenAI, Gemini, Claude, Ollama, Mock adapters)
├── CitationGenerator (Source attribution & reasoning traces)
└── RAGEvaluator (Precision, recall, grounding score metrics)
```

1. **Strict Layer Isolation**: AI services and tools communicate **exclusively** through the Application Layer (`QueryHandlers`) and Search Platform (`SearchService` SAL).
2. **Provider Agnosticism**: Application logic depends strictly on `LLMProvider` and `EmbeddingProvider` abstractions.
3. **No Direct Database Access**: LLMs and tools never query PostgreSQL models directly.

---

## Core Components

| Module | Location | Purpose |
| :--- | :--- | :--- |
| **Providers** | `backend/app/ai/providers/` | `LLMProvider` abstraction, vendor adapters, and fallback registry |
| **Embeddings** | `backend/app/ai/embeddings/` | `EmbeddingProvider` abstraction and vendor vectorizers |
| **Vector Store** | `backend/app/ai/vector/` | Vector store abstraction & cosine similarity engine |
| **Hybrid Retrieval**| `backend/app/ai/retrieval/` | RRF fusion combining lexical FTS search and semantic vector search |
| **Prompts** | `backend/app/ai/prompts/` | System prompts, context assembly, and token budgeting |
| **Guardrails** | `backend/app/ai/guardrails/` | Prompt injection detection, PII filtering, and safety checks |
| **Citations** | `backend/app/ai/citation/` | Source document attribution and reasoning trace generation |
| **Tools** | `backend/app/ai/tools/` | AI tools interacting with Application & Search layers |
| **Evaluation** | `backend/app/ai/evaluation/` | Precision, recall, grounding score, and latency tracking |

---

## API Endpoints

- `POST /api/v1/ai/query` — Execute single-turn RAG query
- `POST /api/v1/ai/chat` — Execute multi-turn conversation RAG
- `POST /api/v1/ai/stream` — Stream SSE response tokens
- `GET /api/v1/ai/providers` — List registered LLM providers
- `GET /api/v1/ai/metrics` — View platform AI performance & grounding metrics
