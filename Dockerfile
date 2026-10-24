# ==============================================================================
# Multi-stage Dockerfile for Election Intelligence Platform
# Production-ready, secure, minimal runtime image (Pure Rust native binary)
# ==============================================================================

# --- Stage 1: Build Environment ---
FROM rust:latest AS builder

WORKDIR /usr/src/election-intelligence

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Cache dependencies layer
COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs && \
    cargo build --release && \
    rm -rf src

# Copy actual source code, templates, and migrations
COPY src/ ./src/
COPY migrations/ ./migrations/

# Touch main.rs to invalidate dummy build and compile native release binary
RUN touch src/main.rs && \
    cargo build --release --bin election-intelligence

# --- Stage 2: Minimal Distroless / Hardened Runtime ---
FROM debian:bookworm-slim AS runtime

# Security: Install CA certificates for TLS and create unprivileged user
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/* && \
    useradd -u 10001 -m -s /bin/bash civic

WORKDIR /app

# Copy binary from builder
COPY --from=builder /usr/src/election-intelligence/target/release/election-intelligence /app/election-intelligence
COPY --from=builder /usr/src/election-intelligence/migrations /app/migrations

# Set file ownership to non-root user
RUN chown -R civic:civic /app

USER civic

# Runtime Environment Defaults
ENV HOST=0.0.0.0 \
    PORT=3000 \
    ENVIRONMENT=production \
    RUST_LOG=info

EXPOSE 3000

# Health check against native /api/v1/health endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/api/v1/health || exit 1

ENTRYPOINT ["/app/election-intelligence"]
