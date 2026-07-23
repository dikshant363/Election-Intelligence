"""ETL data export: CSV, JSON, Parquet, GeoJSON output from staging or production tables."""

from __future__ import annotations

import contextlib
import csv
import io
import json
from datetime import UTC, datetime
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq


class CsvExporter:
    """Export records to CSV bytes."""

    def export(self, records: list[dict[str, Any]], delimiter: str = ",") -> bytes:
        if not records:
            return b""
        fieldnames = list(records[0].keys())
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(records)
        return output.getvalue().encode("utf-8")


class JsonExporter:
    """Export records to JSON bytes with ISO-8601 date serialization."""

    def export(self, records: list[dict[str, Any]], indent: int = 2) -> bytes:
        return json.dumps(records, ensure_ascii=False, indent=indent, default=str).encode("utf-8")


class ParquetExporter:
    """Export records to Apache Parquet bytes using pyarrow."""

    def export(self, records: list[dict[str, Any]]) -> bytes:
        if not records:
            return b""
        table = pa.Table.from_pylist(records)
        buf = io.BytesIO()
        pq.write_table(table, buf)
        return buf.getvalue()


class GeoJsonExporter:
    """Export records containing geometry to GeoJSON FeatureCollection bytes."""

    def export(
        self,
        records: list[dict[str, Any]],
        lat_field: str = "latitude",
        lon_field: str = "longitude",
    ) -> bytes:
        features = []
        for record in records:
            lat = record.get(lat_field)
            lon = record.get(lon_field)
            geometry = None
            if lat is not None and lon is not None:
                with contextlib.suppress(ValueError, TypeError):
                    geometry = {
                        "type": "Point",
                        "coordinates": [float(lon), float(lat)],
                    }

            properties = {k: v for k, v in record.items() if k not in (lat_field, lon_field)}
            features.append(
                {
                    "type": "Feature",
                    "geometry": geometry,
                    "properties": properties,
                }
            )
        collection = {
            "type": "FeatureCollection",
            "features": features,
            "metadata": {
                "exported_at": datetime.now(UTC).isoformat(),
                "total_features": len(features),
            },
        }
        return json.dumps(collection, ensure_ascii=False, default=str).encode("utf-8")


def export_records(
    records: list[dict[str, Any]],
    format: str,
    **kwargs: Any,
) -> bytes:
    """Unified export entry point. format: 'csv' | 'json' | 'parquet' | 'geojson'."""
    exporters: dict[str, Any] = {
        "csv": CsvExporter(),
        "json": JsonExporter(),
        "parquet": ParquetExporter(),
        "geojson": GeoJsonExporter(),
    }
    if format not in exporters:
        raise ValueError(f"Unsupported export format: '{format}'. Choose from {list(exporters)}")
    exporter = exporters[format]
    return exporter.export(records, **kwargs)
