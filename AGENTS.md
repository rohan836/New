# AGENTS.md

## Project
Autonomous ARC-AGI research system.

## Mission
Build an autonomous solver that infers task-specific programs from ARC demonstrations, tests them against every demonstration, searches and refines candidates, and produces reproducible test-time hypotheses.

## Rules
1. Never use test outputs while solving.
2. Never claim an experiment was run unless its result is recorded.
3. Keep solver logic independent from benchmark scoring.
4. Every candidate must be executable and verifiable.
5. Prefer deterministic, inspectable mechanisms before adding model-generated components.
6. Record configuration, seed, candidate budget, and runtime for every experiment.
7. Keep the legacy transformer as a clearly identified baseline.
8. Do not commit credentials, API keys, or generated run artifacts.

## Layout
- src/autonomous_arc/: autonomous solver core.
- scripts/: user-facing entry points.
- configs/: experiment configuration.
- tests/: unit and integration tests.
- docs/: architecture, evaluation, and research protocols.
- Existing top-level src Python files and dataset_building_scripts/ are the legacy baseline.

## Validation
python -m pytest -q
python -m autonomous_arc.cli --help
python scripts/solve.py solve examples/smoke_task.json --output-dir runs/smoke
