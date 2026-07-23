# LLM & Embedding Provider Abstraction Guide

## Overview

The platform uses vendor-independent abstractions for LLMs (`LLMProvider`) and text embeddings (`EmbeddingProvider`).

---

## Supported Providers

```text
LLMProvider
├── MockProvider (Deterministic offline/testing)
├── OpenAIProvider (gpt-4o, gpt-4o-mini)
├── GeminiProvider (gemini-1.5-flash, gemini-1.5-pro)
├── ClaudeProvider (claude-3-5-sonnet, claude-3-haiku)
└── OllamaProvider (Local Llama3, Mistral, vLLM)
```

---

## Provider Registry & Fallback

The `ProviderRegistry` manages provider instances and provides automatic fallback to `MockProvider` if a requested vendor is unavailable or unconfigured:

```python
provider = llm_registry.get("gemini")
response = await provider.generate(request)
```

---

## Embedding Providers

```text
EmbeddingProvider
├── MockEmbeddingProvider (384d / custom)
├── OpenAIEmbeddings (text-embedding-3-small, 1536d)
└── GeminiEmbeddings (text-embedding-004, 768d)
```
