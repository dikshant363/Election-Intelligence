# Election Domain Directory Structure

```
backend/
├── app/
│   └── domain/
│       ├── __init__.py               # Domain package entrypoint
│       ├── candidate/                # Candidate bounded context
│       │   ├── __init__.py
│       │   ├── candidate.py          # Candidate aggregate root & CandidateRegistered event
│       │   └── repository.py         # CandidateRepository contract
│       ├── common/                   # DDD common base building blocks
│       │   ├── __init__.py
│       │   └── base.py               # Entity, AggregateRoot, ValueObject, Identifier, Timestamp
│       ├── constituency/             # Constituency bounded context
│       │   ├── __init__.py
│       │   ├── constituency.py       # Constituency aggregate root
│       │   └── repository.py         # ConstituencyRepository contract
│       ├── election/                 # Election bounded context
│       │   ├── __init__.py
│       │   ├── election.py           # Election aggregate root, ElectionStatus & ElectionCreated
│       │   └── repository.py         # ElectionRepository contract
│       ├── party/                    # Political Party bounded context
│       │   ├── __init__.py
│       │   ├── party.py              # PoliticalParty aggregate root & PartyRegistered event
│       │   └── repository.py         # PartyRepository contract
│       ├── polling/                  # Polling Booth bounded context
│       │   ├── __init__.py
│       │   ├── polling.py            # PollingBooth aggregate root & PollingBoothCreated event
│       │   └── repository.py         # PollingBoothRepository contract
│       ├── results/                  # Election Results bounded context
│       │   ├── __init__.py
│       │   ├── repository.py         # ResultRepository contract
│       │   └── results.py            # ElectionResult aggregate root & ResultDeclared event
│       ├── services/                 # Pure domain service contracts
│       │   ├── __init__.py
│       │   └── services.py           # ElectionService, ResultCalculationService, etc.
│       ├── specifications/           # Domain specifications
│       │   ├── __init__.py
│       │   └── specifications.py     # CandidateEligibility, ElectionOpen, etc.
│       └── value_objects/            # Domain value objects
│           ├── __init__.py
│           └── value_objects.py      # ElectionId, VoteCount, GeoCoordinates, Age, Email, etc.
tests/
├── test_domain_aggregates.py         # Domain aggregate lifecycle unit tests
├── test_domain_events.py             # Domain event payload unit tests
├── test_domain_specifications.py     # Domain specification predicate unit tests
└── test_domain_value_objects.py      # Domain value object validation unit tests
DOMAIN_GUIDE.md                       # Domain architecture & bounded context guide
DOMAIN_STRUCTURE.md                   # Domain layout documentation
DOMAIN_VALIDATION.md                  # Domain layer verification report
```

## Architectural Decoupling Principles
1. **Zero Framework Dependencies**: No FastAPI, Starlette, Pydantic, or web framework imports.
2. **Zero Infrastructure & ORM Dependencies**: No SQLAlchemy, asyncpg, or SQL database imports.
3. **Pure Domain Invariants**: All business rules, validations, and domain events are encapsulated strictly inside aggregate roots and value objects.
