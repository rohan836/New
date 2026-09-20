"""Core typed data structures for ARC tasks and solver traces."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

Grid = tuple[tuple[int, ...], ...]


def freeze_grid(grid: Sequence[Sequence[int]]) -> Grid:
    if not grid or not all(row for row in grid):
        raise ValueError("Grid must contain at least one non-empty row.")
    width = len(grid[0])
    if width == 0 or any(len(row) != width for row in grid):
        raise ValueError("Grid must be rectangular.")
    frozen = tuple(tuple(int(v) for v in row) for row in grid)
    if any(v < 0 or v > 9 for row in frozen for v in row):
        raise ValueError("ARC grid values must be integers in [0, 9].")
    return frozen


def thaw_grid(grid: Grid) -> list[list[int]]:
    return [list(row) for row in grid]


def grid_shape(grid: Grid) -> tuple[int, int]:
    return len(grid), len(grid[0])


@dataclass(frozen=True)
class Example:
    input: Grid
    output: Grid | None = None


@dataclass(frozen=True)
class Task:
    task_id: str
    train: tuple[Example, ...]
    test: tuple[Example, ...]

    @classmethod
    def from_dict(cls, task_id: str, payload: Mapping[str, Any]) -> "Task":
        def parse(split: str) -> tuple[Example, ...]:
            result = []
            for pair in payload.get(split, []):
                result.append(
                    Example(
                        input=freeze_grid(pair["input"]),
                        output=freeze_grid(pair["output"]) if pair.get("output") is not None else None,
                    )
                )
            return tuple(result)

        train = parse("train")
        test = parse("test")
        if not train or not test:
            raise ValueError(f"Task {task_id!r} must contain train and test examples.")
        return cls(task_id=task_id, train=train, test=test)


@dataclass(frozen=True)
class Operation:
    name: str
    params: tuple[Any, ...] = ()

    def label(self) -> str:
        if not self.params:
            return self.name
        return f"{self.name}({', '.join(map(str, self.params))})"


@dataclass(frozen=True)
class Program:
    operations: tuple[Operation, ...] = ()

    def label(self) -> str:
        return " -> ".join(op.label() for op in self.operations) or "identity"


@dataclass(frozen=True)
class Candidate:
    program: Program
    correct: int
    total: int
    complexity: int
    source: str = "search"

    @property
    def exact(self) -> bool:
        return self.correct == self.total and self.total > 0

    @property
    def fit(self) -> float:
        return self.correct / self.total if self.total else 0.0


@dataclass
class SolveResult:
    task_id: str
    candidates: list[Candidate] = field(default_factory=list)
    predictions: list[list[Grid]] = field(default_factory=list)
    traces: list[dict[str, Any]] = field(default_factory=list)

    @property
    def solved_by_verified_program(self) -> bool:
        return any(c.exact for c in self.candidates)
