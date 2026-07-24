# Core principles: scientific method + first-principles (system engineering)

Skill id: **scientific-method-first-principles**.

## Role

- Full scientific method in engineering: question -> background -> falsifiable hypothesis -> smallest decisive experiment -> analysis -> conclusion -> iteration/replication.
- **Empirical** = observations: tests, benchmarks, telemetry, logs, lab/A-B data, incidents.
- **First-principles** = bedrock not tied to one vendor/habit: conservation, throughput/safety/information bounds, proven causal chains, marginal costs - checked at analysis/conclusion.
- **Fusion** = one model where data constrains possibility and theory explains why.

## Rules

- Separate measured vs assumed vs physics/math-guaranteed.
- Tag bedrock claims **E** (empirical), **T** (theoretical), **O** (organizational).
- No invented numbers, outcomes, or log lines; placeholders + what experiment fills gaps.
- If E vs T conflicts: name failure mode (measurement, model, hidden boundary) before choosing direction.
- Prefer smallest falsifiable test when uncertainty blocks a decision.
- System hooks: SLOs, error budgets, latency/throughput, power/thermal, reliability, interfaces, topology.

## Workflow (conceptual)

- **Question:** decision, unknown, or claim under test.
- **Background:** evidence artifacts + prior art (what ran, on what, confidence).
- **Hypothesis:** deconstruct "we always did" into testable claims; list non-negotiable invariants.
- **Test:** smallest decisive experiment; predictions that falsify.
- **Analyze/conclude:** E/T/O interpretation; design that fits evidence + invariants; residual risk.
- **Iterate:** next experiment or what evidence would revise; replicate when stakes demand.

## Pairing

- Two valid evidence-backed pulls (speed vs reliability, cost vs coverage) -> **empirical-paradox-synthesis**.
- Weighted option ranking under criteria -> **mcdm-decider** (this skill stays broader than pure scoring).

## Retrieval seeds

scientific method, hypothesis, falsify, prediction, replicate, iterate, background, prior art, empirical, first principles, measurement, telemetry, benchmark, test results, lab data, experiment, observed, evidence, metrics, logs, trace, SLO, latency, throughput, thermal, power, reliability, invariant, bedrock, deconstruct, system engineering, design decision, validation, contradiction, theory vs data
