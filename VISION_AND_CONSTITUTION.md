# ELECTION INTELLIGENCE PLATFORM — CONSTITUTION & VISION
## Version 2.0.0 Architecture Reset & Public Knowledge Infrastructure

---

## 🏛️ THE CONSTITUTION

### Article I: Mission Statement
> **"The Election Intelligence Platform is an independent, politically neutral, AI-powered public research infrastructure that helps Indian citizens make informed voting decisions by organizing, verifying, and explaining publicly available election information with complete transparency, evidence, and source attribution—without recommending or endorsing any candidate or political party."**

### Article II: Core Guiding Principles

1. **Citizen First**: Every interface, query, and visualization is designed for ordinary citizens, first-time voters, researchers, and journalists—not political campaigns or government administrators.
2. **Strict Political Neutrality**: The platform shall **never** recommend candidates, endorse parties, generate political propaganda, or rank candidates by opinion.
3. **Data-First Architecture**: The platform is a **data platform first** and an application second. Every displayed fact must originate from documented public sources (ECI, MyNeta/ADR, Official Gazettes, Census, Parliament).
4. **Zero Simulation in Production**: The system shall **never** fabricate or generate mock candidate records. If data is unverified or missing, the platform strictly displays *"Official Data Not Available"*.
5. **Apple-Quality Calm UX**: The user experience is designed as a calm, content-first research product inspired by Apple, Notion, Linear, and Perplexity AI—focusing on large typography, generous whitespace, and reading legibility.

---

## 📐 PRODUCT REQUIREMENTS DOCUMENT (PRD)

### 1. User Personas
- **P1: Indian Citizen / First-Time Voter**: Needs fast, neutral, non-partisan summaries of local candidates' Form 26 affidavits (education, assets, liabilities, criminal cases).
- **P2: Investigative Journalist / Researcher**: Needs traceable primary source links, historical election margins, and side-by-side candidate comparison data.
- **P3: Civil Society NGO / Educator**: Needs downloadable PDF/CSV affidavit summaries and verified constituency statistics.

### 2. Information Architecture
```text
Public Election Data Sources (ECI, Gazette, Census, OpenGov)
                         │
                         ▼
        Automated ETL Data Collector & Parser
                         │
                         ▼
        Data Validation, Deduplication & Cleaning
                         │
                         ▼
      Cryptographic Provenance & Verification Tagging
                         │
                         ▼
           PostgreSQL 16 Relational Engine
                         │
                         ▼
      Hybrid Search Index (tsvector) & Vector RAG
                         │
                         ▼
   Live AI Assistant (Mistral AI / Gemini AI + Citations)
                         │
                         ▼
Apple-Quality Content-First UI (Flutter Web, Android, iOS)
```

---

## 🎨 DESIGN SYSTEM SPECIFICATION (Apple / Notion / Linear)

- **Typography**: Display font (Inter / Outfit / SF Pro) with tight letter-spacing (`-0.6px`) and high legibility contrast.
- **Color Palette**:
  - Light Mode Background: `#F8F9FA` | Surface: `#FFFFFF` | Border: `#E5E7EB`
  - Dark Mode Background: `#121212` | Surface: `#1E1E1E` | Border: `#2D3342`
  - Primary Accent: `#2563EB` (Blue) | Verified Emerald: `#10B981`
- **Component Geometry**: Rounded card radius (`16px`), pill-shaped verification badges (`20px`), subtle 1px border lines, zero heavy box shadows.

---

## 🔒 SECURITY & NEUTRALITY GOVERNANCE

- **Zero Partisan Scoring**: No algorithms may assign candidate scores, ratings, or grades.
- **Source Citation Requirement**: Every AI-generated summary must cite its source document (e.g. *ECI Form 26 Affidavit 2024*).
- **Security Controls**: Argon2id password hashing, PyJWT tokens, sliding-window rate limiting, CSP & HSTS security headers.
