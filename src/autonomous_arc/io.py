"""Input/output helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .types import Grid, Task, thaw_grid


def load_task(path: str | Path) -> Task:
    path = Path(path)
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return Task.from_dict(path.stem, payload)


def load_task_dir(path: str | Path) -> list[Task]:
    root = Path(path)
    return [load_task(p) for p in sorted(root.glob("*.json"))]


def write_predictions(path: str | Path, task_id: str, predictions: list[Grid]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "task_id": task_id,
        "predictions": [thaw_grid(grid) for grid in predictions],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_trace(path: str | Path, trace: dict[str, Any]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(trace, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_benchmark_results(path: str | Path, rows: list[dict[str, Any]]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n", encoding="utf-8")
