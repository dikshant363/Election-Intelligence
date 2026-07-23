"""Query Engine: Boolean, phrase, prefix, fuzzy, multi-field, and weighted search execution."""

from __future__ import annotations

import re
import time

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.persistence.models import CandidateModel, ElectionModel
from app.search.highlighting import TextHighlighter
from app.search.queries import ParsedQueryNode, QueryType, SearchOperator, SearchQuery
from app.search.ranking import RelevanceRanker, ScoredHit
from app.search.results import SearchHit, SearchPage

_CLEAN_RE = re.compile(r"[^\w\s\-\.\*]", re.UNICODE)


class QueryParser:
    """Parses raw text queries into a structured Query AST (ParsedQueryNode)."""

    @staticmethod
    def parse(raw_query: str) -> ParsedQueryNode:
        """Parse query string into AST node structure."""
        cleaned = _CLEAN_RE.sub("", raw_query).strip()
        tokens = [t for t in cleaned.split() if t]

        if not tokens:
            return ParsedQueryNode(token="")

        children = []
        for t in tokens:
            is_prefix = t.endswith("*")
            token_clean = t.rstrip("*")
            children.append(
                ParsedQueryNode(
                    token=token_clean,
                    is_prefix=is_prefix,
                    operator=SearchOperator.AND,
                )
            )

        return ParsedQueryNode(
            token=cleaned,
            operator=SearchOperator.AND,
            children=children,
        )


class QueryEngine:
    """Executes SearchQuery requests against PostgreSQL FTS or relational tables."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._highlighter = TextHighlighter()
        self._ranker = RelevanceRanker()

    def build_tsquery_string(self, query: SearchQuery) -> str:
        """Convert SearchQuery into PostgreSQL tsquery string according to QueryType."""
        raw = query.raw_query.strip()
        if not raw:
            return ""

        tokens = [t for t in _CLEAN_RE.sub("", raw).split() if t]
        if not tokens:
            return ""

        if query.query_type == QueryType.PHRASE or query.is_phrase:
            # Phrase search: tokens joined with <->
            return " <-> ".join(tokens)

        if query.query_type == QueryType.PREFIX:
            # Prefix search: tokens joined with :*
            return " & ".join(f"{t}:*" for t in tokens)

        if query.operator == SearchOperator.OR:
            return " | ".join(f"{t}:*" for t in tokens)

        # Default AND boolean prefix search
        return " & ".join(f"{t}:*" for t in tokens)

    async def execute_query(self, query: SearchQuery) -> SearchPage:
        """Execute universal SearchQuery and return paginated, ranked, highlighted results."""
        t0 = time.monotonic()
        tsq_str = self.build_tsquery_string(query)

        raw_hits: list[ScoredHit] = []
        total_count = 0

        # Query Elections
        stmt_el = select(ElectionModel).where(ElectionModel.deleted_at.is_(None))
        if tsq_str:
            tsvector = func.to_tsvector("english", ElectionModel.title)
            stmt_el = stmt_el.where(tsvector.op("@@")(func.to_tsquery("english", tsq_str)))

        elections = (await self._session.execute(stmt_el)).scalars().all()
        total_count += len(elections)

        for el in elections:
            score = self._ranker.config.title_boost if tsq_str else 1.0
            highlighted = (
                self._highlighter.extract_snippet(el.title, query.raw_query.split())
                if query.enable_highlighting
                else el.title
            )
            raw_hits.append(
                ScoredHit(
                    id=str(el.id),
                    entity_type="election",
                    title=el.title,
                    raw_score=score,
                    highlight=highlighted,
                    field_boost=self._ranker.config.title_boost,
                    metadata={"election_type": el.election_type, "status": el.status},
                )
            )

        # Query Candidates
        stmt_cand = select(CandidateModel).where(CandidateModel.deleted_at.is_(None))
        if tsq_str:
            tsvector = func.to_tsvector("english", CandidateModel.name)
            stmt_cand = stmt_cand.where(tsvector.op("@@")(func.to_tsquery("english", tsq_str)))

        candidates = (await self._session.execute(stmt_cand)).scalars().all()
        total_count += len(candidates)

        for cand in candidates:
            score = self._ranker.config.name_boost if tsq_str else 1.0
            highlighted = (
                self._highlighter.extract_snippet(cand.name, query.raw_query.split())
                if query.enable_highlighting
                else cand.name
            )
            raw_hits.append(
                ScoredHit(
                    id=str(cand.id),
                    entity_type="candidate",
                    title=cand.name,
                    raw_score=score,
                    highlight=highlighted,
                    field_boost=self._ranker.config.name_boost,
                    metadata={"age": cand.age, "email": cand.email},
                )
            )

        # Rank hits
        ranked = self._ranker.rank_hits(raw_hits)

        # Paginate
        start = query.pagination.offset
        end = start + query.pagination.page_size
        page_hits = ranked[start:end]

        search_hits = [
            SearchHit(
                id=h.id,
                entity_type=h.entity_type,
                title=h.title,
                score=h.final_score,
                highlight=h.highlight,
                metadata=h.metadata,
            )
            for h in page_hits
        ]

        took_ms = (time.monotonic() - t0) * 1000.0

        return SearchPage(
            hits=search_hits,
            total=total_count,
            page=query.pagination.page,
            page_size=query.pagination.page_size,
            query=query.raw_query,
            took_ms=round(took_ms, 2),
        )
