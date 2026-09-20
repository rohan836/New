"""Verifier for candidate ARC programs."""

from __future__ import annotations

from .program import execute
from .types import Candidate, Program, Task


def verify(task: Task, program: Program, source: str = "search") -> Candidate:
    correct = 0
    for example in task.train:
        if example.output is None:
            continue
        try:
            prediction = execute(program, example.input)
        except (ValueError, IndexError, TypeError):
            continue
        if prediction == example.output:
            correct += 1
    complexity = len(program.operations) + sum(len(str(op.params)) // 32 for op in program.operations)
    return Candidate(
        program=program,
        correct=correct,
        total=len(task.train),
        complexity=complexity,
        source=source,
    )
