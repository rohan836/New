# Experiment Protocol

A research run is valid only when it is reproducible.

## Before a run

Record the Git commit, dataset version and source, task split, solver configuration, search depth, candidate budget, allowed attempts, model/provider identifiers, hardware, and random seed when applicable.

## During a run

Keep logs, candidate traces, generated outputs, and timing/resource metrics.

## After a run

Report task count, solved tasks, task-level accuracy, verified-program rate, average candidates evaluated, median and p95 solve time, and external inference cost when relevant.

Never turn a single successful task into a benchmark claim.

## Comparisons

When comparing systems, keep the task set and scoring procedure fixed and change one major variable at a time when practical.

Suggested fields:

system | generator | verifier | search budget | model | tasks | accuracy | cost | latency
