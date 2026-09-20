# Data and Evaluation

## Dataset contract

A task JSON contains train demonstration input/output pairs and test inputs. During solving, test outputs are treated as unavailable.

ARC grids are rectangular matrices containing integers from 0 to 9.

## Leakage rule

Never load test outputs inside the solver.

A separate scorer may compare generated predictions to labels after the run.

## Evaluation tiers

Keep training, public evaluation, semi-private evaluation, and private evaluation conceptually separate.

Do not repeatedly tune a solver against an evaluation score and then present that score as an untouched evaluation.

## Prediction schema

The solver writes one prediction list per test input. Each list contains at most two distinct candidate grids.

This internal schema is intentionally simple and can later be adapted to an official benchmark submission format.

## Run artifact

Every experiment should record configuration, task set and split, solver commit, per-task predictions, candidate traces, runtime, resource use when relevant, external inference cost when relevant, and separately computed score.
