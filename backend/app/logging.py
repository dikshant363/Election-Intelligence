"""Logging configuration."""

import logging
import sys
from pathlib import Path


def configure_logging() -> None:
    """Configure structured logging."""
    log_level = logging.INFO
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_format))

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        handlers=[console_handler],
        format=log_format,
    )

    # Ensure logs directory exists for file logging
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # File handler (placeholder for production)
    file_handler = logging.FileHandler("logs/app.log")
    file_handler.setFormatter(logging.Formatter(log_format))
    logging.getLogger().addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
