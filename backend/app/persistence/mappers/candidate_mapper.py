"""Bidirectional mapper for Candidate aggregate and ORM model."""

import uuid

from app.domain.candidate import Candidate
from app.domain.value_objects import (
    Age,
    CandidateId,
    ConstituencyId,
    Email,
    PartyId,
    PhoneNumber,
)
from app.persistence.models.candidate import CandidateModel


class CandidateMapper:
    """Mapper translating between Candidate aggregate root and CandidateModel."""

    @staticmethod
    def to_domain(model: CandidateModel) -> Candidate:
        """Convert CandidateModel ORM instance to Candidate domain aggregate."""
        party_id = PartyId(value=model.party_id) if model.party_id else None
        return Candidate(
            id=CandidateId(value=model.id),
            name=model.name,
            age=Age(years=model.age),
            email=Email(address=model.email),
            phone=PhoneNumber(number=model.phone),
            constituency_id=ConstituencyId(value=model.constituency_id),
            party_id=party_id,
        )

    @staticmethod
    def to_orm(entity: Candidate) -> CandidateModel:
        """Convert Candidate domain aggregate to CandidateModel ORM instance."""
        raw_id = (
            uuid.UUID(str(entity.id.value))
            if isinstance(entity.id.value, str)
            else entity.id.value
        )
        con_id = (
            uuid.UUID(str(entity.constituency_id.value))
            if isinstance(entity.constituency_id.value, str)
            else entity.constituency_id.value
        )
        party_id = (
            uuid.UUID(str(entity.party_id.value))
            if entity.party_id and isinstance(entity.party_id.value, str)
            else entity.party_id.value
            if entity.party_id
            else None
        )
        return CandidateModel(
            id=raw_id,
            name=entity.name,
            age=entity.age.years,
            email=entity.email.address,
            phone=entity.phone.number,
            constituency_id=con_id,
            party_id=party_id,
        )
