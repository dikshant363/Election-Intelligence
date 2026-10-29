# Election Intelligence Platform — Free Cloud Deployment Guide
**Target Cost:** ₹0 / $0 per month (100% Free-Tier Architecture)  
**Stack:** Render Free Web Service (Docker Runtime) + Neon Free Serverless PostgreSQL 17  
**Architecture:** Single-tenant SSR Rust Axum Binary with In-Process BM25 Search & Embedded Migrations

---

## 1. Cloud Architecture Overview

The Election Intelligence Platform is compiled into a single self-contained, statically-linked (via Rustls) native binary that runs inside a minimal distroless Debian container. It requires only an authoritative PostgreSQL instance.

```
┌────────────────────────────────────────────────────────┐
│             Free Tier Internet / Users                 │
└──────────────────────────┬─────────────────────────────┘
                           │ HTTPS (Port 443 / SSL)
                           ▼
┌────────────────────────────────────────────────────────┐
│             Render Free Web Service                    │
│  - Runtime: Multi-stage Docker container               │
│  - Resources: 0.5 CPU, 512 MB RAM (Free Plan)          │
│  - Port: Dynamically assigned via PORT (default 10000) │
│  - Auto-sleep: Sleeps after 15 mins of inactivity      │
│  - Auto-wake: Wakes in 30-50s on incoming HTTP query   │
│  - Custom domain & automatic Let's Encrypt SSL: Free   │
└──────────────────────────┬─────────────────────────────┘
                           │ TLS connection (sslmode=require)
                           ▼
┌────────────────────────────────────────────────────────┐
│             Neon Free Serverless PostgreSQL            │
│  - Storage: 0.5 GiB (Lok Sabha 2024 database is < 2 MB)│
│  - Version: PostgreSQL 17                              │
│  - Auto-suspend: Conserves compute when idle           │
│  - Instant resume: Sub-second wakeup on connection     │
│  - Embedded Migrations: Run automatically on connect   │
└────────────────────────────────────────────────────────┘
```

---

## 2. Step 1: Provision Free Serverless PostgreSQL (Neon)

1. Sign up for a free account at [https://neon.tech](https://neon.tech) (No credit card required).
2. Click **Create Project**:
   - **Name:** `election-intelligence`
   - **Postgres version:** `17`
   - **Region:** Choose the region closest to your app (e.g., `AWS US East (Ohio)` or `AWS Frankfurt`).
3. In the Neon Console Dashboard, navigate to **Connection Details**:
   - Select **Pooled connection** checkbox.
   - Copy the provided connection string. It will look like:
     ```
     postgres://alex:AbC123XyZ@ep-cool-resonance-pooler.us-east-2.aws.neon.tech/election_intelligence?sslmode=require
     ```
4. *Note on Migrations:* You do **NOT** need to manually run `psql` scripts. The Rust application automatically verifies and applies all migrations (`0001_initial_schema.sql`, `0002_seed_initial_data.sql`, `0003_authentic_2024_lok_sabha_data.sql`) upon first connection.

---

## 3. Step 2: Deploy to Render Free Web Service

### Option A: One-Click Render Blueprint (Recommended)
1. Fork or push the repository to GitHub: `https://github.com/dikshant363/Election-Intelligence`.
2. Log into [https://render.com](https://render.com) (Free account, no credit card required).
3. Click **New +** -> **Blueprint**.
4. Connect the `Election-Intelligence` GitHub repository.
5. Render will automatically detect [`render.yaml`](../render.yaml):
   - Service name: `election-intelligence-platform`
   - Runtime: `Docker`
   - Plan: `Free`
   - Health Check Path: `/ready`
6. Under Environment Variables, paste your Neon `DATABASE_URL` string into the `DATABASE_URL` prompt.
7. Click **Apply**. Render will trigger the multi-stage Docker build and deploy the container.

### Option B: Manual Web Service Setup
1. In Render Dashboard, click **New +** -> **Web Service**.
2. Connect your GitHub repository.
3. Configure the following fields:
   - **Name:** `election-intelligence`
   - **Region:** Same as your Neon database (e.g., `Oregon (US West)` or `Frankfurt (EU)`)
   - **Branch:** `feature/sprint-25.0-enterprise-control-center` (or `main`)
   - **Runtime:** `Docker`
   - **Instance Type:** `Free`
4. In **Advanced** -> **Health Check Path**, enter:
   ```
   /ready
   ```
5. In **Environment Variables**, add:
   | Key | Value |
   | :--- | :--- |
   | `HOST` | `0.0.0.0` |
   | `PORT` | `10000` |
   | `ENVIRONMENT` | `production` |
   | `RUST_LOG` | `info` |
   | `DATABASE_URL` | `postgres://user:pass@ep-pooler.region.aws.neon.tech/election_intelligence?sslmode=require` |
   | `ADMIN_API_KEY` | *(Generate a random 32-character token)* |
   | `JWT_SECRET` | *(Generate a random 64-character token)* |
6. Click **Create Web Service**.

---

## 4. Step 3: Verification of Public Deployment

Once deployment completes (typically 3–4 minutes for the first Docker image build), Render will assign an HTTPS URL such as:
`https://election-intelligence-platform.onrender.com`

Verify the live deployment from an external terminal:

```bash
# 1. Readiness Check (Verifies application & PostgreSQL connectivity)
curl -s -i https://election-intelligence-platform.onrender.com/ready

# Expected output:
# HTTP/2 200
# content-type: application/json
# {"database":"CONNECTED","status":"READY","timestamp":"..."}

# 2. Health & Component Telemetry
curl -s https://election-intelligence-platform.onrender.com/api/v1/health | jq .

# 3. Authentic Data Endpoint (Candidates with Form 26 Sworn Disclosures)
curl -s https://election-intelligence-platform.onrender.com/api/v1/candidates | jq .

# 4. In-Process BM25 Search
curl -s "https://election-intelligence-platform.onrender.com/api/v1/search?q=Varanasi" | jq .

# 5. Evidence-Grounded AI Query (Offline Verifier Mode)
curl -s -X POST https://election-intelligence-platform.onrender.com/api/v1/ai/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the declared assets of Narendra Modi in Varanasi?", "max_citations": 2}' | jq .
```

---

## 5. Free-Tier Operational Characteristics & Limitations

| Aspect | Free Tier Specification | Behavior & Civic Platform Handling |
| :--- | :--- | :--- |
| **Monthly Cost** | **₹0.00 / $0.00** | Zero recurring charges. No credit card required. |
| **Compute Idle Sleep** | Render spins down instances after 15 mins of no traffic | First incoming request takes 30-50s to wake container; subsequent requests take < 5ms. |
| **Database Auto-Suspend**| Neon suspends compute after 5 mins of inactivity | Instant wake-up upon incoming TCP connection. |
| **Database Storage** | 0.5 GiB storage limit | Current 2024 Lok Sabha dataset is < 2 MB (< 0.4% of limit). |
| **Backups** | Neon retains point-in-time restore for 24 hours | Periodic automated backup via `./scripts/backup_postgres.sh`. |
| **Data Retention** | Persistent across restarts | Data is written to managed Neon PostgreSQL and survives restarts and redeployments. |
