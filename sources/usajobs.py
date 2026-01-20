from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Iterable

import requests

from models.job import JobPosting


class UsaJobsSource:
    """
    Real job source using the official USAJOBS API (no scraping).
    Requires env vars:
      - USAJOBS_API_KEY
      - USAJOBS_USER_AGENT (use your email)
    """
    name = "usajobs"

    def __init__(self) -> None:
        self.api_key = os.getenv("USAJOBS_API_KEY", "").strip()
        self.user_agent = os.getenv("USAJOBS_USER_AGENT", "").strip()
        self.base_url = "https://data.usajobs.gov/api/search"

    def search(
        self,
        *,
        keyword: str = "cybersecurity",
        location_name: str = "Budd Lake, NJ",
        radius_miles: int = 50,
        results_per_page: int = 25,
        page: int = 1,
    ) -> Iterable[JobPosting]:
        # Safe default: if not configured, return no results
        if not self.api_key or not self.user_agent:
            print("WARNING: USAJOBS env vars not set (USAJOBS_API_KEY / USAJOBS_USER_AGENT) - skipping")
            return []

        headers = {
            "Host": "data.usajobs.gov",
            "User-Agent": self.user_agent,
            "Authorization-Key": self.api_key,
            "Accept": "application/json",
        }

        params = {
            "Keyword": keyword,
            "LocationName": location_name,
            "Radius": str(radius_miles),
            "ResultsPerPage": str(results_per_page),
            "Page": str(page),
        }

        resp = requests.get(self.base_url, headers=headers, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        items = (data.get("SearchResult", {}) or {}).get("SearchResultItems", []) or []
        now = datetime.now(timezone.utc)

        results: list[Job] = []
        for it in items:
            d = (it.get("MatchedObjectDescriptor", {}) or {})

            title = d.get("PositionTitle") or ""
            org = d.get("OrganizationName") or ""

            # PositionURI is usually the canonical listing URL
            url = d.get("PositionURI") or ""

            # Location is typically in PositionLocation list
            locs = d.get("PositionLocation", []) or []
            location = (locs[0].get("LocationName") if locs else "") or ""

            results.append(
                JobPosting(
                    source=self.name,
                    title=title,
                    company=org,
                    location=location,
                    url=url,
                    date_found=now,
                    distance_miles=0.0,  # USAJOBS doesn't give distance
                    description_snippet="USAJOBS listing",
                )
            )

        return results
