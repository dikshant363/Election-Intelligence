"""Data format parsers: CSV, Excel, JSON, GeoJSON, Parquet, ZIP."""

from __future__ import annotations

import csv
import io
import json
import zipfile
from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Any

import openpyxl
import pyarrow.parquet as pq

from app.etl.exceptions import ParseError


class DataParser(ABC):
    """Abstract interface for all format parsers."""

    @abstractmethod
    def parse(self, data: bytes) -> list[dict[str, Any]]:
        """Parse raw bytes into a list of record dicts."""

    def parse_chunked(
        self, data: bytes, chunk_size: int = 1000
    ) -> Iterator[list[dict[str, Any]]]:
        """Yield records in chunks. Default: parse all then chunk."""
        records = self.parse(data)
        for i in range(0, len(records), chunk_size):
            yield records[i : i + chunk_size]


class CsvParser(DataParser):
    """Streaming CSV parser supporting large files and configurable encoding."""

    def __init__(
        self, encoding: str = "utf-8", delimiter: str = ","
    ) -> None:
        self.encoding = encoding
        self.delimiter = delimiter

    def parse(self, data: bytes) -> list[dict[str, Any]]:
        try:
            text = data.decode(self.encoding, errors="replace")
            reader = csv.DictReader(io.StringIO(text), delimiter=self.delimiter)
            return [dict(row) for row in reader]
        except Exception as exc:
            raise ParseError(f"CSV parse failure: {exc}") from exc

    def parse_chunked(
        self, data: bytes, chunk_size: int = 1000
    ) -> Iterator[list[dict[str, Any]]]:
        """Streaming chunked CSV parse — avoids loading all rows into memory."""
        try:
            text = data.decode(self.encoding, errors="replace")
            reader = csv.DictReader(io.StringIO(text), delimiter=self.delimiter)
            chunk: list[dict[str, Any]] = []
            for row in reader:
                chunk.append(dict(row))
                if len(chunk) >= chunk_size:
                    yield chunk
                    chunk = []
            if chunk:
                yield chunk
        except Exception as exc:
            raise ParseError(f"CSV streaming parse failure: {exc}") from exc


class ExcelParser(DataParser):
    """Excel (.xlsx) parser using openpyxl."""

    def __init__(self, sheet_name: str | int = 0) -> None:
        self.sheet_name = sheet_name

    def parse(self, data: bytes) -> list[dict[str, Any]]:
        try:
            wb = openpyxl.load_workbook(io.BytesIO(data), read_only=True, data_only=True)
            if isinstance(self.sheet_name, int):
                ws = wb.worksheets[self.sheet_name]
            else:
                ws = wb[self.sheet_name]

            rows = list(ws.iter_rows(values_only=True))
            if not rows:
                return []
            headers = [str(h) if h is not None else f"col_{i}" for i, h in enumerate(rows[0])]
            records = [
                dict(zip(headers, [str(v) if v is not None else "" for v in row], strict=False))
                for row in rows[1:]
            ]
            wb.close()
            return records
        except Exception as exc:
            raise ParseError(f"Excel parse failure: {exc}") from exc


class JsonParser(DataParser):
    """JSON / JSON-Lines parser."""

    def __init__(self, json_lines: bool = False) -> None:
        self.json_lines = json_lines

    def parse(self, data: bytes) -> list[dict[str, Any]]:
        try:
            text = data.decode("utf-8", errors="replace")
            if self.json_lines:
                records = []
                for raw_line in text.splitlines():
                    stripped = raw_line.strip()
                    if stripped:
                        records.append(json.loads(stripped))
                return records
            payload = json.loads(text)
            if isinstance(payload, list):
                return payload
            if isinstance(payload, dict):
                # Support {"data": [...]} envelope pattern
                for key in ("data", "records", "results", "items"):
                    if key in payload and isinstance(payload[key], list):
                        return payload[key]
                return [payload]
            raise ParseError(f"JSON root must be list or object, got {type(payload).__name__}")
        except ParseError:
            raise
        except Exception as exc:
            raise ParseError(f"JSON parse failure: {exc}") from exc


class GeoJsonParser(DataParser):
    """GeoJSON FeatureCollection parser emitting flattened records."""

    def parse(self, data: bytes) -> list[dict[str, Any]]:
        try:
            text = data.decode("utf-8", errors="replace")
            geo = json.loads(text)
            if geo.get("type") != "FeatureCollection":
                raise ParseError("GeoJSON root must be a FeatureCollection")
            records = []
            for feature in geo.get("features", []):
                record: dict[str, Any] = dict(feature.get("properties") or {})
                geometry = feature.get("geometry")
                if geometry:
                    record["_geometry_type"] = geometry.get("type")
                    record["_geometry"] = json.dumps(geometry)
                records.append(record)
            return records
        except ParseError:
            raise
        except Exception as exc:
            raise ParseError(f"GeoJSON parse failure: {exc}") from exc


class ParquetParser(DataParser):
    """Apache Parquet parser using pyarrow."""

    def parse(self, data: bytes) -> list[dict[str, Any]]:
        try:
            table = pq.read_table(io.BytesIO(data))
            return table.to_pylist()
        except Exception as exc:
            raise ParseError(f"Parquet parse failure: {exc}") from exc


class ZipParser(DataParser):
    """ZIP archive parser that recursively parses the first supported member."""

    EXTENSION_MAP: dict[str, type[DataParser]] = {
        ".csv": CsvParser,
        ".json": JsonParser,
        ".geojson": GeoJsonParser,
        ".xlsx": ExcelParser,
    }

    def parse(self, data: bytes) -> list[dict[str, Any]]:
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as zf:
                for name in zf.namelist():
                    ext = "." + name.rsplit(".", 1)[-1].lower() if "." in name else ""
                    parser_cls = self.EXTENSION_MAP.get(ext)
                    if parser_cls:
                        member_bytes = zf.read(name)
                        return parser_cls().parse(member_bytes)
                raise ParseError(
                    f"No supported file found in ZIP. Members: {zf.namelist()}"
                )
        except ParseError:
            raise
        except Exception as exc:
            raise ParseError(f"ZIP parse failure: {exc}") from exc


def get_parser_for_extension(filename: str) -> DataParser:
    """Return appropriate parser based on file extension."""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    mapping: dict[str, DataParser] = {
        "csv": CsvParser(),
        "xlsx": ExcelParser(),
        "json": JsonParser(),
        "geojson": GeoJsonParser(),
        "parquet": ParquetParser(),
        "zip": ZipParser(),
    }
    if ext not in mapping:
        raise ParseError(f"Unsupported file extension: .{ext}")
    return mapping[ext]
