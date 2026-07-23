"""Command and query execution pipeline wrapper."""

from typing import Any

from app.application.commands import (
    CreateConstituency,
    CreateElection,
    CreatePollingBooth,
    DeclareResult,
    RegisterCandidate,
    RegisterParty,
)
from app.application.exceptions import CommandValidationError
from app.application.handlers import CommandHandlers, QueryHandlers
from app.application.validators import CommandValidator
from app.core.result import DomainError, ErrorCode, Result


class CommandPipeline:
    """Pipeline wrapping validation and command execution."""

    def __init__(self, handlers: CommandHandlers) -> None:
        self._handlers = handlers

    async def execute_create_election(
        self, command: CreateElection
    ) -> Result[Any]:
        """Validate and execute CreateElection command."""
        try:
            CommandValidator.validate_create_election(command)
        except CommandValidationError as err:
            return Result.fail(
                DomainError(message=err.message, code=ErrorCode.VALIDATION_ERROR)
            )
        return await self._handlers.handle_create_election(command)

    async def execute_register_party(
        self, command: RegisterParty
    ) -> Result[Any]:
        """Validate and execute RegisterParty command."""
        try:
            CommandValidator.validate_register_party(command)
        except CommandValidationError as err:
            return Result.fail(
                DomainError(message=err.message, code=ErrorCode.VALIDATION_ERROR)
            )
        return await self._handlers.handle_register_party(command)

    async def execute_create_constituency(
        self, command: CreateConstituency
    ) -> Result[Any]:
        """Validate and execute CreateConstituency command."""
        try:
            CommandValidator.validate_create_constituency(command)
        except CommandValidationError as err:
            return Result.fail(
                DomainError(message=err.message, code=ErrorCode.VALIDATION_ERROR)
            )
        return await self._handlers.handle_create_constituency(command)

    async def execute_register_candidate(
        self, command: RegisterCandidate
    ) -> Result[Any]:
        """Validate and execute RegisterCandidate command."""
        try:
            CommandValidator.validate_register_candidate(command)
        except CommandValidationError as err:
            return Result.fail(
                DomainError(message=err.message, code=ErrorCode.VALIDATION_ERROR)
            )
        return await self._handlers.handle_register_candidate(command)

    async def execute_create_polling_booth(
        self, command: CreatePollingBooth
    ) -> Result[Any]:
        """Validate and execute CreatePollingBooth command."""
        try:
            CommandValidator.validate_create_polling_booth(command)
        except CommandValidationError as err:
            return Result.fail(
                DomainError(message=err.message, code=ErrorCode.VALIDATION_ERROR)
            )
        return await self._handlers.handle_create_polling_booth(command)

    async def execute_declare_result(
        self, command: DeclareResult
    ) -> Result[Any]:
        """Validate and execute DeclareResult command."""
        try:
            CommandValidator.validate_declare_result(command)
        except CommandValidationError as err:
            return Result.fail(
                DomainError(message=err.message, code=ErrorCode.VALIDATION_ERROR)
            )
        return await self._handlers.handle_declare_result(command)


class QueryPipeline:
    """Pipeline wrapping query execution."""

    def __init__(self, handlers: QueryHandlers) -> None:
        self._handlers = handlers
