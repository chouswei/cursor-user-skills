---
name: physics-relu-milp-embed
description: >-
  Use when embedding a trained ReLU MLP into MILP (Pyomo/Gurobi, reluMIP
  pattern) for global optimisation or verification of a physics surrogate -- not
  for inventing locked physical coefficients.
metadata:
  pattern: pipeline
  version: "1.0.1"
---
# ReLU ANN -> MILP embed

Embed a **trained ReLU MLP** as a mixed-integer linear program so optimisation / verification can run over the network with MIP solvers (Pyomo or Gurobi), following [ReLU_ANN_MILP](https://github.com/process-intelligence-research/ReLU_ANN_MILP) / `reluMIP` (Grimstad & Andersson; Schweidtmann lineage).

## When

- Surrogate is already trained (prefer TensorFlow sequential ReLU as in the package).
- Need **global** opt, worst-case bounds, or feasibility over the NN response inside input bounds.
- Process / physics outer problem is MILP/MIP-compatible once the net is big-M / indicator encoded.

## When not

- Net still being trained for constraint satisfaction only -- prefer [physics-enforce-constrained-nn](sand-workflow:physics-enforce-constrained-nn) first.
- Smooth activations (tanh/sigmoid) -- use NLP embedding (e.g. MeLOn) or retrain ReLU; do not fake ReLU MILP.
- Inventing labels or targets to force a convenient optimum.

## Pipeline

1. **Freeze** trained weights; record input bounds and scalers (optimisation is in scaled space unless unscaled explicitly).
2. **Encode** each ReLU with binary / big-M (package: Pyomo or Gurobi interface).
3. **Couple** MIP vars to outer physics constraints (locked \(\ell\), balances) -- physics stays outside the net when exact.
4. **Solve** with Gurobi (preferred) or Pyomo+glpk; report gap, bound, and whether the optimum is on a ReLU kink.
5. **Verify** optimum by forward pass of the original net; flag scaler mistakes.

## Emit shape

- Net architecture + bound box
- Solver status / gap
- Physics constraints added outside the embed
- Explicit: the optimum alone does not invent locked physical coefficients

## Related

- OMLT big-M path appears in the KAN repo's MLP baseline -- acceptable sibling tooling when documented.
- Soft alternative for KANs: [physics-kan-global-opt](sand-workflow:physics-kan-global-opt).
