"""Normalization transformers for election domain data."""

from __future__ import annotations

import contextlib
import re
from datetime import datetime
from typing import Any

# Phone number length constants
_PHONE_LEN_10 = 10
_PHONE_LEN_12 = 12

# ─── Indian State / UT name normalisation ────────────────────────────────────
_STATE_ALIASES: dict[str, str] = {
    "andhra": "Andhra Pradesh",
    "andhra pradesh": "Andhra Pradesh",
    "ap": "Andhra Pradesh",
    "arunachal": "Arunachal Pradesh",
    "arunachal pradesh": "Arunachal Pradesh",
    "assam": "Assam",
    "bihar": "Bihar",
    "chhattisgarh": "Chhattisgarh",
    "chattisgarh": "Chhattisgarh",
    "goa": "Goa",
    "gujarat": "Gujarat",
    "haryana": "Haryana",
    "himachal": "Himachal Pradesh",
    "himachal pradesh": "Himachal Pradesh",
    "jharkhand": "Jharkhand",
    "karnataka": "Karnataka",
    "kerala": "Kerala",
    "madhya pradesh": "Madhya Pradesh",
    "mp": "Madhya Pradesh",
    "maharashtra": "Maharashtra",
    "manipur": "Manipur",
    "meghalaya": "Meghalaya",
    "mizoram": "Mizoram",
    "nagaland": "Nagaland",
    "odisha": "Odisha",
    "orissa": "Odisha",
    "punjab": "Punjab",
    "rajasthan": "Rajasthan",
    "sikkim": "Sikkim",
    "tamil nadu": "Tamil Nadu",
    "tn": "Tamil Nadu",
    "telangana": "Telangana",
    "tripura": "Tripura",
    "uttar pradesh": "Uttar Pradesh",
    "up": "Uttar Pradesh",
    "uttarakhand": "Uttarakhand",
    "west bengal": "West Bengal",
    "wb": "West Bengal",
    "delhi": "Delhi",
    "nct delhi": "Delhi",
    "jammu kashmir": "Jammu & Kashmir",
    "j&k": "Jammu & Kashmir",
    "ladakh": "Ladakh",
    "puducherry": "Puducherry",
    "pondicherry": "Puducherry",
}

_ELECTION_TYPE_ALIASES: dict[str, str] = {
    "ls": "Lok Sabha",
    "lok sabha": "Lok Sabha",
    "rs": "Rajya Sabha",
    "rajya sabha": "Rajya Sabha",
    "assembly": "State Assembly",
    "vidhan sabha": "State Assembly",
    "state assembly": "State Assembly",
    "by election": "By-Election",
    "bypolls": "By-Election",
    "by-election": "By-Election",
    "local body": "Local Body",
    "municipal": "Municipal",
    "panchayat": "Panchayat",
}


def normalize_state(raw: str) -> str:
    """Normalize Indian state/UT name to canonical form."""
    key = raw.strip().lower()
    return _STATE_ALIASES.get(key, raw.strip().title())


def normalize_election_type(raw: str) -> str:
    """Normalize election type descriptor to canonical form."""
    key = raw.strip().lower()
    return _ELECTION_TYPE_ALIASES.get(key, raw.strip().title())


def normalize_date(raw: str, formats: list[str] | None = None) -> str | None:
    """Parse a date string into ISO-8601 YYYY-MM-DD format. Returns None on failure."""
    if not raw or not str(raw).strip():
        return None

    candidate = str(raw).strip()
    default_formats = formats or [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%d %b %Y",
        "%d %B %Y",
        "%Y/%m/%d",
        "%d.%m.%Y",
    ]
    for fmt in default_formats:
        with contextlib.suppress(ValueError):
            return datetime.strptime(candidate, fmt).date().isoformat()
    return None


def normalize_party_code(raw: str) -> str:
    """Uppercase and strip whitespace from party code."""
    return re.sub(r"\s+", "", raw.strip().upper())


def normalize_constituency_code(raw: str) -> str:
    """Pad constituency codes to consistent 3-digit format (e.g., '7' → '007')."""
    clean = re.sub(r"[^\w]", "", str(raw).strip())
    if clean.isdigit():
        return clean.zfill(3)
    return clean.upper()


def normalize_phone(raw: str) -> str:
    """Strip non-digits and normalize Indian phone numbers."""
    digits = re.sub(r"\D", "", str(raw))
    if len(digits) == _PHONE_LEN_10:
        return f"+91{digits}"
    if len(digits) == _PHONE_LEN_12 and digits.startswith("91"):
        return f"+{digits}"
    return digits


def normalize_coordinates(raw: str) -> float | None:
    """Parse coordinate string to float. Returns None on failure."""
    with contextlib.suppress(ValueError, TypeError):
        return float(str(raw).strip())
    return None


class RecordTransformer:
    """
    Configurable field-level transformer.

    field_transforms is a dict mapping field_name -> callable(value) -> new_value.
    """

    def __init__(self, field_transforms: dict[str, Any]) -> None:
        self.field_transforms = field_transforms

    def transform(self, record: dict[str, Any]) -> dict[str, Any]:
        """Apply configured transforms to a single record. Returns transformed copy."""
        result = dict(record)
        for field_name, transform_fn in self.field_transforms.items():
            if field_name in result:
                with contextlib.suppress(Exception):
                    result[field_name] = transform_fn(result[field_name])
        return result

    def transform_batch(
        self, records: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Apply transforms to a list of records."""
        return [self.transform(r) for r in records]


# ─── Pre-built transformers for common election data domains ─────────────────
ELECTION_DATASET_TRANSFORMER = RecordTransformer(
    field_transforms={
        "state": normalize_state,
        "state_name": normalize_state,
        "election_type": normalize_election_type,
        "date": normalize_date,
        "election_date": normalize_date,
        "party_code": normalize_party_code,
        "party": normalize_party_code,
        "constituency_code": normalize_constituency_code,
        "latitude": normalize_coordinates,
        "longitude": normalize_coordinates,
        "lat": normalize_coordinates,
        "lon": normalize_coordinates,
    }
)

CANDIDATE_DATASET_TRANSFORMER = RecordTransformer(
    field_transforms={
        "state": normalize_state,
        "party_code": normalize_party_code,
        "party": normalize_party_code,
        "constituency_code": normalize_constituency_code,
        "phone": normalize_phone,
        "dob": normalize_date,
        "date_of_birth": normalize_date,
    }
)
