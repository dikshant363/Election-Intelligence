# Persistence Layer Directory Structure

```
backend/
├── alembic/
│   └── versions/
│       ├── 0001_initial_empty_migration.py
│       └── 0002_create_election_persistence_tables.py   # Alembic DDL migration
├── app/
│   └── persistence/
│       ├── __init__.py               # Persistence package entrypoint
│       ├── mappers/                  # Bidirectional domain <-> ORM mappers
│       │   ├── __init__.py
│       │   ├── candidate_mapper.py   # Candidate <-> CandidateModel mapper
│       │   ├── constituency_mapper.py# Constituency <-> ConstituencyModel mapper
│       │   ├── election_mapper.py   # Election <-> ElectionModel mapper
│       │   ├── party_mapper.py      # PoliticalParty <-> PoliticalPartyModel mapper
│       │   ├── polling_mapper.py    # PollingBooth <-> PollingBoothModel mapper
│       │   └── result_mapper.py     # ElectionResult <-> ElectionResultModel mapper
│       ├── models/                   # SQLAlchemy 2.x ORM models
│       │   ├── __init__.py
│       │   ├── candidate.py          # CandidateModel
│       │   ├── constituency.py       # ConstituencyModel
│       │   ├── election.py           # ElectionModel
│       │   ├── party.py              # PoliticalPartyModel
│       │   ├── polling.py            # PollingBoothModel
│       │   └── results.py            # ElectionResultModel
│       ├── repositories/             # Async SQLAlchemy repository implementations
│       │   ├── __init__.py
│       │   ├── candidate_repository.py  # SqlAlchemyCandidateRepository
│       │   ├── constituency_repository.py# SqlAlchemyConstituencyRepository
│       │   ├── election_repository.py  # SqlAlchemyElectionRepository
│       │   ├── party_repository.py     # SqlAlchemyPartyRepository
│       │   ├── polling_repository.py   # SqlAlchemyPollingRepository
│       │   └── result_repository.py    # SqlAlchemyResultRepository
│       └── uow/                      # Unit of Work & Transaction management
│           ├── __init__.py
│           └── unit_of_work.py       # UnitOfWork & SqlAlchemyUnitOfWork
tests/
└── test_persistence.py               # Persistence mapping, repository CRUD & UoW tests
PERSISTENCE_GUIDE.md                  # Persistence architecture guide
PERSISTENCE_STRUCTURE.md              # Persistence directory layout documentation
PERSISTENCE_VALIDATION.md             # Persistence verification report
```

## Architectural Isolation Constraints
1. **No FastAPI Dependencies**: Zero web framework or HTTP route imports inside `app/persistence/`.
2. **Strict Repository Contracts**: Repositories accept and return pure Domain Aggregates, concealing SQLAlchemy session interactions from calling code.
3. **Transactional Isolation**: All multi-repository state updates execute within `SqlAlchemyUnitOfWork` transaction boundaries.
