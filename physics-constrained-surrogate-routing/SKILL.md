---
name: physics-constrained-surrogate-routing
description: >-
  Use first when choosing among hard-constrained NN (ENFORCE), ReLU-ANN->MILP
  embed, or KAN global opt for physics-consistent surrogates -- not for inventing
  locked physical coefficients.
metadata:
  pattern: pipeline
  version: "1.0.1"
---
# Physics constrained-surrogate routing

Use when a physics or process model needs a **learned surrogate that stays consistent with known constraints**, or when that surrogate must be **embedded in a mathematical program**. Prefer hard physics locks (equations, bounds) over fitting numbers the user forbade inventing.

## Route

| Ask | Skill |
|-----|--------|
| Train / evaluate an NN whose outputs must satisfy equality/inequality physics constraints (projection at inference) | [physics-enforce-constrained-nn](sand-workflow:physics-enforce-constrained-nn) |
| Embed a **trained ReLU MLP** into MILP (Pyomo / Gurobi) for global opt / verification | [physics-relu-milp-embed](sand-workflow:physics-relu-milp-embed) |
| Deterministic global opt over a **trained KAN** (MINLP) or compare to ReLU+OMLT | [physics-kan-global-opt](sand-workflow:physics-kan-global-opt) |
| Propose Lagrangian / Hamiltonian framing before any surrogate | [analytical-mechanics-propose](sand-workflow:analytical-mechanics-propose) |

## Defaults

- Constraints and locks come from **named physics** (e.g. Beer \(A=\varepsilon c \ell\) with locked \(\ell\)). Never invent assay coefficients, wavelengths, or volumes to make a fit look good.
- Surrogates approximate **unknown maps** (sensor response, residual kinetics) inside a feasible set -- they do not replace Beer's law or conservation as soft losses only when a hard constraint is available.
- Upstream refs (learn; cite when using): [ENFORCE](https://github.com/process-intelligence-research/ENFORCE), [ReLU_ANN_MILP](https://github.com/process-intelligence-research/ReLU_ANN_MILP) / reluMIP, [optimization-over-KANs](https://github.com/process-intelligence-research/optimization-over-KANs).

## Do not

- Use these skills to invent locked physical coefficients, assay numbers, or volumes.
- Claim global optimality from a local Adam train without a MILP/MINLP embed step.
