## 2026-07-24 - [Secure Enterprise Control Center Endpoints]
**Vulnerability:** The Enterprise Control Center API endpoints (`/api/v1/admin/*`) lacked authentication and authorization, leaving sensitive administrative operations like feature toggles and cache flushing exposed to unauthorized access.
**Learning:** In FastAPI, it's easy to miss securing an entire sub-router when developing features. Always verify that security dependencies are applied at the `APIRouter` level if all endpoints within the router require the same access level.
**Prevention:** Always apply RBAC rules using `Depends(require_role(...))` at the router level when creating administrative modules. Add tests that explicitly assert unauthenticated requests to administrative endpoints receive a 401 or 403 status code.
