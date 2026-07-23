"""Structured JSON logging with TelemetryContext propagation and secret sanitization."""

from __future__ import annotations

import json
import logging
import re
from datetime import UTC, datetime
from typing import Any

from app.observability.telemetry import TelemetryContext, get_current_telemetry_context

# Sensitive key names to redact
SENSITIVE_KEYS_RE = re.compile(
    r"password|secret|token|api_key|authorization|bearer", re.IGNORECASE
)


def sanitize_dict(data: dict[str, Any]) -> dict[str, Any]:
    """Scrub sensitive keys from log metadata dictionary."""
    clean = {}
    for k, v in data.items():
        if SENSITIVE_KEYS_RE.search(k):
            clean[k] = "[REDACTED_SECRET]"
        elif isinstance(v, dict):
            clean[k] = sanitize_dict(v)
        else:
            clean[k] = v
    return clean


class JSONFormatter(logging.Formatter):
    """JSON log formatter attaching TelemetryContext metadata."""

    def format(self, record: logging.LogRecord) -> str:
        ctx: TelemetryContext = get_current_telemetry_context()
        log_obj = {
            "timestamp": datetime.now(UTC).isoformat(),
            "severity": record.levelname,
            "message": record.getMessage(),
            "service": ctx.service,
            "component": ctx.component,
            "environment": ctx.environment,
            "trace_id": ctx.trace_id,
            "span_id": ctx.span_id,
            "correlation_id": ctx.correlation_id,
            "causation_id": ctx.causation_id,
            "request_id": ctx.request_id,
            "user_id": ctx.user_id,
        }

        if hasattr(record, "extra") and isinstance(record.extra, dict):
            log_obj["extra"] = sanitize_dict(record.extra)

        return json.dumps(log_obj)


def get_structured_logger(name: str = "app") -> logging.Logger:
    """Get structured logger configured with JSONFormatter."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
