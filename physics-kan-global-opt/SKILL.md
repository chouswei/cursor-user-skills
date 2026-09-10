---
name: physics-kan-global-opt
description: >-
  Use when running deterministic global optimisation over a trained KAN (MINLP /
  optimization-over-KANs) as an optional alternative to ReLU MILP embeds -- not
  for inventing locked physical coefficients.
metadata:
  pattern: pipeline
  version: "1.0.1"
---
# Global optimisation over trained KANs

Optional path: deterministic global optimisation over a **trained Kolmogorov-Arnold Network** via MINLP (Pyomo formulation in [optimization-over-KANs](https://github.com/process-intelligence-research/optimization-over-KANs), arXiv:2503.02807). Use when KAN surrogates are chosen over ReLU MLPs.

## When

- Surrogate is a trained KAN (JSON weights as in the repo).
- Need global opt / bounds comparable to ReLU+MILP baselines (repo also shows MLP+OMLT).
- Piecewise / spline-like univariate structure of KAN matches the formulation options file.

## When not

- Default ReLU stack already suffices -- prefer [physics-relu-milp-embed](../physics-relu-milp-embed/SKILL.md) (usually simpler MILP).
- Hard physics equalities at **train** time -- ENFORCE first ([physics-enforce-constrained-nn](../physics-enforce-constrained-nn/SKILL.md)), optimise later if needed.
- No solver budget for MINLP.

## Pipeline

1. Train KAN; export JSON; set **input bounds** in the formulation helper (required).
2. Choose KAN_formulation_options.json per paper; pick solver (e.g. SCIP).
3. Run opt_kan (or equivalent); optionally run MLP+OMLT baseline for comparison.
4. Report primal/dual bounds, time, and forward-check of the KAN at the reported point.
5. Attach outer physics locks as explicit constraints when the KAN only approximates a residual map.

## Emit shape

- Why KAN vs ReLU for this map
- Opt status + bound gap
- Firewall: optimum is not a licence to invent locked assay or physical coefficients

## Quality bar

- Bounds honest; no silent scaler mismatch.
- Cite formulation options actually used.
