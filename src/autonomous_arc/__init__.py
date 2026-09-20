"""Autonomous ARC-AGI solver research package."""

__version__ = "0.1.0"

from .solver import AutonomousSolver, SolverConfig
from .types import Grid, Task, Example, Candidate, SolveResult

__all__ = [
    "AutonomousSolver",
    "SolverConfig",
    "Grid",
    "Task",
    "Example",
    "Candidate",
    "SolveResult",
]
