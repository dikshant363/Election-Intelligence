"""Source connector abstractions and concrete implementations."""

from __future__ import annotations

import hashlib
import io
import urllib.request
import zipfile
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from pathlib import Path

import aiofiles

from app.etl.exceptions import ConnectorError


class SourceConnector(ABC):
    """Abstract interface for all data source connectors."""

    @abstractmethod
    async def fetch(self) -> bytes:
        """Fetch raw bytes from the source."""

    @abstractmethod
    def checksum(self, data: bytes) -> str:
        """Compute SHA-256 checksum for provenance tracking."""


class BaseConnector(SourceConnector):
    """Base connector providing SHA-256 checksum utility."""

    def checksum(self, data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()


class FileConnector(BaseConnector):
    """Connector reading data from a local filesystem path."""

    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)

    async def fetch(self) -> bytes:
        if not self.file_path.exists():
            raise ConnectorError(f"File not found: {self.file_path}")
        async with aiofiles.open(self.file_path, "rb") as f:
            return await f.read()


class HttpConnector(BaseConnector):
    """Connector fetching data from an HTTP/HTTPS URL (synchronous fallback for stdlib)."""

    def __init__(self, url: str, headers: dict[str, str] | None = None) -> None:
        self.url = url
        self.headers = headers or {}

    async def fetch(self) -> bytes:
        request = urllib.request.Request(self.url, headers=self.headers)
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read()
        except Exception as exc:
            raise ConnectorError(f"HTTP fetch failed for {self.url}: {exc}") from exc


class S3Connector(BaseConnector):
    """Connector stub for AWS S3 object storage — requires boto3 in production."""

    def __init__(self, bucket: str, key: str, region: str = "ap-south-1") -> None:
        self.bucket = bucket
        self.key = key
        self.region = region

    async def fetch(self) -> bytes:
        # Production implementation would use aioboto3
        raise ConnectorError(
            f"S3Connector is a production stub. Configure boto3 for s3://{self.bucket}/{self.key}"
        )


class ZipConnector(BaseConnector):
    """Connector extracting a named member from a ZIP archive (local or bytes)."""

    def __init__(self, source: str | Path | bytes, member_name: str) -> None:
        self.source = source
        self.member_name = member_name

    async def fetch(self) -> bytes:
        if isinstance(self.source, (str, Path)):
            raw = await FileConnector(self.source).fetch()
        else:
            raw = self.source

        try:
            with zipfile.ZipFile(io.BytesIO(raw)) as zf:
                if self.member_name not in zf.namelist():
                    raise ConnectorError(
                        f"Member '{self.member_name}' not found in ZIP. "
                        f"Available: {zf.namelist()}"
                    )
                return zf.read(self.member_name)
        except zipfile.BadZipFile as exc:
            raise ConnectorError(f"Invalid ZIP archive: {exc}") from exc


async def stream_file_chunks(
    file_path: str | Path, chunk_size: int = 65_536
) -> AsyncIterator[bytes]:
    """Stream a local file in fixed-size chunks for memory-efficient large file processing."""
    async with aiofiles.open(file_path, "rb") as f:
        while True:
            chunk = await f.read(chunk_size)
            if not chunk:
                break
            yield chunk
