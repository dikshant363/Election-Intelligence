# Public REST API Foundation Guide

## Overview
The Public REST API Layer (`backend/app/api/`) exposes Application Layer CQRS pipelines (`CommandPipeline` and `QueryHandlers`) via FastAPI.

## Architecture

```
   [HTTP Request Client]
             │
             ▼
   [FastAPI REST Routers]  (/api/v1/elections, /candidates, etc.)
             │
             ▼
   [Application Pipelines]  (CommandPipeline & QueryHandlers)
             │
             ▼
     [Domain Model & UoW]
             │
             ▼
   [SQLAlchemy & PostgreSQL]
```

## Guarantees & Constraints
1. **Zero Repository Import in Routers**: Routers interact exclusively with `CommandPipeline` and `QueryHandlers` injected via `Depends()`.
2. **Pydantic v2 API Schemas**: Request and Response schemas are decoupled from Application DTOs and ORM entities.
3. **RFC 7807 Problem Details**: All error responses conform strictly to RFC 7807 JSON format (`type`, `title`, `status`, `detail`, `instance`, `code`).

## REST Endpoints Summary

| Method | Path | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/elections` | Schedule a new election |
| `GET` | `/api/v1/elections/{id}` | Fetch election details by ID |
| `GET` | `/api/v1/elections` | List elections with pagination |
| `POST` | `/api/v1/parties` | Register a new political party |
| `GET` | `/api/v1/parties/{id}` | Fetch party details by ID |
| `GET` | `/api/v1/parties` | List political parties |
| `POST` | `/api/v1/constituencies` | Create an electoral constituency |
| `GET` | `/api/v1/constituencies/{id}` | Fetch constituency details by ID |
| `POST` | `/api/v1/candidates` | Register a nominated candidate |
| `GET` | `/api/v1/candidates/{id}` | Fetch candidate details by ID |
| `GET` | `/api/v1/candidates` | List candidates with filters |
| `POST` | `/api/v1/polling-booths` | Establish a polling booth station |
| `POST` | `/api/v1/results` | Declare constituency election result |
| `GET` | `/api/v1/results` | Fetch constituency election result |

## Interactive Documentation
- **Swagger UI**: `/api/v1/docs`
- **ReDoc**: `/api/v1/redoc`
- **OpenAPI JSON**: `/api/v1/openapi.json`
