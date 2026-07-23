# DEVELOPMENT_SETUP.md

## Prerequisites

- Python 3.12+
- Flutter 3.16+
- Docker (optional, for containerized development)
- PostgreSQL 16+ (for local development)
- Redis 7+ (for caching)

## Quick Start

```bash
# Clone repository
git clone <repository-url>
cd CivicLens India/Election-Intelligence

# Run bootstrap script
./scripts/bootstrap

# Run setup script
./scripts/setup

# Verify installation
./scripts/doctor
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

| Variable | Description | Required |
|----------|-------------|----------|
| DATABASE_URL | PostgreSQL connection string | Yes |
| REDIS_URL | Redis connection string | Yes |
| SECRET_KEY | JWT signing key | Yes |

## Python Setup

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Flutter Setup

```bash
# Get dependencies
flutter pub get

# Run code generation
flutter pub run build_runner build
```

## Verification

Run `./scripts/doctor` to verify all tools are installed correctly.