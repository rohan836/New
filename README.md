# ARC-AGI Autonomous Solver

**Rohan bhise**

An autonomous ARC-AGI research project focused on test-time program search, executable candidate transformations, verification, and adaptive reasoning.

## Research idea

Instead of asking one model to directly emit the final grid, the system treats an ARC task as a search problem:

task -> candidate programs -> execution -> verification -> ranking -> refinement -> test-time hypotheses

A candidate only becomes a verified solution when it exactly reproduces every training output.

The design is intentionally modular so symbolic search, learned proposal models, and reasoning-model proposals can enter the same verification loop.

## Current implementation

The repository currently contains a working first-stage autonomous core:

- Immutable ARC task and grid types.
- Executable transformation primitives.
- Bounded composition search.
- Task-level color-mapping induction.
- Exact training-example verification.
- Simplicity-aware candidate ranking.
- Up to two distinct predictions for each test input.
- Separate prediction generation and scoring.
- JSONL proposal interface for future reasoning-model integration.
- Reproducible run traces.
- Unit tests and a smoke task.

This is a research foundation, not a claim of state-of-the-art performance.

## Repository layout

- src/autonomous_arc/ : autonomous solver core.
- scripts/ : command-line entry points.
- configs/ : experiment configuration.
- tests/ : automated tests.
- docs/ : architecture, evaluation discipline, and experiment protocol.
- examples/ : tiny local smoke tasks.
- experiments/ : research notes and analysis space.
- submissions/ : benchmark artifact space.
- baselines/ : explanation of the retained transformer baseline.
- src/*.py and dataset_building_scripts/ : historical transformer baseline retained for reproducibility.

## Quick start

Install the package in editable mode:

    python -m pip install -e .

Run the bundled smoke task:

    python scripts/solve.py solve examples/smoke_task.json --output-dir runs/smoke

The run writes:

- one prediction file per task,
- a solver trace,
- the searched candidate programs.

Run the test suite:

    python -m pytest -q

Show the CLI:

    python -m autonomous_arc.cli --help

## Batch solving

    python scripts/solve.py batch PATH_TO_TASK_DIRECTORY --output-dir runs/batch

The solver only consumes training outputs and test inputs. Test outputs are not part of the solve path.

## Scoring

Scoring is intentionally separate from solving.

    python scripts/solve.py score PATH_TO_LABELED_TASKS runs/batch

This lets the same solver remain usable on datasets where test labels are unavailable.

## Reasoning-model integration

The project has a provider interface for proposal generation. A future model can propose an executable program, but the verifier remains authoritative.

A JSONL proposal record has the form:

    {"task_id":"example_id","program":[{"name":"rot90"}]}

This keeps external model APIs out of the solver core and makes model-generated ideas directly comparable with symbolic search.

## Research discipline

Every serious run should record:

- Git commit.
- Dataset and split.
- Search depth and candidate budget.
- Number of allowed attempts.
- Model or provider identifier, when applicable.
- Hardware.
- Runtime and cost, when applicable.
- Per-task traces.
- Separately computed score.

Never report a benchmark number without the exact task set, solver commit, configuration, and scoring procedure.

## Benchmark context

ARC-AGI is a program-synthesis and abstract-reasoning benchmark based on small colored grids. ARC-AGI-2 uses training demonstrations followed by novel test inputs and a pixel-perfect success criterion. The official benchmark also separates public development data from stronger private evaluation tiers.

Official references:

- ARC-AGI-2: https://github.com/arcprize/ARC-AGI-2
- ARC-AGI guide: https://arcprize.org/guide/1
- ARC Prize benchmarking: https://github.com/arcprize/arc-agi-benchmarking

## Project status

### Implemented

- Autonomous task representation.
- Executable program representation.
- Bounded search.
- Training-set verifier.
- Test-time hypothesis generation.
- Separate scorer.
- Provider interface.
- Run traces.
- Tests and smoke task.

### Next research layers

- Rich object-centric primitives.
- Better program representations.
- Learned candidate proposal models.
- Reasoning-model proposal integration.
- Adaptive search budgets.
- Candidate diversity and disagreement analysis.
- Verifier models trained on correct versus incorrect programs.
- Search policies learned from prior tasks.
- Large-scale ARC-AGI-1 and ARC-AGI-2 experiments with frozen evaluation protocols.
