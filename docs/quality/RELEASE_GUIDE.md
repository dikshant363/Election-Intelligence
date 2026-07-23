# Release Management Guide

This document defines the release management processes for the Election Intelligence Platform.

## 1. Release Types

- **MAJOR**: Incompatible API changes, major architectural shifts, or large feature epics.
- **MINOR**: Backward-compatible new features and enhancements.
- **PATCH**: Backward-compatible bug fixes and security patches.

## 2. Release Branch Strategy

- Release branches are branched from `main` when a feature freeze occurs.
- Naming convention: `release/vX.Y.Z` or `feature/vX.Y.Z-production-release` (e.g., `feature/v1.0.0-production-release`).
- Only bug fixes and final polish are allowed on a release branch. Once stabilized, it merges back into `main`.

## 3. Version Numbering

We adhere to Semantic Versioning (SemVer: `MAJOR.MINOR.PATCH`).
Pre-release labels:
- `-alpha`: Internal testing, unstable.
- `-beta`: Public/customer testing, mostly stable.
- `-RC`: Release Candidate (e.g., `v1.0.0-RC`), expected to be the final version unless a blocking bug is found.

## 4. Step-by-Step Release Process

1. **Feature Freeze**: No more feature PRs merged into `main` for the targeted release.
2. **Release Branch Creation**: Cut `feature/v1.0.0-production-release` from `main`.
3. **Final Quality Gate Run**: Ensure CI is completely green (`pytest`, `flutter test`, linting, etc.).
4. **CHANGELOG Update**: Document all changes since the last release in `CHANGELOG.md` under the new version header.
5. **Version Bump**: Update version strings in `pyproject.toml`, `pubspec.yaml`, and any hardcoded constants.
6. **Git Tag Creation**: Create an annotated git tag (e.g., `git tag -a v1.0.0 -m "Release v1.0.0"`).
7. **Docker Image Build and Tag**: CI builds the multi-stage Docker image and tags it with the version (e.g., `civiclens/election-intel:1.0.0`).
8. **GitHub Release Creation**: Publish a GitHub Release attaching the release notes and artifacts.
9. **Production Deployment**: Deploy the tagged Docker image and the compiled Flutter application.
10. **Post-Release Monitoring**: Actively monitor application logs, error trackers, and latency metrics for 24-48 hours.

## 5. Hotfix Release Process

1. Branch off the affected release tag (e.g., `hotfix/fix-login-crash` from `v1.0.0`).
2. Implement and test the fix.
3. Bump the PATCH version (e.g., to `v1.0.1`).
4. Update `CHANGELOG.md`.
5. Tag the release (`v1.0.1`), build, and deploy.
6. Merge the hotfix back into `main` to ensure it isn't lost in future releases.

## 6. Release Artifacts

The following artifacts must be generated and archived for each release:
- Multi-stage Docker Image (backend + frontend assets if applicable).
- Compiled Flutter binaries (APK/AAB for Android, IPA for iOS, Web build).
- OpenAPI Specification JSON/YAML.
- Software Bill of Materials (SBOM).
- `CHANGELOG.md`.

## 7. Migration Strategy

- **Database**: We use Alembic for backend migrations. All migrations must be backward-compatible with the *previous* code version to support rolling zero-downtime deployments.
- **Execution**: Migrations run automatically as an init-container or pre-deploy hook before the new application containers spin up.

## 8. Rollback Procedure

- **PATCH/MINOR**: Re-deploy the previous Docker image version. If database migrations were applied, verify if a downgrade script is necessary (ideally avoid downgrades by making schema changes additive).
- **MAJOR**: Same as above, but coordinate with data engineering if massive schema refactoring occurred.
- **Mobile**: Flutter app rollbacks require expediting a previous build through the app stores.

## 9. Release Communication

- **Engineering**: Notified via Slack/Teams automation when the GitHub Release is published.
- **Product/Stakeholders**: Release notes emailed by the Product Manager detailing new features and resolved issues.
- **Users**: In-app notifications and updated documentation.
