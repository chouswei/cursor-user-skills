---
name: memnet-stm-harness
description: >-
  Thin pointer to STM thesis-lock playbooks for agent harness wiring,
  STM debug triage, working set W vs inventory S, and user input as
  control. Triggers: agent harness, STM debug, W vs S, working set vs
  inventory, user-input-as-control, thesis locks, pin_map vs dump.
metadata:
  pattern: pipeline
  version: "1.1"
  domain: memnet
  product: "memnet-llm==0.19.5"
token_guardrails: |
  - Pointer only. MUST load the named GitHub playbook. MUST NOT paste thesis math or playbook body.
  - Product loop stays mcp-memnet + memnet-format. Honesty c / memnet-llm==0.19.5; 1.0 unclaimed.
---

# STM thesis harness (pointer)

**Not a second thesis.** Doctrine SSOT lives in [llm-stm-mechanics](https://github.com/chouswei/llm-stm-mechanics) playbooks. This skill names **when** to open which file. Operational checklist (turn loop): [llm-stm-analytical-mechanics](../llm-stm-analytical-mechanics/SKILL.md). Tools: [mcp-memnet](../mcp-memnet/SKILL.md). Wire: [memnet-format](../memnet-format/SKILL.md). **Package and PyPI 0.19.5** (honesty `c` on 0.19 -- not a usage-method `b`). **1.0** unclaimed.

## When to load

| Job | Open |
|-----|------|
| Wire an agent that uses session memory (cue, `pin_map`, admission, Commit) | Playbook 1 |
| Task failed; need triage | Playbook 2 (after Playbook 1 if the harness is unknown) |
| Investor CompanyMemory desk mapping only | Playbook 3 (one-line; do not treat as generic MemNet law) |

## MUST load (do not restate)

1. **Harness (wire):** https://github.com/chouswei/llm-stm-mechanics/blob/main/playbooks/agent-harness-from-thesis-locks.md
2. **Debug (triage):** https://github.com/chouswei/llm-stm-mechanics/blob/main/playbooks/debugging-stm-from-thesis-locks.md
3. **Investor desk only:** https://github.com/chouswei/llm-stm-mechanics/blob/main/playbooks/investor-companymemory-from-thesis-locks.md -- MemNet owns the session; Neo4j owns the disk. Skip unless that desk is in scope.

## Pointer-level locks (names only)

| Lock | Agent hear |
|------|------------|
| W vs S | Working set **W** / shaped `pin_map` is not inventory dump **S** |
| Cue | kind / labels+properties / keyword, then `pin_map`; empty q = outline; drop prior maps from the prompt |
| User input | Control **u** / admitted mass in W / discrete force -- not automatic inventory |
| Identity | Graph element. Nickname `id` / hid / elementId off shaped emit (`SHAPE_DROP_KEYS`, memnet-llm 0.19.5). Cue by locators as properties -- not nickname or hid |
| Write | Gated Commit / `mutate` (CREATE / MATCH...SET / DELETE). leftover `add`/`update`/`NEW`/`--anchor` are leftover |
| Debug | Split proposal / admission / eviction / integrate / Commit -- Playbook 2 |

## Steps

1. Classify the job (wire / debug / Investor desk).
2. Fetch and follow the matching playbook. Do not invent a local restatement.
3. Execute product tools per [mcp-memnet](../mcp-memnet/SKILL.md). Shared workers: [memnet-multitask](../memnet-multitask/SKILL.md) -- hand off **session id** + locators; peer re-pins; do not ship a dump of S.
4. Stop. Do not paste §13 math, lambda, momentum, coverage, or m onto `pin_map`.

## MUST NOT

- Duplicate playbook or thesis body in this pack.
- Teach leftover `--anchor` / `id:'NEW'` / `add`/`update` as TARGET.
- Treat honesty `c` / wire leaks as a SemVer a/b claim, or claim MemNet **1.0**.
