"""Autonomous solve loop."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from time import perf_counter
from typing import Any

from .program import execute
from .providers import ProposalProvider
from .search import SearchConfig, search
from .types import SolveResult, Task


@dataclass(frozen=True)
class SolverConfig:
    max_depth: int = 2
    beam_size: int = 128
    attempts: int = 2


class AutonomousSolver:
    def __init__(
        self,
        config: SolverConfig | None = None,
        proposal_provider: ProposalProvider | None = None,
    ) -> None:
        self.config = config or SolverConfig()
        self.proposal_provider = proposal_provider

    def solve(self, task: Task) -> SolveResult:
        started = perf_counter()

        candidates = search(
            task,
            SearchConfig(
                max_depth=self.config.max_depth,
                beam_size=self.config.beam_size,
            ),
        )

        if self.proposal_provider is not None:
            from .verifier import verify
            proposed = [
                verify(task, program, source="model")
                for program in self.proposal_provider.propose(task)
            ]
            candidates = sorted(
                candidates + proposed,
                key=lambda c: (-c.correct, c.complexity, c.source, c.program.label()),
            )[: self.config.beam_size]

        predictions = []
        seen = set()
        trace_candidates: list[dict[str, Any]] = []

        for candidate in candidates:
            if candidate.correct < candidate.total:
                continue
            for test_example in task.test:
                try:
                    prediction = execute(candidate.program, test_example.input)
                except (ValueError, IndexError, TypeError):
                    continue
                if prediction not in seen:
                    predictions.append(prediction)
                    seen.add(prediction)
                if len(predictions) >= self.config.attempts:
                    break
            trace_candidates.append(
                {
                    "program": candidate.program.label(),
                    "correct": candidate.correct,
                    "total": candidate.total,
                    "complexity": candidate.complexity,
                    "source": candidate.source,
                }
            )
            if len(predictions) >= self.config.attempts:
                break

        elapsed = perf_counter() - started
        return SolveResult(
            task_id=task.task_id,
            candidates=candidates,
            predictions=predictions,
            traces=[
                {
                    "task_id": task.task_id,
                    "config": asdict(self.config),
                    "elapsed_seconds": elapsed,
                    "candidate_trace": trace_candidates,
                    "prediction_count": len(predictions),
                    "verified_solution_found": any(c.exact for c in candidates),
                }
            ],
        )
