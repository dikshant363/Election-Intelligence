# Model Configuration Guide — Election Intelligence Platform v1.0.0

## Overview

The AI subsystem uses a pluggable `LLMProvider` abstraction that isolates all model-specific configuration from application logic. Switching models requires only environment variable changes — no code modifications.

---

## 1. Configuration Architecture

Model configuration is managed through `pydantic-settings` and loaded from the `.env` file or environment variables at startup.

```python
# Settings fields relevant to AI models
AI_PROVIDER: str = "openai"          # Active provider: openai | gemini | local
AI_MODEL: str = "gpt-4o"            # Model identifier
AI_TEMPERATURE: float = 0.2         # Lower = more deterministic
AI_MAX_TOKENS: int = 2048           # Max tokens in response
AI_TIMEOUT: float = 30.0            # Request timeout in seconds
EMBEDDING_MODEL: str = "text-embedding-3-small"  # Embedding model
EMBEDDING_DIMENSIONS: int = 1536    # Embedding vector size
```

---

## 2. Supported Models by Provider

### OpenAI

| Model | Use Case | Context Window | Best For |
| :--- | :--- | :--- | :--- |
| `gpt-4o` | Primary reasoning | 128K tokens | Complex election queries, RAG |
| `gpt-4-turbo` | Cost-efficient reasoning | 128K tokens | Production default |
| `gpt-3.5-turbo` | Fast, cheap | 16K tokens | Simple lookups |
| `text-embedding-3-small` | Embeddings | — | Vector search |
| `text-embedding-3-large` | High-quality embeddings | — | Production RAG |

### Google Gemini

| Model | Use Case | Context Window | Best For |
| :--- | :--- | :--- | :--- |
| `gemini-1.5-pro` | Primary reasoning | 1M tokens | Long document analysis |
| `gemini-1.5-flash` | Cost-efficient | 1M tokens | High-throughput scenarios |
| `text-embedding-004` | Embeddings | — | Vector search |

### Local / Self-Hosted

| Model | Framework | Use Case |
| :--- | :--- | :--- |
| `llama3` | Ollama | Air-gapped environments |
| `mistral` | Ollama | Privacy-sensitive deployments |
| Any GGUF model | LM Studio | Local development |

---

## 3. Environment Variable Reference

```bash
# Provider selection
AI_PROVIDER=openai               # openai | gemini | local

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_ORG_ID=org-...            # Optional, for organization accounts

# Google Gemini
GOOGLE_API_KEY=AIza...

# Local / Ollama
OLLAMA_BASE_URL=http://localhost:11434
LOCAL_MODEL_NAME=llama3

# Model behaviour
AI_MODEL=gpt-4o
AI_TEMPERATURE=0.2
AI_MAX_TOKENS=2048
AI_TIMEOUT=30.0

# Embeddings
EMBEDDING_PROVIDER=openai        # openai | gemini | local
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSIONS=1536
```

---

## 4. Per-Environment Model Recommendations

| Environment | Recommended Model | Reasoning |
| :--- | :--- | :--- |
| **Local development** | `ollama/llama3` or `gpt-3.5-turbo` | Low cost, fast iteration |
| **Staging** | `gpt-4o-mini` or `gemini-1.5-flash` | Realistic behaviour, controlled cost |
| **Production** | `gpt-4o` or `gemini-1.5-pro` | Maximum accuracy for election queries |

---

## 5. Changing Models

1. Update the relevant env var in `.env` or your secrets manager.
2. Restart the backend (`uvicorn` / `docker compose restart api`).
3. No code change required — the `LLMProvider` abstraction handles the rest.
4. Run a smoke test: `curl http://localhost:8000/api/v1/ai/query -d '{"prompt":"Who won the 2024 Lok Sabha election?"}'`

---

## 6. Token Budget Management

| Component | Token Budget |
| :--- | :--- |
| System prompt | ~500 tokens |
| Retrieved context (RAG) | ~2000 tokens |
| User query | ~200 tokens |
| Response | ≤2048 tokens |
| **Total** | **≤4748 tokens** |

Tune `AI_MAX_TOKENS` and the number of retrieved documents to fit within the model's context window.

---

## 7. Embedding Dimension Considerations

> [!IMPORTANT]
> If you change the embedding model and it produces a different vector dimension, you **must** re-index all documents. The vector store schema is tied to `EMBEDDING_DIMENSIONS`. Changing this requires a migration.

Steps to change embedding model safely:
1. Update `EMBEDDING_MODEL` and `EMBEDDING_DIMENSIONS`.
2. Create a migration to drop and recreate the vector column.
3. Run a full reindex: `POST /api/v1/search/reindex`.
4. Validate search quality before deploying to production.

---

## 8. Adding a New Model Provider

1. Implement the `LLMProvider` abstract interface in `backend/app/ai/providers/`.
2. Register the new provider in the provider factory.
3. Add required environment variables to `settings.py`.
4. Write unit tests in `tests/test_ai.py`.
5. Update this guide with the new provider's configuration options.
