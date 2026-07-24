# Core MCDM principles library (token-optimized)

## Core rules

- Decompose decision into clear criteria.
- Assign relative weights to criteria (sum to 1.0 or 100%).
- Score each option against every criterion on a consistent scale (0-10 or 1-5).
- Compute weighted score = sum (criterion_score × weight).
- Rank options by total weighted score.
- Perform sensitivity analysis: how does ranking change if weights shift?

## Common MCDM patterns

- Simple weighted sum
- Pairwise comparison (AHP style) for consistency
- Elimination by aspects for screening
- Trade-off matrix visualization

## Mathematical building blocks

- Weighted score_i = Σ (score_{i,j} × w_j)
- Consistency ratio for pairwise matrices (optional advanced step)

## Retrieval seeds

mcdm, multi criteria, weighted score, decision matrix, tradeoff, ranking, criteria, weight, ahp, pairwise
