# Search Query Engine & Syntax Guide

## Overview

The Query Engine (`backend/app/search/engine/`) translates user input strings and `SearchQuery` objects into optimized PostgreSQL `tsquery` expressions or SQL conditions.

---

## Supported Query Types

### 1. Boolean Search (`QueryType.BOOLEAN`)
Combines search terms with boolean logic (`AND`, `OR`, `NOT`).
- **Input**: `"Lok Sabha"`
- **tsquery**: `lok:* & sabha:*`

### 2. Phrase Search (`QueryType.PHRASE`)
Requires exact term sequence adjacency using the distance operator `<->`.
- **Input**: `"Lok Sabha"`
- **tsquery**: `lok <-> sabha`

### 3. Prefix Search (`QueryType.PREFIX`)
Matches words beginning with the specified prefix wildcard (`*`).
- **Input**: `"Rah*"`
- **tsquery**: `rah:*`

### 4. Fuzzy & Multi-field Search
Fuzzy Levenshtein distance matching and field boosting across multiple columns.

---

## Filtering Architecture

The `SearchFilterSet` class allows arbitrary combinations of domain filters:
- **Election**: `election_id`, `election_type`, `status`, `election_year`
- **Geography**: `state_code`, `district`, `constituency_code`
- **Identity**: `party_code`, `candidate_id`, `gender`
- **Temporal**: `date_from`, `date_to`

```python
from app.search.filters import SearchFilterSet

filters = SearchFilterSet(
    election_type="GENERAL",
    state_code="DL",
    election_year=2024,
)
filters.validate()
```

---

## Relevance Ranking & Scoring

Final hit relevance score is computed as:

$$\text{Final Score} = \text{Raw Score} \times \text{Field Boost} \times \text{Recency Boost} \times \text{Popularity Boost}$$

### Field Boost Weights
- Title / Election Name: `3.0x`
- Candidate Name: `2.5x`
- Party / Constituency Code: `2.0x`
- Description Body: `1.0x`

---

## Snippet Highlighting

`TextHighlighter` extracts text fragments around matched query terms and wraps them in configurable HTML tags (default: `<mark>...</mark>`):

```python
highlighter = TextHighlighter(HighlightConfig(fragment_size=150))
snippet = highlighter.extract_snippet(text, ["Lok", "Sabha"])
```
