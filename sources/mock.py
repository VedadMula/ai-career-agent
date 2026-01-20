from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

from models.job import JobPosting
from sources.base import JobSource


class MockSource(JobSource):
    name = "mock"

    def search(self) -> Iterable[JobPosting]:
        now = datetime.now(timezone.utc)

        # These are intentionally realistic “cybersecurity-ish” examples.
        # We’ll replace this source with real endpoints in later sprints.
        return [
            JobPosting(
                source=self.name,
                title="SOC Analyst (Tier 1)",
                company="Acme Security",
                location="Budd Lake, NJ",
                url="https://example.com/jobs/soc-analyst-tier-1",
                date_found=now,
                distance_miles=0.8,
                description_snippet="Monitor SIEM alerts, triage incidents, escalate as needed.",
            ),
            JobPosting(
                source=self.name,
                title="GRC Analyst (Junior)",
                company="North Ridge Compliance",
                location="Randolph, NJ",
                url="https://example.com/jobs/grc-analyst-jr",
                date_found=now,
                distance_miles=0.9,
                description_snippet="Assist with risk assessments, policies, and audit evidence collection.",
            ),
        ]
