"""Performance optimizations: Compression, Cursor Pagination, and Streaming query helpers."""

from __future__ import annotations

import base64
import zlib
from typing import Any


def compress_payload(data: str | bytes) -> bytes:
    """Compress payload using zlib compression."""
    raw_bytes = data if isinstance(data, bytes) else data.encode("utf-8")
    return zlib.compress(raw_bytes, level=6)


def decompress_payload(compressed: bytes) -> str:
    """Decompress zlib compressed payload back to string."""
    return zlib.decompress(compressed).decode("utf-8")


class CursorPaginator:
    """Efficient O(1) cursor-based pagination helper for large election datasets."""

    @staticmethod
    def encode_cursor(last_id: str, last_created_at: str) -> str:
        """Encode opaque base64 pagination cursor."""
        raw = f"{last_id}:{last_created_at}"
        return base64.b64encode(raw.encode("utf-8")).decode("utf-8")

    @staticmethod
    def decode_cursor(cursor: str) -> tuple[str, str]:
        """Decode pagination cursor into (last_id, last_created_at)."""
        raw = base64.b64decode(cursor.encode("utf-8")).decode("utf-8")
        parts = raw.split(":", 1)
        return parts[0], parts[1]


class StreamingResultOptimizer:
    """Chunks large database results into memory-efficient streams."""

    @staticmethod
    def chunk_generator(items: list[Any], chunk_size: int = 100) -> list[list[Any]]:
        """Split a large list into chunked batches to prevent RAM spikes."""
        return [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]
