# Support Lifecycle & Deprecation Policy

This document outlines the support lifecycle, version support policies, and deprecation processes for the Election Intelligence Platform (v1.0.0).

## 1. Supported Versions

| Version | Release Date | Active Support Until | Security Support Until | Status |
|---|---|---|---|---|
| **v1.0.0** | 2026-07-01 | 2028-07-01 | 2029-07-01 | **Current Active** |
| **v1.0.0-RC** | 2026-05-15 | 2026-08-15 | 2026-11-15 | Maintenance |

## 2. Support Tiers

- **Active Support**: Full bug fixes, feature backports (where applicable), and security patches.
- **Security Support Only**: Critical security patches only. No new features or non-critical bug fixes.
- **End of Life (EOL)**: No support provided. Upgrading to a supported version is strongly recommended.

## 3. Support Window Policy

- **Long-Term Support (LTS) Releases**: 24 months of Active Support, followed by 12 months of Security Support. (e.g., v1.0.0, v2.0.0).
- **Regular Releases**: 12 months of Active Support, followed by 6 months of Security Support.

## 4. API Deprecation Process

When an API endpoint (FastAPI) needs to be retired, we follow a strict process:

1. **Mark as Deprecated**: Update the OpenAPI specification by adding `deprecated=True` to the FastAPI route decorator.
2. **Log Warnings**: Add a deprecation warning log when the endpoint is accessed (`logger.warning("Deprecated endpoint accessed")`). Include a `Deprecation` HTTP header in the response.
3. **Announce**: Document the deprecation in the `CHANGELOG.md` and release notes.
4. **Window**: Maintain the endpoint for a minimum of two minor version releases.
5. **Removal**: Remove the endpoint completely in the next major version release.

## 5. Feature Deprecation Process

For internal code features (Python/Flutter):
1. Use the `warnings.warn(..., DeprecationWarning)` in Python or `@deprecated` annotation in Dart/Flutter.
2. Announce in the release notes.
3. Provide a migration path.
4. Remove the feature in the next major version.

## 6. Migration Support

When major features or APIs are removed, we provide:
- Detailed migration guides in the `/docs/migrations/` directory.
- Database migration scripts (Alembic) if schema changes are involved.
- When applicable, CLI tools to automate codebase updates for API consumers.

## 7. Reporting Bugs

To report a bug for a supported version, open an issue on the GitHub repository using the `Bug Report` template. Please include the platform version, reproduction steps, and relevant logs.

## 8. Requesting Extended Support

Enterprise clients requiring extended support beyond the standard EOL dates should contact the Principal Architect or the commercial support team at `support@civiclens.example.com` to negotiate an extended support contract.

## 9. Security Vulnerability Reporting

Do not report security vulnerabilities in public issues. Please refer to our [SECURITY.md](../SECURITY.md) for detailed instructions on securely reporting vulnerabilities. The Security Engineer will review all reports.

## 10. Communication Channels

Lifecycle announcements (deprecations, EOL warnings) are communicated via:
- GitHub Releases page.
- Developer mailing list.
- Platform dashboard notifications for registered API developers.
