# CONTROL CENTER DEPLOYMENT GUIDE
## Enterprise Control Center — Version 1.0.0

---

## 1. Hosting Architecture

The Enterprise Control Center can be hosted in two configurations:

1. **Embedded Single-Page Application (SPA)**:
   - Flutter Web build bundle (`build/web`) served directly by FastAPI or NGINX at `/admin` or `/control-center`.
2. **Standalone Flutter Desktop / Web Deployment**:
   - Deployed as a dedicated administrative web service on port `3000` or packaged as a desktop binary (macOS / Windows / Linux) for internal ops teams.

---

## 2. Docker & Compose Integration

The Docker image (`election-intelligence:1.0.0`) packages both the FastAPI administrative API endpoints and static Flutter Web assets.

```bash
# Build production image
docker build -t election-intelligence:1.0.0 .

# Launch complete stack
docker compose up -d
```

- API Base: `http://localhost:8000/api/v1`
- Control Center UI: `http://localhost:3000` or `http://localhost:8000/api/v1/docs`
