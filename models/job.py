from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class JobPosting:
    source: str
    title: str
    company: str
    location: str
    url: str
    date_found: datetime
    distance_miles: Optional[float] = None
    description_snippet: Optional[str] = None
