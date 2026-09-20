"""Optional proposal interfaces for reasoning models.

The autonomous core does not require a model API. Future learned or reasoning
models can emit executable programs through this interface and use the same verifier.
"""

from __future__ import annotations

from pathlib import Path
import json
from typing import Protocol

from .types import Operation, Program, Task


class ProposalProvider(Protocol):
    def propose(self, task: Task) -> list[Program]:
        ...


class JsonlProposalProvider:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def propose(self, task: Task) -> list[Program]:
        if not self.path.exists():
            return []
        programs: list[Program] = []
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                record = json.loads(line)
                if record.get("task_id") != task.task_id:
                    continue
                operations = []
                for item in record.get("program", []):
                    params = tuple(item.get("params", []))
                    if item["name"] == "recolor" and params:
                        params = (tuple(tuple(pair) for pair in params[0]),)
                    operations.append(Operation(item["name"], params))
                programs.append(Program(tuple(operations)))
        return programs
