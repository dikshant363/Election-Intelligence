# Election Domain Foundation Architecture Guide

## Overview
The Election Domain layer (`backend/app/domain/`) establishes the core Domain-Driven Design (DDD) model for the Election Intelligence Platform. It is 100% persistence-agnostic, framework-independent, and pure Python.

## Core Domain Concepts & Bounded Contexts

### 1. Common Domain Primitives (`app/domain/common/`)
- **`Identifier`**: Value object encapsulating UUID or string identities.
- **`Timestamp`**: Immutable UTC timestamp container.
- **`ValueObject`**: Abstract base for immutable value equality types.
- **`Entity[ID]`**: Abstract base for domain entities with identity lifecycle.
- **`AggregateRoot[ID]`**: Abstract base for aggregate roots managing domain event records.

### 2. Value Objects (`app/domain/value_objects/`)
- Immutable domain primitives enforcing strict invariant validation rules upon instantiation:
  - `ElectionId`, `CandidateId`, `PartyId`, `ConstituencyId`, `PollingBoothId`
  - `StateCode`, `DistrictCode`, `AssemblyCode`, `ParliamentCode`
  - `GeoCoordinates` (WGS84 latitude [-90, 90], longitude [-180, 180])
  - `ElectionDate` (start_date, end_date validation)
  - `ElectionType` (`GENERAL`, `ASSEMBLY`, `BYE_ELECTION`, `MUNICIPAL`, `LOCAL_BODY`)
  - `VoteCount`, `Percentage` [0.0, 100.0], `Age`, `Email`, `PhoneNumber`

### 3. Aggregate Roots & Bounded Contexts
- **`Election`** (`app/domain/election/`): Manages election lifecycle (`DRAFT` $\rightarrow$ `ACTIVE` $\rightarrow$ `COMPLETED` / `CANCELLED`). Emits `ElectionCreated`.
- **`Candidate`** (`app/domain/candidate/`): Manages candidate nomination, party affiliation, and contact details. Emits `CandidateRegistered`.
- **`PoliticalParty`** (`app/domain/party/`): Manages party registration code and symbol updates. Emits `PartyRegistered`.
- **`Constituency`** (`app/domain/constituency/`): Represents electoral geographical divisions.
- **`PollingBooth`** (`app/domain/polling/`): Manages booth location coordinates and numbering. Emits `PollingBoothCreated`.
- **`ElectionResult`** (`app/domain/results/`): Manages vote tallies and official winner declaration. Emits `ResultDeclared`.

### 4. Domain Specifications (`app/domain/specifications/`)
- Reusable domain business rule predicates:
  - `CandidateEligibility`: Enforces candidate age $\ge$ 25 years.
  - `ElectionOpen`: Checks if election status is `ACTIVE`.
  - `ValidVotePercentage`: Validates percentage boundaries.
  - `UniquePartySymbol` & `ValidConstituency`: Validates structural integrity.

### 5. Domain Repositories & Services (`app/domain/*/repository.py` & `app/domain/services/`)
- Pure abstract domain repository interfaces: `ElectionRepository`, `CandidateRepository`, `PartyRepository`, `ConstituencyRepository`, `PollingBoothRepository`, `ResultRepository`.
- Domain service interfaces: `ElectionService`, `ResultCalculationService`, `CandidateValidationService`, `ConstituencyService`.

## Testing Command Reference

```bash
# Run domain unit test suite
.venv/bin/pytest tests/test_domain_*.py
```
