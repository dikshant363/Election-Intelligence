## Summary of Changes
<!-- Provide a clear, concise summary of what this pull request modifies and why. -->

## Civic Neutrality & Data Integrity Checklist
- [ ] **Strict Political Neutrality**: Does not favor, endorse, or criticize any party or candidate.
- [ ] **Evidence-First Grounding**: All factual election statistics, vote tallies, and disclosures cite verifiable sources (ECI Gazettes, ADR/MyNeta filings).
- [ ] **Legal Terminology**: Accurately distinguishes between pending legal allegations/trials and formal judicial convictions.
- [ ] **Zero Synthetic Mocks in Production**: Production routes strictly use PostgreSQL persistence; no hardcoded success badges or fake metrics.

## Engineering Quality Gates
- [ ] `cargo fmt --all -- --check` passes.
- [ ] `cargo clippy --all-targets --all-features -- -D warnings` passes with 0 warnings.
- [ ] `cargo test --all-features` passes with live PostgreSQL migrations.
- [ ] Apple Human Interface Guidelines and WCAG 2.2 AA contrast standards preserved.
