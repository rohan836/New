# Architecture

## Core loop

1. Parse a task into immutable grids.
2. Generate executable candidate programs.
3. Execute each program on every training input.
4. Verify exact agreement with every training output.
5. Rank by training fit, then simplicity.
6. Search or refine within a bounded budget.
7. Apply verified programs independently to each unseen test input.
8. Keep at most two distinct hypotheses for each test input.
9. Record a trace containing configuration, candidates, and runtime.

The candidate generator can later be replaced without changing verification or scoring.

## Research axes

- Symbolic search: deterministic executable transformations.
- Learned proposals: a trained model can propose programs.
- Reasoning-model proposals: an external or open-weight model can emit candidates through a provider adapter.

All candidates enter the same verifier. A proposal is not a solution merely because a model generated it.

## Baseline separation

The existing top-level src Python implementation remains the historical transformer baseline from the starting repository. New autonomous research code lives under src/autonomous_arc/.

## Evaluation isolation

The solver never reads test outputs. Scoring is a separate concern and lives in scorer.py.

ARC-AGI-2 uses public development data plus semi-private and private evaluation tiers. The task format is training demonstrations followed by test inputs, with pixel-perfect outputs required.
