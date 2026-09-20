"""Command-line interface for the autonomous solver."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .io import load_task, load_task_dir, write_benchmark_results, write_predictions, write_trace
from .providers import JsonlProposalProvider
from .scorer import score_prediction_dir
from .solver import AutonomousSolver, SolverConfig


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="arc-solver",
        description="Autonomous ARC-AGI research solver",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    solve = sub.add_parser("solve", help="Solve one ARC task without using test outputs")
    solve.add_argument("task", type=Path)
    solve.add_argument("--output-dir", type=Path, default=Path("runs/manual"))
    solve.add_argument("--max-depth", type=int, default=2)
    solve.add_argument("--candidate-budget", type=int, default=128)
    solve.add_argument("--attempts", type=int, default=2)
    solve.add_argument("--proposal-file", type=Path)

    batch = sub.add_parser("batch", help="Solve every JSON task in a directory")
    batch.add_argument("task_dir", type=Path)
    batch.add_argument("--output-dir", type=Path, default=Path("runs/batch"))
    batch.add_argument("--max-depth", type=int, default=2)
    batch.add_argument("--candidate-budget", type=int, default=128)
    batch.add_argument("--attempts", type=int, default=2)

    score = sub.add_parser("score", help="Score an existing prediction directory against labeled tasks")
    score.add_argument("task_dir", type=Path)
    score.add_argument("prediction_dir", type=Path)
    score.add_argument("--output", type=Path)

    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.command == "score":
        result = score_prediction_dir(args.task_dir, args.prediction_dir)
        print(json.dumps(result, indent=2))
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        return

    config = SolverConfig(
        max_depth=args.max_depth,
        candidate_budget=args.candidate_budget,
        attempts=args.attempts,
    )

    provider = getattr(args, "proposal_file", None)
    solver = AutonomousSolver(
        config=config,
        proposal_provider=JsonlProposalProvider(provider) if provider else None,
    )

    if args.command == "solve":
        task = load_task(args.task)
        result = solver.solve(task)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        write_predictions(args.output_dir / f"{task.task_id}.json", task.task_id, result.predictions)
        write_trace(args.output_dir / f"{task.task_id}.trace.json", result.traces[0])
        print(f"{task.task_id}: {len(result.predictions)} test input(s) processed")
        for candidate in result.candidates[:5]:
            print(
                f"  {candidate.source:6s} fit={candidate.correct}/{candidate.total} "
                f"complexity={candidate.complexity} :: {candidate.program.label()}"
            )
        return

    results = []
    for task in load_task_dir(args.task_dir):
        result = solver.solve(task)
        write_predictions(args.output_dir / f"{task.task_id}.json", task.task_id, result.predictions)
        write_trace(args.output_dir / f"{task.task_id}.trace.json", result.traces[0])
        results.append(
            {
                "task_id": task.task_id,
                "verified_solution_found": result.solved_by_verified_program,
                "prediction_count": [len(x) for x in result.predictions],
            }
        )
    write_benchmark_results(args.output_dir / "summary.json", results)
    print(f"Solved {len(results)} task file(s).")


if __name__ == "__main__":
    main()
