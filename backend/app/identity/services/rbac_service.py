"""Role-Based Access Control (RBAC) service evaluating roles and permissions."""


class RoleHierarchy:
    """Predefined system roles and hierarchical permissions."""

    PLATFORM_ADMIN = "PlatformAdmin"
    ELECTION_COMMISSIONER = "ElectionCommissioner"
    STATE_OFFICER = "StateOfficer"
    DISTRICT_OFFICER = "DistrictOfficer"
    ANALYST = "Analyst"
    AUDITOR = "Auditor"
    PUBLIC_USER = "PublicUser"

    ROLE_PERMISSIONS: dict[str, set[str]] = {
        PLATFORM_ADMIN: {"*"},
        ELECTION_COMMISSIONER: {
            "elections:create",
            "elections:read",
            "candidates:register",
            "parties:register",
            "constituencies:create",
            "polling:create",
            "results:declare",
            "audit:read",
        },
        STATE_OFFICER: {
            "elections:read",
            "constituencies:create",
            "polling:create",
            "candidates:register",
        },
        DISTRICT_OFFICER: {
            "elections:read",
            "polling:create",
        },
        ANALYST: {
            "elections:read",
            "candidates:read",
            "parties:read",
            "results:read",
        },
        AUDITOR: {
            "audit:read",
            "elections:read",
        },
        PUBLIC_USER: {
            "elections:read",
            "candidates:read",
            "parties:read",
            "results:read",
        },
    }


class RbacService:
    """Service evaluating role permissions and hierarchical access rules."""

    @classmethod
    def get_permissions_for_roles(cls, user_roles: list[str]) -> set[str]:
        """Compute consolidated permission set for user roles."""
        permissions: set[str] = set()
        for role in user_roles:
            role_perms = RoleHierarchy.ROLE_PERMISSIONS.get(role, set())
            permissions.update(role_perms)
        return permissions

    @classmethod
    def has_permission(
        cls, user_roles: list[str], required_permission: str
    ) -> bool:
        """Evaluate if user roles satisfy required permission."""
        user_perms = cls.get_permissions_for_roles(user_roles)
        if "*" in user_perms or required_permission in user_perms:
            return True
        return False

    @classmethod
    def has_role(cls, user_roles: list[str], required_role: str) -> bool:
        """Evaluate if user possesses required role or PlatformAdmin superuser role."""
        if RoleHierarchy.PLATFORM_ADMIN in user_roles or required_role in user_roles:
            return True
        return False
