from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable
from models.job import JobPosting


class JobSource(ABC):
    name: str

    @abstractmethod
    def search(self) -> Iterable[JobPosting]:
        """
        Perform a job search and yield JobPosting results.
        No side effects. No persistence.
        """
        raise NotImplementedError
