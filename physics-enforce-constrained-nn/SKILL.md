---
name: physics-enforce-constrained-nn
description: >-
  Use when training or reviewing a hard-constrained neural surrogate (ENFORCE /
  AdaNP) so outputs satisfy named physics equalities/inequalities -- not for
  inventing locked physical coefficients.
metadata:
  pattern: pipeline
  version: "1.0.1"
---
# ENFORCE hard-constrained neural nets

Train or review a surrogate whose predictions are driven onto a **constraint manifold** via adaptive-depth neural projection (AdaNP), following the [ENFORCE](https://github.com/process-intelligence-research/ENFORCE) pattern (`enforce-nn`, arXiv:2502.06774).

## When

- Outputs must obey nonlinear **equalities** and/or **inequalities** from known physics (conservation, Beer with locked path length, stoichiometric balances, box bounds).
- Soft penalty-only PINNs are not enough; need epsilon-feasibility at inference.
- Supervised fit **or** self-supervised parametric optimisation with constraints.

## When not

- Inventing missing physical coefficients to define c(x,y).
- Replacing an already-linear locked law with a free NN (just enforce the law).
- Need for **global** optimisation over the net -- train with ENFORCE, then embed via [physics-relu-milp-embed](../physics-relu-milp-embed/SKILL.md) or [physics-kan-global-opt](../physics-kan-global-opt/SKILL.md) if required.

## Pipeline

1. **Name constraints** c(x,y)=0, g(x,y)<=0 from locks / first principles; mark every symbol locked vs free.
2. **Affine-in-y** constraints: one NP step can be exactly feasible -- prefer writing physics affine in the predicted outputs when honest.
3. **Inequalities**: Fischer-Burmeister reformulation into equalities on extended [y, lambda] (ENFORCE FB module).
4. **Train**: Adam on task loss + displacement + residual; do **not** wrap forward in no_grad (AdaNP needs autograd through c).
5. **Report**: task error, ||c||, depth used, and whether epsilon was met -- local convergence only for nonlinear c.

## Emit shape

- Constraint list (physics source per row)
- Feasibility metrics (train/test)
- Firewall: which quantities remain analysis-only (do not invent locked coefficients)

## Quality bar

- Constraints cite a lock or equation; no fabricated epsilon, lambda, mL.
- Scaling: constrain in **physical** units or document scaled c carefully.
