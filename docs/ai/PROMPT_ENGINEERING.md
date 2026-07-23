# Prompt Engineering Guide

This document outlines the architecture, testing, and lifecycle management for prompts used within the Election Intelligence Platform. All prompts strictly reside within `backend/app/ai/prompts/`.

## 1. Prompt Architecture

Prompts are treated as code. They are versioned, modular, and defined using Jinja2 templates (`.j2`).
- **Directory Structure**:
  - `backend/app/ai/prompts/system/`: Base behaviors and guardrails.
  - `backend/app/ai/prompts/query/`: Task-specific templates.
  - `backend/app/ai/prompts/evaluation/`: LLM-as-a-judge evaluation prompts.

The `PromptRegistry` class dynamically loads and caches these templates on service startup.

## 2. System Prompt Design

The system prompt grounds the AI exclusively in the election domain. It enforces a professional, strictly analytical persona.

**Core Directives (`system_base.j2`)**:
1. You are an expert election analyst for the Indian Election Intelligence Platform.
2. You rely *only* on provided context. You do not hallucinate external facts.
3. You maintain absolute political neutrality.

## 3. Query Prompt Templates

User questions are not passed raw to the LLM. They are parsed and injected into structured query templates.

```jinja2
{# query/electoral_analysis.j2 #}
Analyze the following user query regarding electoral data:
<UserQuery>
{{ user_query }}
</UserQuery>

Ensure your response addresses the query directly without conversational filler.
```

## 4. RAG Context Injection

Retrieved documents from the search engine (`backend/app/search/`) are injected using clear XML-style tags. This prevents prompt injection and helps the LLM distinguish between instructions and context.

```jinja2
<Context>
{% for doc in documents %}
<Document id="{{ doc.id }}" source="{{ doc.metadata.source_type }}">
{{ doc.content }}
</Document>
{% endfor %}
</Context>
```

## 5. Citation Instruction Prompting

We require granular traceability. The LLM must cite its sources using the document IDs provided in the context.

**Citation Instruction snippet**:
> "When stating a fact, you MUST append a citation inline using the format `[DocID: <id>]`. If the answer cannot be found in the provided `<Context>`, you must state 'Insufficient data available' and refuse to answer."

## 6. Guardrail Prompting

Prior to the main generation step, a fast, lightweight check is executed against `backend/app/ai/guardrails/`.
The guardrail prompt evaluates the `user_query` for:
- Hate speech or incendiary political rhetoric.
- Attempts to extract system prompts (jailbreaks).
- Off-topic inquiries (e.g., "Write a recipe for cake").

If the guardrail returns `FLAGGED`, the API aborts with a `400 Bad Request`.

## 7. Output Format Instructions

For structured data extraction (e.g., parsing candidate affidavits), we enforce JSON output using both Pydantic models (in Python) and explicit JSON schemas in the prompt.

**Formatting Instruction**:
> "Return the data as a valid JSON object matching this schema: {{ json_schema }}. Do not output markdown code blocks. Output raw JSON only."

## 8. Prompt Versioning

Every prompt file contains a header defining its version and valid models:
```jinja2
{# 
version: 1.2.0
models_tested: gpt-4o, gemini-1.5-pro
description: Analyzes historical constituency voting patterns
#}
```
Breaking changes to prompts require a minor version bump in the platform.

## 9. Prompt Testing

Prompts are evaluated in `backend/app/ai/evaluation/`.
- **Unit Tests**: Ensure template variables render correctly.
- **Evaluation Pipeline**: We use an LLM-as-a-judge system to score prompt outputs on a scale of 1-5 for:
  - **Faithfulness**: Are claims supported by the context?
  - **Relevance**: Did it answer the specific user query?
  - **Format adherence**: Did it follow the requested output structure?

## 10. Common Prompt Failures and Fixes

| Failure Mode | Root Cause | Fix Applied in Template |
|--------------|------------|-------------------------|
| **Hallucination** | Weak context boundaries. | Enforce `<Context>` XML boundaries; add strict "refuse to answer" clauses. |
| **Missing Citations** | LLM forgets citation format midway. | Place citation instructions at the *very end* of the prompt (Recency bias). |
| **Off-topic responses** | System prompt ignored. | Increase `temperature=0.0` and utilize the pre-flight guardrail check. |

## 11. Indian Election Domain Context

The system prompt is pre-loaded with critical domain terminology to reduce zero-shot error rates:
- **Institutions**: ECI (Election Commission of India).
- **Legislatures**: Lok Sabha (Lower House), Rajya Sabha (Upper House), Vidhan Sabha (State Assembly).
- **Seat Mapping**: Understands that Parliamentary Constituencies (PCs) contain multiple Assembly Constituencies (ACs).
- **Alliances**: NDA, INDIA bloc, UPA. (Prompts are instructed to map party acronyms to alliances dynamically based on context year).
