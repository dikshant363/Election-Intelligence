"""Pydantic schemas for Search API endpoints."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SearchRequestSchema(BaseModel):
    """API request model for search query."""

    model_config = ConfigDict(frozen=True)

    q: str = Field(default="", max_length=500, description="Query text string")
    query_type: str = Field(default="boolean", description="boolean, phrase, prefix, fuzzy")
    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=20, ge=1, le=100, description="Results per page")
    filters: dict[str, Any] = Field(default_factory=dict, description="Arbitrary filter key-values")
    enable_highlighting: bool = Field(default=True, description="Enable snippet highlighting")


class SearchHitSchema(BaseModel):
    """API response hit schema."""

    model_config = ConfigDict(frozen=True)

    id: str
    entity_type: str
    title: str
    subtitle: str = ""
    highlight: str = ""
    score: float = 1.0
    metadata: dict[str, Any] = Field(default_factory=dict)


class SearchResponseSchema(BaseModel):
    """API response page schema."""

    model_config = ConfigDict(frozen=True)

    hits: list[SearchHitSchema]
    total: int
    page: int
    page_size: int
    total_pages: int
    query: str
    took_ms: float
    cached: bool = False


class AutocompleteRequestSchema(BaseModel):
    """API request model for autocomplete."""

    model_config = ConfigDict(frozen=True)

    prefix: str = Field(..., min_length=1, max_length=100, description="Search prefix")
    entity_type: str = Field(default="all", description="candidate, party, constituency, election, all")
    limit: int = Field(default=10, ge=1, le=50, description="Max suggestions to return")


class AutocompleteSuggestionSchema(BaseModel):
    """API response model for autocomplete suggestion."""

    model_config = ConfigDict(frozen=True)

    id: str
    label: str
    entity_type: str
    secondary: str = ""


class GeoSearchRequestSchema(BaseModel):
    """API request model for geospatial radius search."""

    model_config = ConfigDict(frozen=True)

    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    radius_km: float = Field(default=5.0, gt=0.0, le=500.0)
    limit: int = Field(default=10, ge=1, le=100)


class GeoHitSchema(BaseModel):
    """API response model for nearest polling booth hit."""

    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    constituency_id: str
    distance_km: float
