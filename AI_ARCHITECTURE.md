# AI Architecture

## 1. Overview
The AI subsystem (`backend/app/ai/`) powers the intelligent querying capabilities of the Election Intelligence Platform v1.0.0. By providing a natural language interface over structured election data, it solves the problem of complex data accessibility for end users. At its core, the `AIService` (`backend/app/ai/services/__init__.py`) orchestrates query execution, seamlessly blending robust retrieval with generative AI.

## 2. Hybrid RAG Design
The architecture employs a Hybrid RAG (Retrieval-Augmented Generation) approach.
- **BM25 Retrieval:** Ensures high precision for exact keyword matches (e.g., specific candidate names or constituency codes).
- **Vector Embeddings:** Captures semantic meaning for conceptual queries.
- **Fusion:** Results from both pipelines are merged and scored. Configurable weights (e.g., 0.6 BM25, 0.4 Vector) prioritize exact matches while still surfacing semantically relevant context.

## 3. LLMProvider Abstraction
The `LLMProvider` interface abstracts interactions with Large Language Models.
- **Supported Backends:** OpenAI, Gemini, and Local Models.
- **Extensibility:** To add a new provider, implement the base `LLMProvider` class methods (`generate`, `stream_generate`) and register the provider in the service factory.

## 4. Vector Store Abstraction
The `vector/` submodule abstracts vector database interactions.
- **Interface:** Provides standard methods (`upsert`, `similarity_search`, `delete`).
- **Storage:** Embeddings generated via the `embeddings/` submodule are stored in the active vector backend. Retrievals return standardized document chunks with distance scores.

## 5. Guardrails Pipeline
The `guardrails/` submodule ensures safety and compliance.
- **Pre-LLM Filtering:** Intercepts malicious prompts, PII, and out-of-domain queries before they reach the model.
- **Post-LLM Filtering:** Validates the generated response for toxicity, hallucinations, and formatting constraints. Blocked requests raise an `AIGuardrailException`.

## 6. Citation System
Transparency is maintained via the `citation/` submodule.
- **Tracking:** Each document chunk injected into the prompt carries a unique source ID.
- **Attribution:** The LLM is instructed to cite sources inline (e.g., `[1]`). The system parses these and appends a structured list of references to the response, linking claims back to platform data.

## 7. Evaluation Framework
The `evaluation/` submodule provides continuous assessment of RAG quality.
- **Metrics:** Evaluates on Faithfulness, Answer Relevance, and Context Precision.
- **Process:** Automated tests run against benchmark datasets to score the pipeline, ensuring updates to embeddings or prompts do not degrade quality.

## 8. Prompt Engineering
The `prompts/` submodule centralizes all prompt templates.
- **Template System:** Uses parameterized templates (e.g., Jinja2 or f-strings) for dynamic context injection.
- **Modification:** Modifying a prompt involves updating the corresponding template file, enabling quick iterations without touching application logic.

## 9. Request and Response Schemas
Defined in the `schemas/` submodule.
- **Request:** `AIQueryRequestSchema` includes fields for the query string, conversation history, optional filters, and configuration overrides.
- **Response:** Returns a standard JSON format containing the `answer`, `citations` list, `confidence_score`, and `metadata`.

## 10. Error Handling
The `exceptions/` submodule defines domain-specific errors.
- **Types:** `AIProviderError`, `AIRetrievalError`, `AIGuardrailException`.
- **Propagation:** These bubble up to the `/api/v1/ai/query` route, which maps them to appropriate HTTP status codes (e.g., 400 for guardrail blocks, 503 for provider outages) with sanitized user-facing messages.

## 11. Performance Considerations
- **Caching:** Identical queries are cached at the API layer (Redis) to reduce latency and API costs.
- **Async Inference:** All LLM and vector store calls use `async`/`await` to prevent blocking the event loop under heavy concurrent load.

## 12. Future Extension Points
- **New Models:** Plug-and-play support for emerging local or cloud LLMs.
- **Advanced Retrieval:** Integration of graph-based retrieval (Knowledge Graphs) or query decomposition strategies to handle multi-hop reasoning.
