# Application Layer Directory Structure

```
backend/
├── app/
│   └── application/
│       ├── __init__.py               # Application layer package entrypoint
│       ├── commands/                 # CQRS Command data structures
│       │   ├── __init__.py
│       │   ├── candidate_commands.py # RegisterCandidate
│       │   ├── constituency_commands.py# CreateConstituency
│       │   ├── election_commands.py  # CreateElection
│       │   ├── party_commands.py     # RegisterParty
│       │   ├── polling_commands.py   # CreatePollingBooth
│       │   └── result_commands.py    # DeclareResult
│       ├── dto/                      # Pure Data Transfer Objects
│       │   ├── __init__.py
│       │   ├── candidate_dto.py      # CandidateDTO
│       │   ├── constituency_dto.py   # ConstituencyDTO
│       │   ├── election_dto.py       # ElectionDTO
│       │   ├── party_dto.py          # PartyDTO
│       │   ├── polling_dto.py        # PollingBoothDTO
│       │   └── results_dto.py        # ElectionResultDTO
│       ├── events/                   # Application event dispatcher
│       │   ├── __init__.py
│       │   └── dispatcher.py         # EventDispatcher
│       ├── exceptions/               # Application exception hierarchy
│       │   ├── __init__.py
│       │   └── exceptions.py         # ApplicationException, CommandValidationError
│       ├── handlers/                 # CQRS Command & Query handlers
│       │   ├── __init__.py
│       │   ├── command_handlers.py   # CommandHandlers
│       │   └── query_handlers.py     # QueryHandlers
│       ├── pipeline/                 # Command pipeline wrapper
│       │   ├── __init__.py
│       │   └── pipeline.py           # CommandPipeline, QueryPipeline
│       ├── queries/                  # CQRS Query data structures
│       │   ├── __init__.py
│       │   └── queries.py            # GetElection, ListElections, GetCandidate, etc.
│       └── validators/               # Command & Query structural validators
│           ├── __init__.py
│           └── validators.py         # CommandValidator, QueryValidator
tests/
└── test_application.py               # Application layer CQRS & pipeline test suite
APPLICATION_GUIDE.md                  # Application layer architecture & CQRS guide
APPLICATION_STRUCTURE.md              # Application layer directory layout
APPLICATION_VALIDATION.md             # Application layer verification report
```

## Architectural Isolation Guarantees
1. **Zero Web Framework Imports**: No FastAPI, Starlette, or HTTP route dependencies.
2. **Zero ORM Leakage**: Handlers return pure DTOs or `Result[DTO]`. ORM models never cross the application boundary.
3. **Transaction Safety**: All command mutations occur inside `UnitOfWork` context managers and dispatch domain events upon successful commit.
