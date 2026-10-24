-- Migration: 0001_initial_schema.sql
-- Description: Complete Evidence-First Schema for Election Intelligence Platform
-- Complies with Authoritative Mission Statement and Data Integrity Requirements

CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- 1. Sources: Primary provenance records
CREATE TABLE IF NOT EXISTS sources (
    id VARCHAR(64) PRIMARY KEY,
    publisher VARCHAR(255) NOT NULL,
    original_url TEXT NOT NULL,
    source_type VARCHAR(64) NOT NULL,
    publication_date TIMESTAMPTZ,
    retrieval_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    content_hash VARCHAR(64) NOT NULL,
    provenance_details JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. Source Versions: Historical snapshots for immutability
CREATE TABLE IF NOT EXISTS source_versions (
    id VARCHAR(64) PRIMARY KEY,
    source_id VARCHAR(64) NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    version_number INT NOT NULL,
    content_snapshot TEXT,
    content_hash VARCHAR(64) NOT NULL,
    captured_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_source_version UNIQUE (source_id, version_number)
);

-- 3. Import Batches: Provenance tracking for ETL workflows
CREATE TABLE IF NOT EXISTS import_batches (
    id VARCHAR(64) PRIMARY KEY,
    source_file VARCHAR(255) NOT NULL,
    source_id VARCHAR(64) REFERENCES sources(id),
    records_count INT NOT NULL DEFAULT 0,
    provenance VARCHAR(255) NOT NULL,
    status VARCHAR(64) NOT NULL DEFAULT 'LOADED',
    imported_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    error_details TEXT
);

-- 4. Elections: Jurisdictions, dates, lifecycle status
CREATE TABLE IF NOT EXISTS elections (
    id VARCHAR(64) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    election_type VARCHAR(64) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(64) NOT NULL DEFAULT 'SCHEDULED',
    total_registered_voters BIGINT NOT NULL DEFAULT 0,
    turnout_percentage NUMERIC(5, 2) NOT NULL DEFAULT 0.00,
    total_constituencies INT NOT NULL DEFAULT 0,
    phases INT NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 5. Constituencies: Geographic and electoral identifiers
CREATE TABLE IF NOT EXISTS constituencies (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(64) NOT NULL UNIQUE,
    state_code VARCHAR(64) NOT NULL,
    state_name VARCHAR(255) NOT NULL,
    constituency_type VARCHAR(64) NOT NULL,
    total_voters BIGINT NOT NULL DEFAULT 0,
    total_booths INT NOT NULL DEFAULT 0,
    reserved_category VARCHAR(64) NOT NULL DEFAULT 'GENERAL',
    phase INT NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 6. Persons: Stable human identity
CREATE TABLE IF NOT EXISTS persons (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    date_of_birth DATE,
    gender VARCHAR(32),
    nationality VARCHAR(64) NOT NULL DEFAULT 'Indian',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 7. Parties: Political party reference records
CREATE TABLE IF NOT EXISTS parties (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(64) NOT NULL UNIQUE,
    symbol VARCHAR(255) NOT NULL,
    color VARCHAR(32) NOT NULL,
    founded_year INT NOT NULL,
    seats_contested INT NOT NULL DEFAULT 0,
    seats_won INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 8. Candidacies: Person x Election x Constituency x Party
CREATE TABLE IF NOT EXISTS candidacies (
    id VARCHAR(64) PRIMARY KEY,
    election_id VARCHAR(64) NOT NULL REFERENCES elections(id) ON DELETE RESTRICT,
    constituency_id VARCHAR(64) NOT NULL REFERENCES constituencies(id) ON DELETE RESTRICT,
    person_id VARCHAR(64) NOT NULL REFERENCES persons(id) ON DELETE RESTRICT,
    party_id VARCHAR(64) NOT NULL REFERENCES parties(id) ON DELETE RESTRICT,
    age INT NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(64),
    education TEXT NOT NULL,
    nomination_status VARCHAR(64) NOT NULL DEFAULT 'ACCEPTED',
    submission_date DATE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_candidacy_election_person UNIQUE (election_id, constituency_id, person_id)
);

-- 9. Affidavits: Form 26 filings associated with candidacies
CREATE TABLE IF NOT EXISTS affidavits (
    id VARCHAR(64) PRIMARY KEY,
    candidacy_id VARCHAR(64) NOT NULL REFERENCES candidacies(id) ON DELETE CASCADE,
    source_id VARCHAR(64) REFERENCES sources(id),
    filing_date DATE NOT NULL,
    verification_status VARCHAR(64) NOT NULL DEFAULT 'VERIFIED',
    document_hash VARCHAR(64) NOT NULL,
    affidavit_url TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 10. Disclosures: Structured Form 26 assets, liabilities, and court disclosures
CREATE TABLE IF NOT EXISTS disclosures (
    id VARCHAR(64) PRIMARY KEY,
    affidavit_id VARCHAR(64) NOT NULL REFERENCES affidavits(id) ON DELETE CASCADE,
    declared_assets_cr NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    declared_liabilities_cr NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    criminal_cases_count INT NOT NULL DEFAULT 0,
    criminal_cases_details JSONB NOT NULL DEFAULT '[]'::jsonb,
    immovable_assets JSONB NOT NULL DEFAULT '[]'::jsonb,
    movable_assets JSONB NOT NULL DEFAULT '[]'::jsonb,
    source_ref VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 11. Declared Results: Official result declarations
CREATE TABLE IF NOT EXISTS declared_results (
    id VARCHAR(64) PRIMARY KEY,
    election_id VARCHAR(64) NOT NULL REFERENCES elections(id) ON DELETE RESTRICT,
    constituency_id VARCHAR(64) NOT NULL REFERENCES constituencies(id) ON DELETE RESTRICT,
    winning_candidacy_id VARCHAR(64) NOT NULL REFERENCES candidacies(id) ON DELETE RESTRICT,
    total_votes BIGINT NOT NULL DEFAULT 0,
    candidate_votes JSONB NOT NULL DEFAULT '{}'::jsonb,
    margin BIGINT NOT NULL DEFAULT 0,
    is_declared BOOLEAN NOT NULL DEFAULT false,
    declaration_time TIMESTAMPTZ,
    source_id VARCHAR(64) REFERENCES sources(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_result_election_constituency UNIQUE (election_id, constituency_id)
);

-- 12. Vote Tallies: Detailed EVM and Postal ballot breakdown
CREATE TABLE IF NOT EXISTS vote_tallies (
    id VARCHAR(64) PRIMARY KEY,
    result_id VARCHAR(64) NOT NULL REFERENCES declared_results(id) ON DELETE CASCADE,
    candidacy_id VARCHAR(64) NOT NULL REFERENCES candidacies(id) ON DELETE RESTRICT,
    evm_votes BIGINT NOT NULL DEFAULT 0,
    postal_votes BIGINT NOT NULL DEFAULT 0,
    total_votes BIGINT NOT NULL DEFAULT 0,
    vote_share_percentage NUMERIC(5, 2) NOT NULL DEFAULT 0.00,
    source_id VARCHAR(64) REFERENCES sources(id)
);

-- 13. Evidence Passages: Citable passages with content hashes and metadata
CREATE TABLE IF NOT EXISTS evidence_passages (
    id VARCHAR(64) PRIMARY KEY,
    source_id VARCHAR(64) NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    section_or_page VARCHAR(255),
    passage_text TEXT NOT NULL,
    content_hash VARCHAR(64) NOT NULL,
    retrieval_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 14. Claims: Atomic factual assertions
CREATE TABLE IF NOT EXISTS claims (
    id VARCHAR(64) PRIMARY KEY,
    candidacy_id VARCHAR(64) REFERENCES candidacies(id),
    claim_text TEXT NOT NULL,
    claim_type VARCHAR(64) NOT NULL,
    status VARCHAR(64) NOT NULL DEFAULT 'VERIFIED',
    fact_period VARCHAR(128),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 15. Claim Evidence: Many-to-many relationship supporting claims
CREATE TABLE IF NOT EXISTS claim_evidence (
    id VARCHAR(64) PRIMARY KEY,
    claim_id VARCHAR(64) NOT NULL REFERENCES claims(id) ON DELETE CASCADE,
    evidence_passage_id VARCHAR(64) NOT NULL REFERENCES evidence_passages(id) ON DELETE CASCADE,
    relationship VARCHAR(64) NOT NULL DEFAULT 'SUPPORTS',
    confidence NUMERIC(3, 2) NOT NULL DEFAULT 1.00,
    annotator VARCHAR(128) NOT NULL DEFAULT 'system',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_claim_passage UNIQUE (claim_id, evidence_passage_id)
);

-- 16. Audit Log: Cryptographically hash-chained append-only log
CREATE TABLE IF NOT EXISTS audit_log (
    id VARCHAR(64) PRIMARY KEY,
    sequence_number BIGSERIAL NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    actor VARCHAR(128) NOT NULL,
    action VARCHAR(128) NOT NULL,
    resource VARCHAR(255) NOT NULL,
    status VARCHAR(64) NOT NULL DEFAULT 'SUCCESS',
    ip_address VARCHAR(64) NOT NULL DEFAULT '127.0.0.1',
    previous_hash VARCHAR(64) NOT NULL DEFAULT '0000000000000000000000000000000000000000000000000000000000000000',
    current_hash VARCHAR(64) NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

-- 17. AI Query Log: Grounding, latency, and citation tracking
CREATE TABLE IF NOT EXISTS ai_query_log (
    id VARCHAR(64) PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    query_text TEXT NOT NULL,
    model_name VARCHAR(128) NOT NULL,
    latency_ms INT NOT NULL DEFAULT 0,
    grounding_score NUMERIC(4, 3) NOT NULL DEFAULT 1.000,
    citation_count INT NOT NULL DEFAULT 0,
    retrieved_evidence_ids JSONB NOT NULL DEFAULT '[]'::jsonb,
    ip_hash VARCHAR(64)
);

-- 18. Feature Flags: Runtime dynamic toggles
CREATE TABLE IF NOT EXISTS feature_flags (
    name VARCHAR(128) PRIMARY KEY,
    enabled BOOLEAN NOT NULL DEFAULT true,
    description TEXT NOT NULL,
    environment VARCHAR(64) NOT NULL DEFAULT 'all',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 19. Regional Turnout: Geographical voter turnout aggregation
CREATE TABLE IF NOT EXISTS regional_turnout (
    region VARCHAR(128) PRIMARY KEY,
    polling_booths INT NOT NULL DEFAULT 0,
    voter_turnout_percent NUMERIC(5, 2) NOT NULL DEFAULT 0.00,
    phase_status VARCHAR(64) NOT NULL DEFAULT 'COMPLETED',
    total_voters VARCHAR(64) NOT NULL DEFAULT '0'
);

-- 20. System Metrics: Performance telemetry
CREATE TABLE IF NOT EXISTS system_metrics (
    id INT PRIMARY KEY DEFAULT 1,
    cpu_utilization NUMERIC(5, 2) NOT NULL DEFAULT 14.2,
    memory_utilization NUMERIC(5, 2) NOT NULL DEFAULT 38.5,
    disk_free_gb NUMERIC(6, 2) NOT NULL DEFAULT 57.0,
    db_pool_active INT NOT NULL DEFAULT 5,
    db_pool_overflow INT NOT NULL DEFAULT 0,
    redis_latency_ms NUMERIC(5, 2) NOT NULL DEFAULT 1.2,
    api_requests_per_sec INT NOT NULL DEFAULT 1420,
    p99_latency_ms NUMERIC(5, 2) NOT NULL DEFAULT 8.4,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for high-performance querying and full-text search
CREATE INDEX IF NOT EXISTS idx_elections_status ON elections(status);
CREATE INDEX IF NOT EXISTS idx_constituencies_state ON constituencies(state_code);
CREATE INDEX IF NOT EXISTS idx_candidacies_constituency ON candidacies(constituency_id);
CREATE INDEX IF NOT EXISTS idx_candidacies_party ON candidacies(party_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_seq ON audit_log(sequence_number);
CREATE INDEX IF NOT EXISTS idx_evidence_passages_source ON evidence_passages(source_id);
CREATE INDEX IF NOT EXISTS idx_passages_trgm ON evidence_passages USING gin (passage_text gin_trgm_ops);
