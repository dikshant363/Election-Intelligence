"""Geospatial queries: radius, bounding box, polygon, nearest polling booths."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.persistence.models import PollingBoothModel
from app.search.exceptions import GeospatialError

EARTH_RADIUS_KM = 6371.0


@dataclass
class Point:
    """Geographic point coordinate."""

    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        if not (-90.0 <= self.latitude <= 90.0):  # noqa: PLR2004
            raise GeospatialError(f"Latitude out of bounds: {self.latitude}")
        if not (-180.0 <= self.longitude <= 180.0):  # noqa: PLR2004
            raise GeospatialError(f"Longitude out of bounds: {self.longitude}")


@dataclass
class BoundingBox:
    """Geographic bounding box defined by min/max coordinates."""

    min_lat: float
    min_lon: float
    max_lat: float
    max_lon: float

    def contains(self, point: Point) -> bool:
        return (
            self.min_lat <= point.latitude <= self.max_lat
            and self.min_lon <= point.longitude <= self.max_lon
        )


@dataclass
class Polygon:
    """Geographic polygon defined by a list of boundary Points."""

    vertices: list[Point]

    def contains(self, point: Point) -> bool:
        """Ray-casting algorithm to determine if point is inside polygon."""
        n = len(self.vertices)
        if n < 3:  # noqa: PLR2004
            return False

        inside = False
        p1 = self.vertices[0]
        for i in range(n + 1):
            p2 = self.vertices[i % n]
            if point.latitude > min(p1.latitude, p2.latitude):
                if point.latitude <= max(p1.latitude, p2.latitude):
                    if point.longitude <= max(p1.longitude, p2.longitude):
                        if p1.latitude != p2.latitude:
                            xinters = (point.latitude - p1.latitude) * (
                                p2.longitude - p1.longitude
                            ) / (p2.latitude - p1.latitude) + p1.longitude
                        if p1.longitude == p2.longitude or point.longitude <= xinters:
                            inside = not inside
            p1 = p2
        return inside


def haversine_distance(p1: Point, p2: Point) -> float:
    """Calculate Haversine distance in kilometers between two Points in Python."""
    lat1, lon1 = math.radians(p1.latitude), math.radians(p1.longitude)
    lat2, lon2 = math.radians(p2.latitude), math.radians(p2.longitude)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(EARTH_RADIUS_KM * c, 3)


class SpatialSearchEngine:
    """Executes spatial queries against PostgreSQL / PostGIS or Haversine math fallback."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_nearest_polling_booths(
        self,
        center: Point,
        radius_km: float = 5.0,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """Find polling booths within radius_km ordered by proximity."""
        haversine_sql = text("""
            6371.0 * acos(
                LEAST(1.0, GREATEST(-1.0,
                    cos(radians(:lat)) * cos(radians(latitude))
                    * cos(radians(longitude) - radians(:lon))
                    + sin(radians(:lat)) * sin(radians(latitude))
                ))
            )
        """)

        stmt = (
            select(PollingBoothModel, haversine_sql.label("distance_km"))
            .where(haversine_sql <= radius_km)
            .order_by(haversine_sql.asc())
            .limit(limit)
        )

        params = {"lat": center.latitude, "lon": center.longitude}
        rows = (await self._session.execute(stmt, params)).all()

        return [
            {
                "id": str(booth.id),
                "name": booth.name,
                "constituency_id": str(booth.constituency_id),
                "distance_km": round(float(dist), 3),
            }
            for booth, dist in rows
        ]

    async def search_bounding_box(
        self, bbox: BoundingBox, limit: int = 100
    ) -> list[dict[str, Any]]:
        """Find polling booths inside a bounding box."""
        stmt = (
            select(PollingBoothModel)
            .where(PollingBoothModel.latitude >= bbox.min_lat)
            .where(PollingBoothModel.latitude <= bbox.max_lat)
            .where(PollingBoothModel.longitude >= bbox.min_lon)
            .where(PollingBoothModel.longitude <= bbox.max_lon)
            .limit(limit)
        )

        rows = (await self._session.execute(stmt)).scalars().all()
        return [
            {
                "id": str(b.id),
                "name": b.name,
                "latitude": b.latitude,
                "longitude": b.longitude,
            }
            for b in rows
        ]
