---
name: prompt-writing-discipline
description: >-
  Author discipline for LLM-consumed prose: accurate, precise, low noise,
  consistent, coherent; drop unnecessary abbreviations (expand first use if kept).
  Use when writing or editing skills, rules, prompts, agent hubs, design notes,
  or other text aimed at models — not product wire formats.
  Triggers: prompt writing, writing discipline, low noise prose, precise wording,
  consistent terminology, coherent docs, expand abbreviations, LLM-facing text,
  skill prose, agent hub copy.
metadata:
  pattern: pipeline
  domain: doc
  version: "1.0"
---

# Prompt writing discipline

Author discipline for **LLM-consumed** text (skills, rules, prompts, agent hubs, design notes). Not a product or wire-format skill.

## When to apply

Writing or editing prose that a model will read. Skip for human-only marketing fluff or proprietary serialisation dialects unless the user asks.

## Six disciplines (MUST)

| Discipline | MUST |
|------------|------|
| **Accurate** | State only what is true and checkable; no invented facts or soft hedges that hide uncertainty. |
| **Precise** | Prefer the exact term, bound, or step; avoid vague fillers (“somehow”, “various”, “appropriately”). |
| **Low noise** | Cut throat-clearing, repetition, and ornamental asides; every sentence earns its place. |
| **Consistent** | One term per concept; same voice, tense, and naming across the piece. |
| **Coherent** | Order so later lines follow from earlier ones; no orphan claims or topic jumps. |
| **Abbreviations** | Drop unnecessary abbreviations; prefer expanded forms (see below). |

## Abbreviation rule

1. Default: write the expanded form.
2. Keep an abbreviation only if it is standard in the domain **and** clearer than the expansion after first use.
3. If kept: expand on first use (`application programming interface (API)`), then the short form.
4. Do not invent house abbreviations for one-off phrases.

## Good vs bad (one-liners)

| Bad | Good |
|-----|------|
| “Leverage the util to somehow sync stuff ASAP.” | “Run `scripts/sync.py` to copy config into the target folder.” |
| “Use CFG / ENV / RT interchangeably.” | “Use **config** for files; **environment variable** for process env.” |
| “The NFT of the SKL is TBD w.r.t. QoS.” | “Skill metadata version is unset; quality targets are not defined yet.” |
| Three paragraphs restating the same MUST. | One MUST line; no restatement. |

## Checklist before emit

- [ ] Accurate — claims match sources or are marked unknown
- [ ] Precise — terms and bounds are concrete
- [ ] Low noise — no padding or duplicate instructions
- [ ] Consistent — one name per concept
- [ ] Coherent — sequence and cross-references hold
- [ ] Abbreviations — needless ones removed; kept ones glossed once
- [ ] British English for new docs unless the host file already uses another locale
