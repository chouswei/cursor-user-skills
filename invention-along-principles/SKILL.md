---
name: invention-along-principles
description: >-
  Use when defining, teaching, or running invention as experiment: delete the
  lying part, diverge candidates, remeter with a proof bar, converge
  KEEP/KILL/NARROW/CORRECT/EXTEND. Identity is what is bound. Pair with
  first-principles-work-critique for the cut.
metadata:
  pattern: pipeline
  version: 1.1.0
---
# Invention along principles

**Invention** = producing a new, working thing by **experiment under named principles**, not by brainstorm theater or vibes-as-ship.

Principles are the non-negotiable axes. Experiments are the only proof. Soft-pass is the enemy.

## One line

Diverge many candidates → remeter against a proof bar → converge one lock (KEEP / KILL / NARROW / CORRECT / EXTEND).

**Spline:** a thing is only what a named experiment can still entail after you delete the part that was lying. Delete that part before you optimize anything else. Identity is what is bound, not what is named. Speed is remeter rate.

Pair with [first-principles-work-critique](sand-workflow:first-principles-work-critique) for the convergent cut. This skill owns the **invent loop**; that skill owns the **review verdict**.

## Lineage (web anchors)

Not one branded method — a family that shares **purpose ↔ principle ↔ decisive experiment**. Map onto our principles; do not replace them.

| Anchor | Core idea | Maps to |
| --- | --- | --- |
| [W. Brian Arthur — Logic of Invention](https://santafe.edu/research/results/working-papers/the-logic-of-invention) ([PDF](https://sites.santafe.edu/~wbarthur/Papers/InventionOffprint.pdf)) | Link a *purpose* to a *principle* (harnessable effect); recurse subproblems until real parts exist | Claim first · Constructability |
| [Lee Frank — Nature and Method of Invention](http://www.leefrank.net/PDFs/Nature%20and%20Method%20of%20Invention.pdf) | Full first-principles laws (not textbook shortcuts); one key yes/no experiment that can kill the approach | Proof bar · Soft-pass kill |
| [Edisonian approach](https://en.wikipedia.org/wiki/Edisonian_approach) | Systematic hunt-and-try when theory is missing; failures map what won't work; invent *systems*, not orphan parts; utility/sell is a filter | Remeter · Ship the survivor · One factor |
| [Riskiest Assumption Test (RAT)](https://www.koji.so/docs/riskiest-assumption-test-guide) | Cheapest experiment on the highest-importance / lowest-evidence belief before building | One factor · Proof bar before green |
| PoL / PoC probes (disposable, falsifiable, pass/fail before build) | One hypothesis, narrow scope, criteria locked before code; soft evidence ≠ hard pass | Soft-pass kill · Sufficiency |
| [Paul Graham — Six Principles for Making New Things](https://www.paulgraham.com/newthings.html) | Overlooked problem · informal delivery · crude v1 · iterate | Diverge cheap · Ship the survivor |

**Ours adds (product / agent sharpening):** KEEP / KILL / NARROW / CORRECT / EXTEND as the converge verbs. Priority if two fit: CORRECT > EXTEND > NARROW > KILL > KEEP; **identity honesty** (face ≠ tip, what is bound ≠ what is named); delete the lying part before optimizing; human gate on SSOT; soft-pass checklist that voids invent.

## What counts as invention

| Is invention | Is not |
| --- | --- |
| A candidate that can fail a named meter | A brainstorm with no falsifier |
| A prototype that ships a *weaker true claim* | Oversell of a demo as product |
| A CORRECT that names error + replacement | Renaming failure as "green" |
| A Narrow that shrinks claim to what evidence entails | Killing a minority falsifier to pick "best" |
| An EXTEND that names the missing path the experiment already requires, then remeters | Adding a part that should not exist, or shrinking the claim |
| Measured wall / fidelity / refuse behavior | CI merge, feature count, or tip-as-product |
| Deleting a part that should not exist, then remetering | Polishing a seed, label, or metaphor-as-type |

## Principles (non-negotiable)

1. **Claim first.** State the sold claim in one sentence before the build. Invention without a claim cannot remeter.
2. **Delete before optimize.** Name the part that should not exist. Do not improve, seed, or special-case it. A metaphor may teach; once it is a type, it is fog.
3. **Proof bar before green.** Name meters (what, how, pass/fail) *before* running. No bar → no KEEP.
4. **Sufficiency over story.** Evidence must *entail* the claim (no more, no less). Efficiency never outranks sufficiency or quality. Speed is remeter rate, not story rate.
5. **Constructability.** The path must run for real (live desk, real face, real refuse) — not proxy, cache-as-live, or tip sold as product.
6. **Soft-pass kill.** Forbidden: redefine pass after seeing data; drop the falsifier; score from coaching not fields; sell scaffold/CI as product gold.
7. **Identity honesty.** What you invent *is* what you bind. Wrong identity → CORRECT or KILL, not rebrand.
8. **Human gate where SSOT lives.** Agents propose; humans save/apply when the principle says so. Invention does not sneak-write the source of truth.
9. **One factor when possible.** Change one variable per remeter so the meter attributes cause. Prefer RAT: riskiest unsupported assumption first.
10. **Ship the survivor.** KEEP ships the narrowed true claim. KILL stops spend. NARROW updates the sell pack. CORRECT replaces the wrong artifact and remeters. EXTEND names the missing path the experiment already requires, then remeters — do not add a part that should not exist, and do not shrink the claim.

## Invent loop (operational)

```
1. Name claim + non-claims
2. Delete the part that should not exist
3. Name proof bar (meters + pass/fail)
4. Diverge 2–N candidates (cheap prototypes / apparatus)
5. Remeter each on the same bar
6. Converge: KEEP | KILL | NARROW | CORRECT | EXTEND
7. If CORRECT, NARROW, or EXTEND → update claim / name the path → remeter
8. Only KEEP may be sold / folded into product locks
```

Arthur-shaped check: is the claim a *purpose* linked to a *principle*, and does each remeter resolve a real subproblem toward constructable parts?

RAT-shaped check: is this the riskiest unsupported assumption, tested as cheaply as possible?

## Soft-pass checklist (void invent if any)

- [ ] Pass redefined after numbers landed
- [ ] Proxy / Fake / tip used as product meter
- [ ] STALE / refuse / silent-drop ignored
- [ ] Different desk or different Qs than the locked bar
- [ ] Feature count or merge treated as fidelity
- [ ] Invent bot answered a human-only gate
- [ ] Coaching text scored instead of meter fields
- [ ] Soft evidence (demo polish, CI, compliments) sold as hard pass
- [ ] Metaphor promoted to a product type
- [ ] Work optimized a part that should have been deleted

## Output shape (invent cut)

One short card:

- **Claim** (one sentence)
- **Deleted** (part that should not exist)
- **Bar** (meters)
- **Survivors** (what remetered)
- **Verdict** KEEP | KILL | NARROW | CORRECT | EXTEND
- **Next invent** (one factor) or **stop**; if EXTEND, name the missing path then remeter

## When not

- Pure brainstorm with no intent to remeter → diverge only; do not call it invention
- On-domain physics/math proofs → use real domain necessaries; do not invent product fields from analogy symbols
- Convergent review of someone else's already-claimed green → use first-principles-work-critique alone
