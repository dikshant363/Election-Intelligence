# Authorization Guide

This document describes the Role-Based Access Control (RBAC) authorization model for the Election Intelligence Platform (v1.0.0).

## 1. RBAC Model
The platform uses a Role-Based Access Control model where permissions are assigned to roles, and roles are assigned to users. API endpoints enforce authorization by requiring specific permissions rather than specific roles, promoting flexibility.

## 2. Role Definitions
Standard roles include:
- **SystemAdmin**: Full access to all platform settings and user management.
- **DataAnalyst**: Access to read and analyze election data, create reports, but cannot modify core datasets.
- **DataIngestor**: Access to trigger ETL pipelines and upload raw data.
- **Viewer**: Read-only access to published dashboards and reports.

## 3. Permission Enforcement
Authorization is enforced via `backend/app/identity/services/rbac_service.py`. 
- In request handlers (FastAPI dependencies or similar), the service checks if the current user's role contains the required permission for the requested action on the specific resource.
- Example: `rbac_service.require_permission(user, "dataset:read")`

## 4. Adding New Permissions
1. Define the new permission string in the centralized permissions enum/constants file (e.g., `identity/domain/permissions.py`). Format: `<resource>:<action>`.
2. Map the new permission to the appropriate existing roles in the role definitions.
3. Update the API endpoint to enforce the new permission.
4. Add unit tests for the new permission logic.

## 5. Adding a New Role
1. Define the new role in the roles enum (e.g., `identity/domain/roles.py`).
2. Assign the necessary list of permissions to this role in the RBAC mapping configuration.
3. Update database seeding scripts if necessary.
4. Write tests verifying that users with the new role can access permitted resources and are denied access to restricted resources.

## 6. Permission Inheritance Model
Currently, the RBAC model is flat. Roles do not inherit from other roles. If a new role requires the permissions of a `Viewer` plus some extras, all `Viewer` permissions must be explicitly assigned to the new role.

## 7. Audit Logging of Authorization Decisions
- All authorization failures (HTTP 403) are logged via the `backend/app/production/audit/` module.
- High-sensitivity operations (e.g., deleting a dataset, modifying users) log successful authorization and execution for forensic auditing.

## 8. Testing Authorization
- **Unit Tests**: Test `rbac_service.py` independently to ensure role-to-permission mappings are correct.
- **Integration Tests**: Test API endpoints with test tokens representing different roles to verify that 403 Forbidden is correctly returned when unauthorized, and 200/201 when authorized.

## 9. Common Authorization Mistakes to Avoid
- **Checking roles instead of permissions**: Always check for `dataset:write`, never check if `user.role == 'SystemAdmin'`.
- **Forgetting authorization on new endpoints**: Ensure all non-public endpoints have a permission check.
- **Insecure direct object reference (IDOR)**: RBAC ensures the user can read "a" report, but you must also verify they own or have access to the *specific* report requested.
