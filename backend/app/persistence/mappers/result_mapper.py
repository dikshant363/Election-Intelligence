"""Bidirectional mapper for ElectionResult aggregate and ORM model."""

import uuid

from app.domain.results import ElectionResult
from app.domain.value_objects import (
    CandidateId,
    ConstituencyId,
    ElectionId,
    VoteCount,
)
from app.persistence.models.results import ElectionResultModel


class ResultMapper:
    """Mapper translating between ElectionResult aggregate root and ElectionResultModel."""

    @staticmethod
    def to_domain(model: ElectionResultModel) -> ElectionResult:
        """Convert ElectionResultModel ORM instance to ElectionResult domain aggregate."""
        result = ElectionResult(
            election_id=ElectionId(value=model.election_id),
            constituency_id=ConstituencyId(value=model.constituency_id),
        )
        result.total_votes = VoteCount(count=model.total_votes)
        result.winning_candidate_id = (
            CandidateId(value=model.winning_candidate_id)
            if model.winning_candidate_id
            else None
        )
        result.is_declared = model.is_declared

        # Populate candidate votes
        for c_id_str, count in model.candidate_votes_json.items():
            result.candidate_votes[CandidateId(value=c_id_str)] = VoteCount(
                count=count
            )

        return result

    @staticmethod
    def to_orm(entity: ElectionResult) -> ElectionResultModel:
        """Convert ElectionResult domain aggregate to ElectionResultModel ORM instance."""
        e_id = (
            uuid.UUID(str(entity.election_id.value))
            if isinstance(entity.election_id.value, str)
            else entity.election_id.value
        )
        c_id = (
            uuid.UUID(str(entity.constituency_id.value))
            if isinstance(entity.constituency_id.value, str)
            else entity.constituency_id.value
        )
        winner_id = (
            uuid.UUID(str(entity.winning_candidate_id.value))
            if entity.winning_candidate_id
            and isinstance(entity.winning_candidate_id.value, str)
            else entity.winning_candidate_id.value
            if entity.winning_candidate_id
            else None
        )

        candidate_votes_dict = {
            str(cand_id.value): count.count
            for cand_id, count in entity.candidate_votes.items()
        }

        return ElectionResultModel(
            result_key=str(entity.id),
            election_id=e_id,
            constituency_id=c_id,
            winning_candidate_id=winner_id,
            total_votes=entity.total_votes.count,
            candidate_votes_json=candidate_votes_dict,
            is_declared=entity.is_declared,
        )
