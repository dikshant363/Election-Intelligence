# Dependency Update and Security Patch Policy

## 1. Update Categories and SLAs

- **Security Patches (CVSS ≥ 7.0 - High/Critical):** Must be patched and deployed within **24 hours** of discovery.
- **Security Patches (CVSS 4.0 - 6.9 - Medium):** Must be patched and deployed within **7 days**.
- **Security Patches (CVSS < 4.0 - Low):** Must be patched within **30 days**.
- **Minor Version Updates (Features/Bugfixes):** Reviewed and processed on a **monthly** cycle.
- **Major Version Updates (Breaking Changes):** Reviewed and processed on a **quarterly** cycle, requiring extensive compatibility testing.

## 2. Python Dependency Update Process

- **Monitor:** Continuous monitoring via `pip-audit`, GitHub Dependabot, and GitHub Security Advisories.
- **Test:** Upgrades must run against the full `pytest` suite. No updates are permitted if tests fail.
- **Review:** Major version updates require an architectural impact assessment (e.g., migrating from SQLAlchemy 1.x to 2.x).
- **Approve:** The Principal Architect must explicitly approve all major version bumps.

## 3. Flutter/Dart Dependency Update Process

- Run `flutter pub outdated` monthly to identify stale packages.
- Run `flutter pub upgrade` to apply compatible minor/patch updates.
- Verify UI integrity post-update via `flutter test` and manual smoke testing of core flows.

## 4. Direct vs Transitive Dependency Policy

- We strictly manage **direct dependencies**.
- Transitive dependencies are managed via lockfiles (`poetry.lock` or `requirements.txt` with hashes, and `pubspec.lock`).
- If a transitive dependency has a vulnerability, we attempt to upgrade the parent direct dependency. If unavailable, we forcefully override the transitive dependency version only as a temporary measure.

## 5. Pinning Policy

- **Applications (API, Mobile App):** Pin exact versions in lockfiles to ensure highly reproducible builds.
- **Libraries (if applicable):** Use version ranges (e.g., `>=2.0.0, <3.0.0`) in `pyproject.toml` or `pubspec.yaml` to allow consumers flexibility.

## 6. Automated Scanning Tools

The following tools are actively integrated into the CI/CD pipeline:
- **Python:** `pip-audit`, `safety` (run on every PR).
- **Dart/Flutter:** `dart pub outdated --mode=security` (via custom script).
- **GitHub:** Dependabot alerts and automated PR generation.

## 7. Dependency Approval Checklist

Before introducing any **new** dependency, it must pass this checklist:
1. [ ] **License Check:** Must be MIT, Apache 2.0, BSD, or similar permissive license.
2. [ ] **Maintenance Status:** Repository must have commits within the last 6 months.
3. [ ] **Security History:** Review past CVEs for the package.
4. [ ] **Size Impact:** Assess bloat to Docker image size or mobile app binary size.
5. [ ] **Necessity:** Ensure the functionality cannot be easily built in-house with standard libraries.

## 8. Banned Dependencies

- **Telemetry/Analytics SDKs:** Any package that sends data to third parties without explicit, configurable consent is banned.
- **GPL Licensed Packages:** Strictly prohibited in API-serving code or mobile applications to avoid viral licensing issues affecting proprietary code.

## 9. SBOM Maintenance

- A Software Bill of Materials (SBOM) in **SPDX 2.3 format** is generated via `backend/app/production/sbom/`.
- The SBOM must be automatically regenerated during the CI build process whenever `pyproject.toml`, `requirements.txt`, or `pubspec.yaml` changes.

## 10. Emergency Patch Process (Same-Day)

If a Critical CVE (e.g., in FastAPI, AsyncPG, or standard library) is announced:
1. Security team opens an emergency incident ticket.
2. Engineering bypasses standard sprint work to immediately bump the package version on a hotfix branch.
3. Run automated tests locally.
4. Open PR, require 1 approval, and merge.
5. Deploy immediately to staging, run health checks.
6. Deploy to production outside of normal deployment windows.
7. Post-incident review to ensure all environments are patched.
