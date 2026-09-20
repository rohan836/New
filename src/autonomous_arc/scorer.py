"""Separate scoring utility. Never imported by the solver."""

from __future__ import annotations

from pathlib import Path
import json

from .io import load_task
from .types import freeze_grid


def score_prediction_dir(task_dir: str | Path, prediction_dir: str | Path) -> dict:
    task_root = Path(task_dir)
    prediction_root = Path(prediction_dir)
    task_count = 0
    solved_tasks = 0
    solved_test_pairs = 0
    total_test_pairs = 0

    for task_path in sorted(task_root.glob("*.json")):
        task = load_task(task_path)
        prediction_path = prediction_root / f"{task.task_id}.json"
        if not prediction_path.exists():
            continue
        payload = json.loads(prediction_path.read_text(encoding="utf-8"))
        predictions = payload.get("predictions", [])
        task_count += 1
        task_solved = True

        for index, example in enumerate(task.test):
            total_test_pairs += 1
            candidate_outputs = predictions[index] if index < len(predictions) else []
            gold = example.output
            if gold is None:
                task_solved = False
                continue
            matches = any(freeze_grid(candidate) == gold for candidate in candidate_outputs)
            if matches:
                solved_test_pairs += 1
            else:
                task_solved = False

        if task_solved:
            solved_tasks += 1

    return {
        "tasks_evaluated": task_count,
        "tasks_solved": solved_tasks,
        "task_accuracy": solved_tasks / task_count if task_count else 0.0,
        "test_pairs_solved": solved_test_pairs,
        "test_pairs_total": total_test_pairs,
        "test_pair_accuracy": solved_test_pairs / total_test_pairs if total_test_pairs else 0.0,
    }
