# Project Governance

This document establishes the governance, roles, and processes for the Election Intelligence Platform.

## 1. Project Governance Model

The project operates under a technical steering model. Decisions are driven by consensus among code owners, with the Principal Architect acting as the final arbiter for technical deadlocks.

## 2. Roles and Responsibilities

- **Principal Architect**: Owns overall system design, API contracts, and cross-cutting architectural decisions.
- **Senior Developer (Backend/Frontend)**: Leads subsystem implementation, conducts rigorous code reviews, and mentors junior staff.
- **DevOps Engineer**: Owns CI/CD pipelines, Docker infrastructure, and deployment processes.
- **QA Engineer**: Defines test plans, maintains quality gates, and oversees integration testing.
- **Security Lead**: Audits code for vulnerabilities, manages dependency security, and ensures data compliance.

## 3. Decision-Making Process

- **Architectural Decisions**: Require an Architecture Decision Record (ADR) detailing context, options, and consequences. ADRs are reviewed in architecture meetings.
- **Feature Decisions**: Driven by the Product Roadmap. Scope is negotiated during release planning.

## 4. Code Ownership

- **Backend**: The Python backend (`/backend`) is owned by the Backend Engineering Team. At least one backend code owner must approve backend PRs.
- **Frontend (Flutter)**: The Flutter application (`/app` or frontend directory) is owned by the Mobile Engineering Team.
- Detailed routing is defined in a `CODEOWNERS` file.

## 5. Contribution Process

- External contributors must fork the repository, create a feature branch, and submit a Pull Request.
- All contributions must pass the automated CI/CD pipeline and adhere to the guidelines in `QUALITY_GUIDE.md`.
- PRs must follow Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `chore:`, `refactor:`).

## 6. Change Management Process

- Breaking changes (API contract changes, major DB schema alterations) require an approved ADR and an explicit announcement in the engineering channel prior to merging.

## 7. Security Vulnerability Handling Process

- Do not report security vulnerabilities via public GitHub issues.
- Report them to the Security Lead directly.
- A hotfix will be coordinated, developed on a secure, private branch, and released with an advisory.

## 8. Dependency Update Policy

- Dependencies are evaluated monthly.
- Automated tools (e.g., Dependabot) will raise PRs for minor/patch updates.
- Major dependency updates require explicit testing and approval by a code owner to ensure no breaking behavior occurs.

## 9. AI Coding Agent Governance

- AI agents (like GitHub Copilot or internal autonomous agents) may assist in code generation.
- **Rule**: All AI-generated code MUST be reviewed by a human code owner. AI agents are not authorized to directly merge code to `main`.
- AI agents must adhere to the formatting and linting rules defined in `pyproject.toml` and `analysis_options.yaml`.

## 10. Compliance Requirements

- Given the sensitive nature of election data, strict data privacy protocols must be followed.
- PII must be encrypted at rest and in transit.
- Audit logs must record all destructive actions (creates, updates, deletes) in the system.

## 11. Meeting Cadence

- **Architecture Review**: Bi-weekly (reviewing new ADRs).
- **Security Review**: Monthly (reviewing dependency scans and audit logs).
- **Release Planning**: Prior to starting a new release cycle (reviewing the roadmap).

## 12. Documentation Governance

- Documentation is treated as code.
- Code owners are responsible for ensuring `README.md`, OpenAPI specs, and these governance documents stay up to date.
- Changes to core logic must be accompanied by relevant documentation updates in the same PR.
