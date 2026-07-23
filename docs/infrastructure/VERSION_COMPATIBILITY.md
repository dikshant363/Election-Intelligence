# Version Compatibility Matrix

## 1. Core Runtime Compatibility Table

| Component | Minimum | Recommended | Maximum Tested | Notes |
|-----------|---------|-------------|----------------|-------|
| Python | 3.11 | 3.12 | 3.13 | Platform utilizes 3.12 typing features heavily. |
| Flutter | 3.16 | 3.19 | 3.24 | Material 3 requires 3.16+. |
| Dart | 3.2 | 3.3 | 3.4 | Pattern matching relies on 3.0+. |
| PostgreSQL | 14 | 15 | 16 | JSONB features optimized for 15+. |
| Redis | 6.2 | 7.0 | 7.2 | Rate limiting scripts optimized for Redis 7. |
| Docker | 24.0 | 25.0 | 26.0 | BuildKit required for multi-stage builds. |

## 2. Python Dependency Compatibility

| Package | Tested Range | Notes |
|---------|--------------|-------|
| FastAPI | `>=0.109.0, <0.111.0` | Pydantic v2 support required. |
| Pydantic | `>=2.6.0, <3.0.0` | Core validation layer. |
| SQLAlchemy | `>=2.0.25, <2.1.0` | v2.0 style queries enforced. |
| asyncpg | `>=0.29.0, <0.30.0` | High-performance async driver. |
| Alembic | `>=1.13.0, <1.14.0` | Migration framework. |
| PyJWT | `>=2.8.0, <3.0.0` | Token management. |
| argon2-cffi | `>=23.1.0, <24.0.0` | Password hashing algorithm. |

## 3. Flutter Dependency Compatibility

| Package | Tested Range | Notes |
|---------|--------------|-------|
| go_router | `^13.2.0` | Declarative routing. |
| hooks_riverpod | `^2.4.9` | State management. |
| flutter_hooks | `^0.20.5` | Widget lifecycle management. |
| freezed | `^2.4.7` | Code generation for models. |
| equatable | `^2.0.5` | Value equality. |

## 4. Database Driver Compatibility

- **Application:** Uses `asyncpg` exclusively for high-concurrency asynchronous operations.
- **Migrations:** Alembic uses `asyncpg` via the `postgresql+asyncpg://` dialect.
- **Constraints:** Ensure `asyncpg` version matches PostgreSQL 15 connection protocols.

## 5. OS Compatibility

- **Development:** macOS 13+ (Apple Silicon recommended), Ubuntu 22.04 LTS.
- **Production Server:** Ubuntu 24.04 LTS (Noble Numbat).
- **Container Environment:** Alpine Linux 3.19 or Debian 12 (Bookworm-slim) for Docker images.

## 6. CI/CD Environment

- **Runner:** GitHub Actions `ubuntu-latest`.
- **Python Matrix:** Tests run on Python 3.12 primarily.
- **Flutter Matrix:** Tests run on Flutter `stable` channel.
- **Database:** Services leverage PostgreSQL 15 and Redis 7 containers during testing.

## 7. API Versioning Compatibility

- **Current API Version:** `v1` (`/api/v1/...`).
- **Client Requirements:** All clients (mobile, web) must send the `Accept-Version: v1` header (optional but recommended) and handle standard JWT Bearer authentication. Clients must gracefully handle new JSON keys in responses.

## 8. Known Incompatibilities

- **FastAPI < 0.100.0:** Incompatible due to lack of native Pydantic v2 support.
- **SQLAlchemy 1.4:** Incompatible; platform relies entirely on SQLAlchemy 2.0 native syntax.
- **Redis 5.x:** Incompatible with Lua scripts used for sliding-window rate limiting.

## 9. Upgrade Path Table

| From | To | Breaking Changes | Mitigation |
|------|----|------------------|------------|
| Python 3.11 | Python 3.12 | Minor async loop changes. | Update test runner configs. |
| Flutter 3.16| Flutter 3.19 | Deprecated typography. | Run `dart fix --apply`. |
| Postgres 14 | Postgres 15 | Public schema permissions changed. | Update initialization scripts. |

## 10. How to Test Compatibility

Verify local environment using the following commands:
```bash
python3 --version  # Expect: 3.12.x
flutter --version  # Expect: 3.19.x
psql --version     # Expect: 15.x
redis-server -v    # Expect: 7.x
pytest             # Ensure all 287 backend tests pass
flutter test       # Ensure all 6 Flutter tests pass
```
