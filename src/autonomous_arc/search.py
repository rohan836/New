"""Bounded test-time program search."""

from __future__ import annotations

from dataclasses import dataclass

from .program import candidate_programs
from .types import Candidate, Task
from .verifier import verify


@dataclass(frozen=True)
class SearchConfig:
    max_depth: int = 2
    candidate_budget: int = 128


def search(task: Task, config: SearchConfig) -> list[Candidate]:
    candidates = [
        verify(task, program)
        for program in candidate_programs(task, config.max_depth)
    ]
    candidates.sort(key=lambda c: (-c.correct, c.complexity, c.program.label()))
    exact = [c for c in candidates if c.exact]
    remainder = [c for c in candidates if not c.exact]
    return (exact + remainder)[: config.candidate_budget]
