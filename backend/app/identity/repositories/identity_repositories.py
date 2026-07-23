"""Repositories for managing User, RefreshToken, ApiKey, and Audit persistence."""

import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.identity.models.api_key import ApiKeyModel
from app.identity.models.audit import AuditEntryModel
from app.identity.models.role import RoleModel, RolePermissionModel
from app.identity.models.token import RefreshTokenModel
from app.identity.models.user import UserModel, UserRoleModel


class UserRepository:
    """Async repository for User ORM persistence."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: uuid.UUID) -> UserModel | None:
        stmt = (
            select(UserModel)
            .options(
                selectinload(UserModel.user_roles)
                .selectinload(UserRoleModel.role)
                .selectinload(RoleModel.permissions)
                .selectinload(RolePermissionModel.permission)
            )
            .where(UserModel.id == user_id)
        )
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_email(self, email: str) -> UserModel | None:
        stmt = (
            select(UserModel)
            .options(
                selectinload(UserModel.user_roles)
                .selectinload(UserRoleModel.role)
                .selectinload(RoleModel.permissions)
                .selectinload(RolePermissionModel.permission)
            )
            .where(UserModel.email == email)
        )
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()

    async def add(self, user: UserModel) -> UserModel:
        self._session.add(user)
        await self._session.flush()
        return user

    async def assign_role_by_name(self, user_id: uuid.UUID, role_name: str) -> None:
        stmt = select(RoleModel).where(RoleModel.name == role_name)
        res = await self._session.execute(stmt)
        role = res.scalar_one_or_none()
        if not role:
            role = RoleModel(name=role_name, description=f"{role_name} role")
            self._session.add(role)
            await self._session.flush()

        user_role = UserRoleModel(user_id=user_id, role_id=role.id)
        self._session.add(user_role)
        await self._session.flush()


class RefreshTokenRepository:
    """Async repository for RefreshToken tracking and revocation."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, token: RefreshTokenModel) -> RefreshTokenModel:
        self._session.add(token)
        await self._session.flush()
        return token

    async def get_by_hash(self, token_hash: str) -> RefreshTokenModel | None:
        stmt = select(RefreshTokenModel).where(
            RefreshTokenModel.token_hash == token_hash
        )
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()

    async def revoke(self, token_hash: str) -> bool:
        token = await self.get_by_hash(token_hash)
        if token:
            token.is_revoked = True
            await self._session.flush()
            return True
        return False


class ApiKeyRepository:
    """Async repository for ApiKey management."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, api_key: ApiKeyModel) -> ApiKeyModel:
        self._session.add(api_key)
        await self._session.flush()
        return api_key

    async def get_by_hash(self, key_hash: str) -> ApiKeyModel | None:
        stmt = select(ApiKeyModel).where(ApiKeyModel.key_hash == key_hash)
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()


class AuditRepository:
    """Async repository for AuditEntry queries."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_user(
        self, user_id: uuid.UUID, limit: int = 100
    ) -> Sequence[AuditEntryModel]:
        stmt = (
            select(AuditEntryModel)
            .where(AuditEntryModel.user_id == user_id)
            .order_by(AuditEntryModel.timestamp.desc())
            .limit(limit)
        )
        res = await self._session.execute(stmt)
        return res.scalars().all()
