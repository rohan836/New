"""Command-line interface for the autonomous solver."""

from __future__ import annotations

import argparse
from pathlib import Path

from .io import load_task, load_task_dir, write_benchmark_results, write_predictions, write_trace
from .providers import JsonlProposalProvider
from .solver import AutonomousSolver, SolverConfig


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="arc-solver", description="Autonomous ARC-AGI research solver")
    sub = parser.add_subparsers(dest="command", required=True)

    solve = sub.add_parser("solve", help="Solve one ARC task without using test outputs")
    solve.add_argument("task", type=Path)
    solve.add_argument("--output-dir", type=Path, default=Path("runs/manual"))
    solve.add_argument("--max-depth", type=int, default=2)
    solve.add_argument("--beam-size", type=int, default=128)
    solve.add_argument("--attempts", type=int, default=2)
    solve.add_argument("--proposal-file", type=Path)

    batch = sub.add_parser("batch", help="Solve every JSON task in a directory")
    batch.add_argument("task_dir", type=Path)
    batch.add_argument("--output-dir", type=Path, default=Path("runs/batch"))
    batch.add_argument("--max-depth", type=int, default=2)
    batch.add_argument("--beam-size", type=int, default=128)
    batch.add_argument("--attempts", type=int, default=2)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    config = SolverConfig(
        max_depth=args.max_depth,
        beam_size=args.beam_size,
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
        print(f"{task.task_id}: {len(result.predictions)} prediction(s)")
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
                "prediction_count": len(result.predictions),
            }
        )
    write_benchmark_results(args.output_dir / "summary.json", results)
    print(f"Solved {len(results)} task file(s).")


if __name__ == "__main__":
    main()
