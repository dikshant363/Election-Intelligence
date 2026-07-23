"""Application command and query validators."""

from app.application.commands import (
    CreateConstituency,
    CreateElection,
    CreatePollingBooth,
    DeclareResult,
    RegisterCandidate,
    RegisterParty,
)
from app.application.exceptions import CommandValidationError

MIN_CANDIDATE_AGE = 25
MIN_LATITUDE = -90.0
MAX_LATITUDE = 90.0
MIN_LONGITUDE = -180.0
MAX_LONGITUDE = 180.0
MAX_PAGE_LIMIT = 1000


class CommandValidator:
    """Validator enforcing structural and value constraints on incoming commands."""

    @staticmethod
    def validate_create_election(command: CreateElection) -> None:
        """Validate CreateElection command fields."""
        if not command.title or not command.title.strip():
            raise CommandValidationError("Election title cannot be empty.")
        if command.end_date < command.start_date:
            raise CommandValidationError(
                "end_date cannot be earlier than start_date."
            )

    @staticmethod
    def validate_register_party(command: RegisterParty) -> None:
        """Validate RegisterParty command fields."""
        if not command.name or not command.name.strip():
            raise CommandValidationError("Party name cannot be empty.")
        if not command.code or not command.code.strip():
            raise CommandValidationError("Party code cannot be empty.")
        if not command.symbol or not command.symbol.strip():
            raise CommandValidationError("Party symbol cannot be empty.")

    @staticmethod
    def validate_create_constituency(command: CreateConstituency) -> None:
        """Validate CreateConstituency command fields."""
        if not command.name or not command.name.strip():
            raise CommandValidationError("Constituency name cannot be empty.")
        if not command.code or not command.code.strip():
            raise CommandValidationError("Constituency code cannot be empty.")
        if not command.state_code or not command.state_code.strip():
            raise CommandValidationError("State code cannot be empty.")

    @staticmethod
    def validate_register_candidate(command: RegisterCandidate) -> None:
        """Validate RegisterCandidate command fields."""
        if not command.name or not command.name.strip():
            raise CommandValidationError("Candidate name cannot be empty.")
        if command.age < MIN_CANDIDATE_AGE:
            raise CommandValidationError(
                f"Candidate age ({command.age}) is below minimum requirement of 25."
            )
        if not command.email or "@" not in command.email:
            raise CommandValidationError("Invalid email address format.")
        if not command.constituency_id or not command.constituency_id.strip():
            raise CommandValidationError("Constituency ID cannot be empty.")

    @staticmethod
    def validate_create_polling_booth(command: CreatePollingBooth) -> None:
        """Validate CreatePollingBooth command fields."""
        if not command.booth_name or not command.booth_name.strip():
            raise CommandValidationError("Polling booth name cannot be empty.")
        if not command.booth_number or not command.booth_number.strip():
            raise CommandValidationError("Polling booth number cannot be empty.")
        if not (MIN_LATITUDE <= command.latitude <= MAX_LATITUDE):
            raise CommandValidationError(
                f"Latitude out of range [-90, 90]: {command.latitude}"
            )
        if not (MIN_LONGITUDE <= command.longitude <= MAX_LONGITUDE):
            raise CommandValidationError(
                f"Longitude out of range [-180, 180]: {command.longitude}"
            )

    @staticmethod
    def validate_declare_result(command: DeclareResult) -> None:
        """Validate DeclareResult command fields."""
        if not command.election_id or not command.election_id.strip():
            raise CommandValidationError("Election ID cannot be empty.")
        if not command.constituency_id or not command.constituency_id.strip():
            raise CommandValidationError("Constituency ID cannot be empty.")
        if not command.candidate_votes:
            raise CommandValidationError(
                "candidate_votes tally dictionary cannot be empty."
            )
        for cand_id, count in command.candidate_votes.items():
            if count < 0:
                raise CommandValidationError(
                    f"Vote count for candidate '{cand_id}' cannot be negative."
                )


class QueryValidator:
    """Validator enforcing parameter constraints on incoming queries."""

    @staticmethod
    def validate_pagination(skip: int, limit: int) -> None:
        """Validate pagination parameters."""
        if skip < 0:
            raise CommandValidationError(f"skip cannot be negative: {skip}")
        if limit <= 0 or limit > MAX_PAGE_LIMIT:
            raise CommandValidationError(
                f"limit must be between 1 and 1000: {limit}"
            )
