"""Create election persistence tables.

Revision ID: 0002
Revises: 0001
Create Date: 2026-07-23

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "0002"
down_revision: str | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create persistence tables for election domain aggregates."""
    # 1. Elections table
    op.create_table(
        "elections",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("election_type", sa.String(length=50), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False, default=1),
    )
    op.create_index("ix_elections_election_type", "elections", ["election_type"])
    op.create_index("ix_elections_status", "elections", ["status"])
    op.create_index("ix_elections_type_status", "elections", ["election_type", "status"])

    # 2. Political parties table
    op.create_table(
        "political_parties",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False, unique=True),
        sa.Column("code", sa.String(length=50), nullable=False, unique=True),
        sa.Column("symbol", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False, default=1),
    )
    op.create_index("ix_political_parties_code", "political_parties", ["code"])

    # 3. Constituencies table
    op.create_table(
        "constituencies",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False, unique=True),
        sa.Column("state_code", sa.String(length=10), nullable=False),
        sa.Column("constituency_type", sa.String(length=50), nullable=False, server_default="ASSEMBLY"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False, default=1),
    )
    op.create_index("ix_constituencies_name", "constituencies", ["name"])
    op.create_index("ix_constituencies_code", "constituencies", ["code"])
    op.create_index("ix_constituencies_state_code", "constituencies", ["state_code"])

    # 4. Candidates table
    op.create_table(
        "candidates",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("phone", sa.String(length=50), nullable=False),
        sa.Column("constituency_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("constituencies.id", ondelete="CASCADE"), nullable=False),
        sa.Column("party_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("political_parties.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False, default=1),
    )
    op.create_index("ix_candidates_name", "candidates", ["name"])
    op.create_index("ix_candidates_constituency_id", "candidates", ["constituency_id"])
    op.create_index("ix_candidates_party_id", "candidates", ["party_id"])
    op.create_index("ix_candidates_constituency_party", "candidates", ["constituency_id", "party_id"])

    # 5. Polling booths table
    op.create_table(
        "polling_booths",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("constituency_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("constituencies.id", ondelete="CASCADE"), nullable=False),
        sa.Column("booth_name", sa.String(length=255), nullable=False),
        sa.Column("booth_number", sa.String(length=50), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False, default=1),
        sa.UniqueConstraint("constituency_id", "booth_number", name="uq_polling_booths_constituency_booth_number"),
    )
    op.create_index("ix_polling_booths_constituency_id", "polling_booths", ["constituency_id"])
    op.create_index("ix_polling_booths_booth_number", "polling_booths", ["booth_number"])

    # 6. Election results table
    op.create_table(
        "election_results",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("result_key", sa.String(length=255), nullable=False, unique=True),
        sa.Column("election_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("elections.id", ondelete="CASCADE"), nullable=False),
        sa.Column("constituency_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("constituencies.id", ondelete="CASCADE"), nullable=False),
        sa.Column("winning_candidate_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("candidates.id", ondelete="SET NULL"), nullable=True),
        sa.Column("total_votes", sa.Integer(), nullable=False, default=0),
        sa.Column("candidate_votes_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("is_declared", sa.Boolean(), nullable=False, default=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False, default=1),
        sa.UniqueConstraint("election_id", "constituency_id", name="uq_election_results_election_constituency"),
    )
    op.create_index("ix_election_results_result_key", "election_results", ["result_key"])
    op.create_index("ix_election_results_election_id", "election_results", ["election_id"])
    op.create_index("ix_election_results_constituency_id", "election_results", ["constituency_id"])
    op.create_index("ix_election_results_election_constituency", "election_results", ["election_id", "constituency_id"])


def downgrade() -> None:
    """Drop persistence tables for election domain aggregates."""
    op.drop_table("election_results")
    op.drop_table("polling_booths")
    op.drop_table("candidates")
    op.drop_table("constituencies")
    op.drop_table("political_parties")
    op.drop_table("elections")
