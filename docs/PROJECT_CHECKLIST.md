# Autonomous Solver Project Checklist

Use this as the definition of done for the research repository.

## Foundation

- [x] Canonical project identity.
- [x] Autonomous solver package.
- [x] Typed ARC task representation.
- [x] Executable program representation.
- [x] Deterministic primitive library.
- [x] Candidate search.
- [x] Training-set verifier.
- [x] Candidate ranking.
- [x] Per-test prediction budget.
- [x] Separate scorer.
- [x] Run traces.
- [x] Unit tests.
- [x] CI.
- [x] Citation metadata.
- [x] Documentation.

## Search system

- [x] Bounded program composition.
- [x] Exact consistency across demonstrations.
- [x] Simplicity-aware ranking.
- [ ] Object extraction.
- [ ] Relational reasoning between objects.
- [ ] Parameterized transformation synthesis.
- [ ] Search heuristics learned from prior tasks.
- [ ] Adaptive search budget.
- [ ] Diversity-aware candidate selection.

## Model-assisted reasoning

- [x] Provider interface.
- [x] API-independent JSONL proposal path.
- [ ] Learned proposal model.
- [ ] Reasoning-model adapter.
- [ ] Proposal repair loop.
- [ ] Model-based verifier.
- [ ] Candidate critique and revision.
- [ ] Search guided by verifier feedback.

## Evaluation

- [x] Solver does not require test labels.
- [x] Separate scoring stage.
- [x] Reproducibility protocol.
- [ ] ARC-AGI-1 benchmark harness.
- [ ] ARC-AGI-2 benchmark harness.
- [ ] Frozen public-evaluation experiment.
- [ ] Cost and latency accounting.
- [ ] Failure taxonomy.
- [ ] Repeated independent runs where stochastic components exist.

## Research quality

- [x] Explicit hypothesis.
- [x] Experiment protocol.
- [x] Research log template.
- [ ] Baseline comparison table.
- [ ] Ablation suite.
- [ ] Error analysis.
- [ ] Search trace analysis.
- [ ] Program library growth analysis.
- [ ] Publication-quality experiment report.
