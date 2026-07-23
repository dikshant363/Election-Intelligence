# Versioning Policy

This document details the versioning strategies used across the Election Intelligence Platform.

## 1. SemVer Policy

We use Semantic Versioning (SemVer) format: `MAJOR.MINOR.PATCH`.
- **MAJOR**: Breaking changes (e.g., changing API response structures, major UI overhaul).
- **MINOR**: New features added in a backward-compatible manner.
- **PATCH**: Backward-compatible bug fixes.

## 2. API Versioning

- APIs are versioned in the URL path: `/api/v1/...`.
- When introducing a `v2` (Major change), `v1` will remain operational alongside `v2` for a deprecation period to allow clients to migrate safely.

## 3. Database Schema Versioning

- Managed via Alembic migrations.
- Revision IDs must be sequential or properly chained.
- Do not modify existing migration files once they are merged into `main`; always create a new migration for schema updates.

## 4. Docker Image Tagging

- Images are tagged with the specific release version: `1.0.0`.
- The `latest` tag always points to the most recent stable release.
- Pre-release images use tags like `1.0.0-rc.1`.

## 5. Flutter App Versioning

- Versioned in `pubspec.yaml` using the format `MAJOR.MINOR.PATCH+BUILD`.
- Example: `version: 1.0.0+1`.
- The `BUILD` number must increment monotonically with every build submitted to an app store, regardless of the SemVer change.

## 6. Git Tag Conventions

- Use **annotated tags** for all releases: `git tag -a v1.0.0 -m "Production release v1.0.0"`.
- Tags must always include the `v` prefix.
- Do not use lightweight tags for releases.

## 7. Pre-release Versioning

- Used for builds not yet ready for production.
- `alpha`: `v1.1.0-alpha.1` (Feature incomplete, for internal testing).
- `beta`: `v1.1.0-beta.1` (Feature complete, for user acceptance testing).
- `RC`: `v1.0.0-RC` (Release Candidate, ready for production unless bugs are found).

## 8. Breaking Change Policy

- A breaking change requires a MAJOR version bump.
- Examples include: removing a public API endpoint, renaming required JSON payload fields, changing the authentication mechanism.

## 9. Deprecation Policy

- Before removing a feature or API, it must be marked as deprecated for at least one MINOR release.
- Deprecation notices must be included in the API documentation (e.g., OpenAPI `deprecated: true`) and release notes.

## 10. Historical Version Table

| Version | Date | Key Changes |
|---------|------|-------------|
| **v1.0.0** | TBD | Initial Production Release. |
| **v1.0.0-RC** | [Date] | Release Candidate for v1.0.0. Feature freeze. |
| **v1.1** (Roadmap) | Future | AI Intelligence modules. |
| **v1.2** (Roadmap) | Future | Dev Platform enhancements. |
| **v1.3** (Roadmap) | Future | Multi-tenant architecture. |
| **v1.4** (Roadmap) | Future | Government integrations. |
