# RAG Guide

## 1. What is RAG?
Retrieval-Augmented Generation (RAG) grounds Large Language Models in verifiable facts by fetching relevant data before generating an answer. In the Election Intelligence Platform, RAG prevents hallucinations and ensures responses are based on the latest election data rather than the model's static training weights.

## 2. Dual Retrieval Strategy
We use a Hybrid Retrieval approach:
- **BM25:** A sparse keyword-based system excellent for exact matches (e.g., "Constituency 142", "Rahul Gandhi").
- **Vector Search:** A dense semantic system that understands context and intent (e.g., "Who won in the northern districts by a narrow margin?").

## 3. Data Indexing for RAG
Election data (candidates, results, constituencies) is converted into textual representations.
- **Process:** Data is fetched from the primary database, serialized into descriptive text, embedded into vectors, and indexed in the vector store alongside BM25 indexing.

## 4. Query Processing Pipeline
1. **Query Parsing:** The raw user query is sanitized.
2. **Retrieval:** Both BM25 and vector stores fetch top candidate documents.
3. **Reranking:** Candidates are scored and fused.
4. **Generation:** The top-N documents are injected into the LLM prompt.
5. **Citations:** The final response is parsed to extract source attributions.

## 5. Chunking Strategy
Election documents are chunked logically rather than by strict token limits.
- **Entity Chunking:** A single chunk might represent a candidate's profile and their specific election result to preserve context.
- **Size:** Kept under 512 tokens to maximize embedding precision.

## 6. Embedding Model Configuration
The `embeddings/` submodule handles vectorization.
- **Model:** Configured via environment variables (defaults to high-dimensional models like OpenAI `text-embedding-3-small` or local alternatives).
- **Normalization:** Embeddings are L2 normalized prior to storage for efficient cosine similarity calculations.

## 7. Reranking and Fusion
We use Reciprocal Rank Fusion (RRF) to combine BM25 and Vector scores.
- **Mechanism:** RRF assigns a score based on the rank of a document in both lists, smoothing out outliers and elevating documents that perform well in both exact and semantic matching.

## 8. Context Window Management
To prevent overwhelming the LLM and increasing costs:
- **Top-K Limit:** Only the highest-scoring `K` chunks are included.
- **Formatting:** Chunks are formatted as `<source id="X">content</source>` to provide clear boundaries for the LLM.

## 9. Citation Attribution
- **Process:** The prompt strictly instructs the LLM to use the `[id]` format when stating a fact.
- **Resolution:** The platform regex-parses the output, mapping `[id]` back to the original database entity, exposing this metadata in the API response.

## 10. Quality Evaluation
Using RAGAS-style metrics:
- **Faithfulness:** Does the answer strictly align with the retrieved context?
- **Answer Relevance:** Does the answer address the actual query?
- **Context Completeness:** Did the retrieval step fetch all necessary information?

## 11. Debugging RAG Responses
If an answer is wrong, investigate:
1. **Retrieval Failure:** Check the raw retrieval logs. Were the right chunks fetched?
2. **Context Overload:** Was the right chunk fetched but ignored by the LLM?
3. **Prompting Issue:** Did the model hallucinate despite good context? Check guardrail logs.

## 12. Tuning the Pipeline
- **Adjusting K:** Increase retrieval count for complex queries; decrease for speed.
- **Score Thresholds:** Set minimum similarity scores to prevent injecting irrelevant context on out-of-domain queries.
