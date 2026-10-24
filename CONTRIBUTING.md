# Contributing to Election Intelligence Platform

Thank you for your interest in contributing to the **Election Intelligence Platform**—an independent, politically neutral, community-driven civic-tech research platform.

---

## 1. Core Principles for Contributors

1. **Strict Political Neutrality**: The platform never favors, endorses, attacks, or recommends any political party or candidate. Contributions must maintain objective, non-partisan language.
2. **Evidence Before Conclusions**: Every factual claim (vote tallies, candidate assets, legal filings) must cite an official or statutory primary source (e.g., ECI Gazettes, ADR/MyNeta Form 26 filings).
3. **Legal Distinction Integrity**: Under Indian electoral law, allegations or pending trials stated in Form 26 affidavits are legal proceedings, not judicial convictions. Contributor copy must never infer or state guilt from pending cases.
4. **No Fabricated Data**: Never insert synthetic data, fake confidence numbers, or mocked success states into production code paths.

---

## 2. Development Setup

### Prerequisites
- **Rust Toolchain**: 1.85+ (`rustup default stable`)
- **PostgreSQL**: 17+ (`brew services start postgresql@17` or Docker)

### Setup Steps
```bash
# 1. Clone repository
git clone https://github.com/dikshant363/Election-Intelligence.git
cd Election-Intelligence

# 2. Initialize Database & Seed Verified Records
psql -d election_intelligence -f migrations/0001_initial_schema.sql
psql -d election_intelligence -f migrations/0002_seed_initial_data.sql

# 3. Run Automated Tests
cargo test

# 4. Start Development Server
cargo run
```

---

## 3. Engineering Quality Gates

Before submitting a Pull Request, ensure all checks pass:

```bash
# Code formatting
cargo fmt --all -- --check

# Clippy linter
cargo clippy --all-targets --all-features -- -D warnings

# Unit and integration test suite
cargo test --all-features
```

---

## 4. Reporting Data Disputes or Inaccuracies
To report incorrect election statistics, outdated affidavits, or conflicting source data, please use our [Evidence Dispute Template](.github/ISSUE_TEMPLATE/evidence_dispute.md).

---

## 5. License
By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
