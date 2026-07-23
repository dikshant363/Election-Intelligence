"""FastAPI router for /api/v1/search endpoints."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query, status

from app.api.v1.dependencies.dependencies import get_search_service
from app.search.queries import Pagination, QueryType, SearchQuery
from app.search.schemas import (
    AutocompleteSuggestionSchema,
    GeoHitSchema,
    SearchHitSchema,
    SearchResponseSchema,
)
from app.search.services import SearchService

router = APIRouter(prefix="/search", tags=["Search & Discovery"])


@router.get(
    "",
    response_model=SearchResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Execute multi-field search",
)
async def execute_search(
    q: Annotated[str, Query(max_length=500, description="Query string")] = "",
    query_type: Annotated[str, Query(description="boolean, phrase, prefix, fuzzy")] = "boolean",
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    search_service: SearchService = Depends(get_search_service),
) -> SearchResponseSchema:
    """Execute search query through Search Abstraction Layer (SAL)."""
    search_query = SearchQuery(
        raw_query=q,
        query_type=QueryType(query_type) if query_type in QueryType else QueryType.BOOLEAN,
        pagination=Pagination(page=page, page_size=page_size),
    )
    result_page = await search_service.search(search_query)

    hits_schema = [
        SearchHitSchema(
            id=h.id,
            entity_type=h.entity_type,
            title=h.title,
            subtitle=h.subtitle,
            highlight=h.highlight,
            score=h.score,
            metadata=h.metadata,
        )
        for h in result_page.hits
    ]

    return SearchResponseSchema(
        hits=hits_schema,
        total=result_page.total,
        page=result_page.page,
        page_size=result_page.page_size,
        total_pages=result_page.total_pages,
        query=result_page.query,
        took_ms=result_page.took_ms,
    )


@router.get(
    "/autocomplete",
    response_model=list[AutocompleteSuggestionSchema],
    status_code=status.HTTP_200_OK,
    summary="Fetch typeahead suggestions",
)
async def autocomplete(
    prefix: Annotated[str, Query(min_length=1, max_length=100)],
    entity_type: Annotated[str, Query()] = "all",
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
    search_service: SearchService = Depends(get_search_service),
) -> list[AutocompleteSuggestionSchema]:
    """Fetch prefix autocomplete suggestions."""
    suggestions = await search_service.autocomplete(prefix, entity_type, limit)
    return [
        AutocompleteSuggestionSchema(
            id=s.id,
            label=s.label,
            entity_type=s.entity_type,
            secondary=s.secondary,
        )
        for s in suggestions
    ]


@router.get(
    "/geospatial",
    response_model=list[GeoHitSchema],
    status_code=status.HTTP_200_OK,
    summary="Geospatial proximity search",
)
async def geospatial_search(
    latitude: Annotated[float, Query(ge=-90.0, le=90.0)],
    longitude: Annotated[float, Query(ge=-180.0, le=180.0)],
    radius_km: Annotated[float, Query(gt=0.0, le=500.0)] = 5.0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    search_service: SearchService = Depends(get_search_service),
) -> list[GeoHitSchema]:
    """Search for nearest polling booths within radius."""
    booths = await search_service.find_nearest_polling_booths(
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
        limit=limit,
    )
    return [
        GeoHitSchema(
            id=b["id"],
            name=b["name"],
            constituency_id=b["constituency_id"],
            distance_km=b["distance_km"],
        )
        for b in booths
    ]


@router.get(
    "/analytics",
    response_model=dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Get search analytics & aggregations",
)
async def analytics(
    search_service: SearchService = Depends(get_search_service),
) -> dict[str, Any]:
    """Return aggregated election statistical metrics."""
    by_state = await search_service.get_analytics_by_state()
    by_party = await search_service.get_analytics_by_party()
    turnout = await search_service.get_turnout_statistics()

    return {
        "constituency_count_by_state": by_state.data,
        "candidate_count_by_party": by_party.data,
        "turnout_statistics": turnout,
    }


@router.post(
    "/reindex",
    status_code=status.HTTP_200_OK,
    summary="Trigger search index reindex",
)
async def reindex(
    search_service: SearchService = Depends(get_search_service),
) -> dict[str, Any]:
    """Trigger full reindex of search indices."""
    stats = await search_service.reindex_all()
    return {
        "index_name": stats.index_name,
        "version": stats.version,
        "total_documents": stats.total_documents,
        "last_indexed_at": stats.last_indexed_at.isoformat() if stats.last_indexed_at else None,
    }
