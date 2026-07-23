# VERSION 2 ARCHITECTURE RESET & IMPLEMENTATION PLAN
## Election Intelligence Platform — Public Knowledge Infrastructure

---

## Executive Overview

This document outlines the **Version 2 Architecture Reset** for promoting the Election Intelligence Platform from a feature application to an independent **Public Election Knowledge Infrastructure**.

---

## 🏛️ THE 4 PILLARS OF VERSION 2

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                   THE FOUR PILLARS OF VERSION 2 RESET                   │
├──────────────────────────────────────────────────────────────────────────┤
│ 1. Real, Verifiable Public Data Platform                                 │
│    • Ingestion from ECI, Gazette, Census, Parliament, and MyNeta.       │
│    • Zero mock data fallback in production — explicit data unavailability.│
│                                                                          │
│ 2. Apple / Notion Calm Content-First Design System                      │
│    • High legibility typography, generous whitespace, subdued palette.   │
│    • Calm research publication feel instead of heavy admin dashboards.   │
│                                                                          │
│ 3. Evidence-Grounded AI Research Assistant                               │
│    • Live Mistral AI & Gemini AI integration with 1 RPS throttling.      │
│    • Mandatory source citations, confidence scores, and provenance.      │
│                                                                          │
│ 4. Scalable Public Infrastructure                                        │
│    • Open API contracts, PostgreSQL 16 database, and multi-target apps.  │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 PHASE IMPLEMENTATION PLAN

### Phase 0: Constitution & Product Specification (Completed)
- Formulate `VISION_AND_CONSTITUTION.md` and `PROJECT_VERIFICATION_REQUIREMENTS.md`.
- Establish non-partisan governance rules and Apple-inspired design system.

### Phase 1: Real Data Platform & Ingestion Pipeline
- Build automated ETL collectors (`backend/app/etl`) connecting to official public election repositories.
- Enforce strict provenance tagging (`Official Source`, `Verified Public Record`, `AI Summary`).
- Eliminate simulation mode from production runtime.

### Phase 2: Apple-Quality Knowledge Product UI
- Deploy calm, content-first Flutter theme (`AppTheme`) across Web SPA, Android APK, and iOS App.
- Implement floating Perplexity-style search interface and clean Form 26 candidate comparison cards.

### Phase 3: Grounded AI Assistant & SAL Search Engine
- Integrate Mistral AI (`mistral-small-latest`) with 1 RPS rate-limiting throttling.
- Require mandatory citation generation (`CitationGenerator`) for every AI response.

---

## 🌐 Git & Deployment Handoff

- **GitHub Repository**: [https://github.com/dikshant363/Election-Intelligence](https://github.com/dikshant363/Election-Intelligence)
- **Active Branch**: `feature/v1.0.0-stabilization`
- **Master Handoff Contract**: [`PROJECT_VERIFICATION_REQUIREMENTS.md`](PROJECT_VERIFICATION_REQUIREMENTS.md)
- **Constitution Document**: [`VISION_AND_CONSTITUTION.md`](VISION_AND_CONSTITUTION.md)
