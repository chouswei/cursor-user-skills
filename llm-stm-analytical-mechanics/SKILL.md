---
name: llm-stm-analytical-mechanics
description: >-
  Applies LLM short-term-memory analytical-mechanics locks as an ordered
  turn loop (cue/control u, proposal, admission, integrate, eviction,
  Commit) when wiring or triaging ShapeWalk/pin_map working set W versus
  inventory S. Use for STM harness, W vs S, ShapeWalk/pin_map control
  surfaces, gauge/identity, caps, or triage from the STM thesis. Triggers:
  analytic mechanics STM, LLM STM, working set W, ShapeWalk harness,
  STM debug from thesis. Skip: MemNet install/wire grammar
  (mcp-memnet, memnet-format); CompanyMemory desk mapping except as a pointer.
metadata:
  pattern: pipeline
  version: "1.0"
  domain: memnet
pipeline_steps:
  1. Classify -- wire harness, debug triage, or CompanyMemory pointer only.
  2. L3 -- fetch the matching thesis playbook; do not paste the thesis.
  3. Turn loop -- cue/control u -> proposal -> admission -> integrate -> eviction -> optional Commit.
  4. Surfaces -- log proposal / admission / eviction separately (W is not S).
  5. Firewalls -- honesty-c shaped read; no rag_query; no analysis fields on pin_map.
  6. Pair -- execute product tools via mcp-memnet; wire via memnet-format.
system_instruction: |
  Analysis-only STM harness from thesis locks. Not a MemNet SemVer claim.
  Pack metadata.version is this skill only. MemNet 1.0 unclaimed. British English. ASCII.
token_guardrails: |
  - L2 = this checklist. L3 = GitHub thesis/playbooks. MUST NOT paste thesis math or playbook body.
  - MUST NOT duplicate mcp-memnet install or memnet-format GQL grammar.
  - MUST NOT put momentum / coverage / lambda / m on pin_map.
  - MUST NOT emit hid / _memnet_hid / elementId / nickname id on shaped read. Cue-by-nickname lookup is OK.
---

# LLM STM analytical mechanics (turn loop)

**Analysis only.** Doctrine SSOT: [llm-stm-mechanics](https://github.com/chouswei/llm-stm-mechanics) (`thesis/analytical-mechanics-of-llm-stm.md` plus playbooks). This skill is the **operational checklist** (L2). L3 URLs: [references/l3-sources.md](references/l3-sources.md).

**Not a MemNet SemVer claim.** Pack `metadata.version` is this skill folder only. Do **not** claim MemNet **1.0** or a 1.0 product cut. Honesty `c` / wire leaks are **symptoms**, not version cuts.

**Pair (do not duplicate):** how-to-use [memnet-use](../memnet-use/SKILL.md); tools [mcp-memnet](../mcp-memnet/SKILL.md); GQL wire [memnet-format](../memnet-format/SKILL.md). Thin playbook **pointer** (which file to open): [memnet-stm-harness](../memnet-stm-harness/SKILL.md).

One-sentence model (thesis lock): STM is a **controlled trajectory** of working set **W**, not a dump of inventory **S**. The LLM **integrates** admitted W. Steering chooses controls.

## When to load

| Job | This skill | Then open (L3) |
|-----|------------|----------------|
| Wire an agent that uses session memory (cue, `pin_map`, admission, Commit) | Turn loop below | Playbook 1 (harness) |
| Task failed; need triage | Debug tree below | Playbook 2 (after Playbook 1 if harness unknown) |
| Investor CompanyMemory desk mapping only | Pointer; stop | Playbook 3 -- MemNet owns the session; Neo4j owns the disk. Skip unless that desk is in scope. |

## Turn loop (native update)

Per turn `t`:

1. **Cue -> control** -- map product cue `q` (codebook tokens) to analysis control **u** once at the boundary. User input is experimenter **u**, not the integrator and not dump-S by default.
2. **Proposal** -- offer Shape `X-tilde` (e.g. MemNet `pin_map`, bounded `k`, hard LIMIT `M`). If emit signals **truncation** or rows were capped, the extract is **incomplete** -- MUST NOT paint a complete census; re-cue / filter-out or raise compose `M` / uncap and re-pin. Caps stay hard.
3. **Admission** -- caller builds actual `W` from offer + instructions + dialogue + tools. `X-tilde` is a subset of `W` only if the **whole** Shape is admitted.
4. **Integrate** -- LLM generates under `W` (drift at `T=0`; path measure at `T>0` -- fix `T` or average seeds).
5. **Eviction** -- window / KV policy removes mass from `W` (discrete force on the hard window). Continuous `R` is the forgetting **account**, not a second discrete channel.
6. **Commit (optional)** -- gated `mutate` changes inventory `S`; impulse, not a third retrieval verb. Product write stays [mcp-memnet](../mcp-memnet/SKILL.md) / [memnet-format](../memnet-format/SKILL.md). leftover `add` / `update` / `id:'NEW'` / leftover `--anchor` are leftover.

**W is not S.** Empty cue outline = census under hard LIMIT, not a neighbourhood dump of edges. Handoff = **session id**; peer re-pins. Do not ship a dump of S.

## Three control surfaces (inspectability)

Always log separately:

1. **Proposal** -- what was offered (`X-tilde`, order preserved), including truncation / caps / rejects.
2. **Admission** -- what entered `W` and in what order.
3. **Eviction** -- what left `W`.

A global ranker may **only propose**. Collapsing the three into one opaque score fails inspectability.

User input **u** (may stack): (1) cue / control `u`; (2) admitted mass in `W`; (3) discrete impulse `F+/-`. Not automatic inventory. "The user said X" is not merge-by-name.

## Gauge / identity (honesty `c` shaped read)

- Identity is the **graph element**. Nickname `id` is nickname only.
- Cue-by-nickname / locators as **properties** is OK. Shaped **read** MUST NOT show `hid` / `_memnet_hid` / `elementId` / nickname `id`.
- Admission **order is physical** -- do not sort by hid to "clean" tests.
- Metric on `W`: ordered **observable** identities. No hid in ranking features or the metric.

## Caps

Hard reject in the engine. `lambda-hat_M` (shadow price) is an **account diagnostic**, not a buyable knob. Task fails + biting cap -> Shape pressing the cap. Task fails + slack -> wrong cue / wrong Shape, not "buy more `M`". Softening hard caps inside Recall is not a debug fix.

## Debug tree (first FAIL wins)

Force the split **before** tweaking `M` / window / rankers.

| Surface | Question |
|---------|----------|
| **Proposal** | Was gold in the offer? Split **proposal miss** vs **truncated offer** (`max_rows` cut load-bearing kinds). |
| **Admission** | Gold in the offer but missing from `W`? |
| **Eviction** | Gold entered `W` then left? |
| **Integrate** | `W` held gold; generate still wrong (`T`, seed, model)? |
| **Commit** | Unexpected `Delta` on `S` (impulse), not a retrieval miss? |

Cue / experimenter `u` sits **before** proposal. Wrong codebook tokens look like proposal failure until you check harness user-input placement.

Then: logs exist? gauge leak? cap biting vs slack? cue wrong? admission vs offer? eviction (do not invent stickiness on the wire)? `T` / Markov hidden history? Commit impulse? score circularity?

## MUST NOT

- `rag_query` / dump-S as STM API.
- Put momentum / coverage / lambda / `m` / stickiness on `pin_map`.
- Teach leftover `--anchor` / `id:'NEW'` / `add`/`update` as TARGET.
- Claim MemNet **1.0** or treat honesty `c` as a SemVer a/b cut.
- Duplicate playbook or thesis body in this pack.
- Soften hard caps inside the engine; paint a complete census under truncation.
- Collapse proposal / admission / eviction; merge nodes by nickname.

## Pairing

| Need | Skill |
|------|--------|
| Goldfish loop / how to use | [memnet-use](../memnet-use/SKILL.md) |
| MCP tools / `pin_map` / `mutate` | [mcp-memnet](../mcp-memnet/SKILL.md) |
| GQL / shaped emit grammar | [memnet-format](../memnet-format/SKILL.md) |
| Which GitHub playbook file | [memnet-stm-harness](../memnet-stm-harness/SKILL.md) |
| Shared workers | [memnet-multitask](../memnet-multitask/SKILL.md) -- hand off **session id** + locators; peer re-pins |

## Steps

1. Classify the job (wire / debug / Investor desk pointer).
2. Follow this checklist. Fetch L3 only as needed ([references/l3-sources.md](references/l3-sources.md)).
3. Execute product tools per mcp-memnet; do not restate wire grammar.
4. Stop. Do not paste section-13 math onto `pin_map`.
