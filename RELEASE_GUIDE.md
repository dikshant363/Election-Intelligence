# Release Management & Supply Chain Security Guide

## Overview

The `ReleaseManager`, `DeploymentSafetyManager`, and `SBOMGenerator` ensure supply-chain integrity, migration safety, and deployment readiness.

---

## Pre-Release Checklist Verification

```python
from app.production.release import ReleaseManager

checklist = ReleaseManager.get_release_checklist()
# Returns tests_passed, lint_passed, migrations_verified, sbom_generated, ready_for_deployment
```

---

## SPDX 2.3 SBOM Generation

Generate SPDX 2.3 Software Bill of Materials via API or CLI:

```text
GET /api/v1/release
```

Sample SPDX output:

```json
{
  "spdxVersion": "SPDX-2.3",
  "dataLicense": "CC0-1.0",
  "name": "election-intelligence-platform-sbom",
  "packages": [
    {"name": "fastapi", "versionInfo": "0.115.0", "licenseConcluded": "MIT"},
    {"name": "pydantic", "versionInfo": "2.10.0", "licenseConcluded": "MIT"},
    {"name": "sqlalchemy", "versionInfo": "2.0.35", "licenseConcluded": "MIT"}
  ]
}
```
