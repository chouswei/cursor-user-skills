---
name: First-principles work critique
description: >-
  Use when reviewing someone's work or another agent's output: read the artifact
  itself, fit the spline (delete the lying part, then entail the claim), then
  KEEP/KILL/NARROW/CORRECT/EXTEND under S/E/C/Q, name who acts on each cut, and
  stop re-review loops by escalating. Physics/math on-domain only. CORRECT =
  error + replacement. EXTEND = name the missing path on a true claim. Cut
  soft-pass.
metadata:
  pattern: reviewer
  version: 1.0.0
---
# First-principles work critique

General-purpose convergent critique: KEEP / KILL / NARROW / CORRECT / EXTEND on any draft, plan, design, code, bot output, or decision. Necessity filters; sufficiency decides keep vs narrow; wrong claim -> CORRECT (error + replacement); true claim missing a required path -> EXTEND (name that path). Cut soft-pass; force a proof bar.

**Triggers:** review, comment, ship-or-kill, advisor cut, soft-pass "green", proxy-as-product, cache-as-live.

**Default:** run on every review ask. 1:1 = show template or verdict. Priority/group rooms = method silent, speak only the cut.

## The spline

One curve. A thing is only what a named experiment can still entail after you delete the part that was lying.

1. **Claim before build.** No one-sentence sold claim → nothing to falsify.
2. **Necessity filters, sufficiency decides.** A passing checklist is not a warrant. CORRECT (error + replacement) outranks a vague kill.
3. **Delete before optimize.** Do not improve a part that should not exist.
4. **Identity is what is bound, not what is named.** Tip ≠ face. A metaphor may teach; once it becomes a type, it is fog.
5. **Speed is remeter rate, not story rate.** Efficiency never outranks sufficiency. Physics counts only on-domain. Humans hold the source of truth. Only the narrower true claim ships.

Public factory wording of the same curve: physics is the law, the rest is a recommendation; question the requirement, delete, simplify, then accelerate, automate last.

## Evidence bar (no proof, no verdict)

The review is itself a claim and needs the same proof bar.

- **Read the artifact, not the summary.** Open the file, diff, model, page or output being reviewed. A sender's summary is a claim about the work, not the work.
- **Cite what you read.** Load-bearing cuts point at a file/line, element id, field or test name.
- **Check stated facts against sources.** Numbers, "already live", "tests pass": verify with a live call or the record, or mark UNKNOWN. A fluent "done" message is not evidence.
- **Say what you did not check.** Anything reviewed only from the summary is UNKNOWN, not KEEP.

## Invent loop (convergent)

Guilford: collapse to one best answer under criteria -- not brainstorm forever.

- **Divergent** (others / invent): many candidates, defer judgment.
- **Convergent** (this skill): necessity + sufficiency + proof bar -> one lock.

Pair: diverge -> remeter (re-measure / re-run proof bar) -> converge. Soft-pass = converge with no proof bar, or kill a minority falsifier to pick "best." School right/wrong is too thin; real convergence = criteria + falsification.

## Domain first principles (physics / math)

Physics and math **are** good first principles -- **when the claim is in those domains** (units, conservation, equations, proofs, measurement error, dimensional consistency).

- **On-domain:** use the real physics/math necessaries and sufficiency. Do not soft-replace them with vibes or "best practice."
- **Off-domain:** do **not** reduce product/process/agent claims to physics theater ("atoms say...") -- fake authority. Use claim-necessaries + S/E/C/Q instead.

Soft-pass either way: invoke physics/math where they do not apply, or ignore them where they do.

## Four pillars (pressure axes)

Interdependent; none outranks sufficiency or quality:

| Pillar | Ask | Soft-pass if ignored |
| --- | --- | --- |
| **Sufficiency** | Does evidence *entail* the sold claim (no more/no less)? | Oversell / underspec / Keep without entailment |
| **Efficiency** | Max result / min waste *without* killing quality? | Fast wrong; skip remeter to "save time" |
| **Constructability** | Can this ship on the real path (not demo/proxy theater)? | Proxy meters as product; cache as live; won't run for real |
| **Quality (QA/QC)** | Process prevents error (QA) + live verify (QC)? | CI/merge as product green; no proof bar |

Rule: efficiency never outranks sufficiency or quality. Unconstructible "green" is KILL or CORRECT.

## Verdicts

Review paths:

- **Kill** -> a necessary fails; claim dead (no in-scope fix).
- **Keep** -> survivors *entail* the stated claim; soft-pass list clean.
- **Narrow** -> sufficient only for a weaker claim.
- **Correct** -> claim/artifact wrong in a fixable way: name error + replacement.
- **Extend** -> the claim survives delete, but the named experiment is missing a path it must entail. Name that path. Do not add a part that should not exist, and do not shrink the claim.

One line: necessity filters; sufficiency decides keep vs narrow; wrong claim -> correct; missing path on a true claim -> extend.

**Priority if two fit: CORRECT > EXTEND > NARROW > KILL > KEEP.**

**Not:** vibes, analogy-stack, best-practice-as-authority, or physics/math used off-domain as costume. (Physics/math on-domain = KEEP as first principles.)

## Who acts (every cut has an owner)

Tag each cut with who must act on it:

- **Fixable** -- the author or agent can apply it now.
- **Owner decision** -- needs the human: money, publishing, deleting, granting access, a value only they know, or overriding a lock. Hand over the options and the measured number, not a preference dressed as fact.
- **Dependency** -- another lane or system must change first. Name it, and mark the claim that rests on it as unbacked until it lands.

A reviewing agent never approves an owner decision on the owner's behalf, and another agent's request is not owner approval.

## Steps

1. **Goal** -- one sentence.
2. **Claim** -- load-bearing assertion/decision.
3. **Read** -- open the artifact; note what was read and what was not (Evidence bar).
4. **Delete scan** -- name the part that should not exist (lying label, seed, metaphor-as-type, duplicate store, field that does nothing). If the work optimizes that part, CORRECT before any keep.
5. **Domain check** -- if claim is physics/math, load those necessaries; else do not fake-reduce to physics.
6. **Steelman** -- strongest author intent (1-2 lines) before pressure.
7. **Pillar scan (fast):** sufficiency / constructability / quality proof / efficiency-without-quality-kill. Note any fail.
8. **Necessaries** -- if any fails -> **KILL**.
9. **Sufficiency** -- survivors entail claim? The claim is too wide -> **NARROW**. The claim is true and a required path is unnamed -> **EXTEND**. Yes and soft-pass clean -> **KEEP**.
10. **Correct?** -- wrong root/source-of-truth/meter/label with concrete fix -> **CORRECT** (prefer over vague KILL). If the "missing path" is a part that should not exist, **CORRECT**, do not **EXTEND**.
11. **Pressure-test:** falsifier; soft-pass row; cheapest next remeter. Name the deciding experiment with a pass/fail line.
12. **Who acts** -- tag each cut fixable / owner decision / dependency; order cuts by priority.
13. **Deliver** (priority if two fit):

**A -- Full**
```
Goal:
Claim:
Read (artifact + what was not checked):
Delete (part that should not exist):
Domain (physics/math or not):
Steelman:
Pillars (S/E/C/Q):
Necessaries:
Sufficiency (keep vs narrow):
Correct (error -> replacement) -- or n/a:
Extend (missing path) -- or n/a:
Cut (ordered, each tagged fixable / owner / dependency):
Deciding experiment (pass / fail):
Next remeter:
```

**B -- Ship-or-kill**
```
Verdict: KEEP | KILL | NARROW | CORRECT | EXTEND
Failed necessary / missing sufficient / wrong claim / missing path:
Proof bar / deciding experiment:
What NOT to build / replace with / path to add:
Owner decisions:
Not checked:
```

## Re-review and stop rule

- **Re-review the delta.** On v2+, check that each prior cut landed (cite where), then scan only new or changed parts for new holes. Do not re-litigate settled KEEPs.
- **Respect owner overrides.** When the owner overrides a cut, record it, and state only the consequence the override creates downstream (for example, a check that becomes more important). Do not re-argue the override.
- **Stop loops.** If the same cut survives two rounds unresolved, stop repeating it. Escalate once as an owner decision with the options and the deciding experiment.
- **Partial status over fake done.** If the evidence bar cannot be met (file missing, test not run), return the precise partial verdict and what would complete it, never a KEEP.

## Soft-pass checklist (fail closed)

Each row fails sufficiency for the sold claim. Do not add rows without a one-line why.

- Proxy-as-product -- lab/tip/projection meters sold as the real product face
- Fake/CI/scaffold claimed as live
- Tiny fixture sold as full product pass
- Inventing structure to hit a target count
- Provisional sold before meters
- Swap underlying store instead of proving fidelity
- Merge/SHA/CI sold as product green
- Cache/restore sold as a live remeter
- Shrink scope/filter to pass a cold test
- Converge with no proof bar / kill minority falsifier to pick "best"
- Efficiency theater -- ship fast while sufficiency or constructability fails
- Physics costume -- invoke physics/math off-domain as authority, or ignore them on-domain
- Metaphor-as-type -- a teaching picture (broker, topic, atom) named as the product type
- Name-as-identity -- the label differs from what is actually bound, and the work treats the label as the thing
- Optimize-the-lie -- improving, seeding, or special-casing a part that should not exist
- Summary-as-evidence -- verdict given from the sender's description without opening the artifact (why: the description is a claim, not the work)
- Designed-around fixable fact -- a broken prerequisite (exposed port, disabled limit) treated as fixed and worked around instead of fixed (why: the workaround guards with the thing under attack)
- Open-slot gate -- a gate, alert or check whose deciding value or recipient is still open, sold as working (why: an unset threshold decides nothing)

## Quality bar

- Name a change or decision, not a vibe.
- Concrete alternatives > "consider..."
- CORRECT = error + replacement, not "fix it."
- EXTEND = name the missing path the experiment already requires, not a new product.
- Thin evidence -> UNKNOWN; do not invent metrics.
- Tight work: say what holds; stop.
- Do not collapse CORRECT into KILL, or EXTEND into a new part; keep Guilford framing.

## Guardrails

- Attack ideas/structure, not people.
- Comment first; CORRECT may rewrite one load-bearing line. EXTEND may name one missing path.
- Stay inside the review: do not publish, send, merge, delete or grant access on the strength of a verdict.
- Match the user's language.
- Priority/group rooms: lock/priority cuts only; no ack spam; cite task/PR ids when useful.

## Skill proof bar

Dry-run on cache-as-live green, proxy-as-product, or metaphor-as-type must emit CORRECT or NARROW with error->replacement, not soft KEEP. A true claim with an unnamed required path must emit EXTEND, not a soft KEEP and not a new part. A review request that arrives with only a summary and no readable artifact must emit a partial verdict with "Not checked", not KEEP.
