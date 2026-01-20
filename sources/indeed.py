from __future__ import annotations

from typing import Iterable
from sources.base import JobSource
from models.job import JobPosting


class IndeedSource(JobSource):
    name = "indeed"

    def search(self) -> Iterable[JobPosting]:
        # TODO: implement real search in a later sprint
        return []
