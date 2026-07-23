# Prompt Orchestration, Guardrails & Token Budgeting Guide

## Overview

Prompt orchestration manages system prompt templates, context window budgeting, and safety guardrails.

---

## Safety Guardrails & Injection Protection

The `AIGuardrails` scanner inspects incoming user prompts against known prompt injection signatures:

```text
Injection Signatures Checked:
- "ignore previous instructions"
- "system prompt"
- "disregard above"
- "jailbreak"
- "override rules"
```

Violations trigger `PromptGuardrailError` before any LLM or retrieval execution.

---

## System Prompt Template (v1.0)

```text
You are the Election Intelligence AI Assistant, an authoritative system for analyzing official election data in India.
Answer the user's question using ONLY the provided verified context documents.
Always maintain strict neutrality, zero political bias, and cite your sources using document references.

Context Documents:
{context_str}
```

---

## Token Budgeting

The `PromptOrchestrator` enforces a maximum context token budget (default `2000` tokens). If assembled context exceeds budget, context documents are dynamically truncated to prevent context overflow.
