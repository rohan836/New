"""Autonomous solve loop."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from time import perf_counter

from .program import execute
from .providers import ProposalProvider
from .search import SearchConfig, search
from .types import Grid, SolveResult, Task


@dataclass(frozen=True)
class SolverConfig:
    max_depth: int = 2
    candidate_budget: int = 128
    attempts: int = 2

    def __post_init__(self) -> None:
        if self.max_depth < 1:
            raise ValueError("max_depth must be at least 1")
        if self.candidate_budget < 1:
            raise ValueError("candidate_budget must be positive")
        if self.attempts < 1:
            raise ValueError("attempts must be positive")


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
                candidate_budget=self.config.candidate_budget,
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
            )[: self.config.candidate_budget]

        verified = [candidate for candidate in candidates if candidate.exact]
        predictions_by_test: list[list[Grid]] = []
        per_test_trace = []

        for test_index, test_example in enumerate(task.test):
            predictions: list[Grid] = []
            seen: set[Grid] = set()
            programs_used: list[str] = []

            for candidate in verified:
                try:
                    prediction = execute(candidate.program, test_example.input)
                except (ValueError, IndexError, TypeError):
                    continue

                if prediction not in seen:
                    predictions.append(prediction)
                    seen.add(prediction)
                    programs_used.append(candidate.program.label())

                if len(predictions) >= self.config.attempts:
                    break

            predictions_by_test.append(predictions)
            per_test_trace.append(
                {
                    "test_index": test_index,
                    "prediction_count": len(predictions),
                    "programs": programs_used,
                }
            )

        elapsed = perf_counter() - started

        return SolveResult(
            task_id=task.task_id,
            candidates=candidates,
            predictions=predictions_by_test,
            traces=[
                {
                    "task_id": task.task_id,
                    "config": asdict(self.config),
                    "elapsed_seconds": elapsed,
                    "candidate_count": len(candidates),
                    "verified_solution_count": len(verified),
                    "tests": per_test_trace,
                }
            ],
        )
