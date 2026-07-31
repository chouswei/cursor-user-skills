---
name: prompt-writing-discipline
description: >-
  Author discipline for LLM-consumed prose: accurate, precise, low noise,
  consistent, coherent; prefer clear English names over opaque codes/abbreviations
  (expand first use if a house label must appear).
  Use when writing or editing skills, rules, prompts, agent hubs, design notes,
  or other text aimed at models -- not product wire formats.
  Triggers: prompt writing, writing discipline, low noise prose, precise wording,
  consistent terminology, coherent docs, expand abbreviations, clear English names,
  opaque tier codes, LLM-facing text, skill prose, agent hub copy.
metadata:
  pattern: pipeline
  domain: doc
  version: "1.3"
---

# Prompt writing discipline

Author discipline for **LLM-consumed** text (skills, rules, prompts, agent hubs, design notes). Not a product or wire-format skill.

## When to apply

Writing or editing prose that a model will read. Skip for human-only marketing fluff or proprietary serialisation dialects unless the user asks.

## Seven disciplines (MUST)

| Discipline | MUST |
|------------|------|
| **Accurate** | State only what is true and checkable; no invented facts or soft hedges that hide uncertainty. |
| **Precise** | Prefer the exact term, bound, or step; avoid vague fillers ("somehow", "various", "appropriately"). |
| **Low noise** | Cut throat-clearing, repetition, and ornamental asides; every sentence earns its place. |
| **Consistent** | One term per concept; same voice, tense, and naming across the piece. |
| **Coherent** | Order so later lines follow from earlier ones; no orphan claims or topic jumps. |
| **Abbreviations** | Prefer clear English names over opaque codes; drop needless abbreviations; expand house labels on first use (see below). |
| **Positive** | Name the wire structure in positive terms, then the per-item gate. |

## Abbreviation rule

1. Default: write the expanded, plain-English name -- not an internal code or cryptic tier.
2. Keep an abbreviation only if it is standard in the domain **and** clearer than the expansion after first use.
3. If a house label must appear (design-doc shorthand, legacy pin): expand on first use with the meaning, then prefer the plain name thereafter.
4. Do not invent cryptic tiers/codes (`T1`, `LAW-PIPE20`, unglossed house labels) as the primary agent-facing term.
5. Optional example (MemNet): if a design doc says "Tier A", write **Tier A (shared dialect -- Write = display)** once, then prefer **shared dialect**.
6. Prefer **ASCII** in LLM-consumed skill/rule/hub text (`->` not arrows; `--` not em dashes; no smart quotes). See pack rule R16 in `LLM.md`.
7. When spawning Task/subagents: set `model` per `sub-agent-policy` / R17 (thinking/unclear -> `cursor-grok-4.5-low`; visual items review -> `kimi-k3-max`; MemNet snapshot -> `gpt-5.6-luna-medium`). **MUSTNOT** use any `*-fast` / FAST slug.

## Good vs bad (one-liners)

| Bad | Good |
|-----|------|
| "Leverage the util to somehow sync stuff ASAP." | "Run `scripts/sync.py` to copy config into the target folder." |
| "Use CFG / ENV / RT interchangeably." | "Use **config** for files; **environment variable** for process env." |
| "Follow Tier A / T1 / LAW-PIPE20." | "Follow the **shared dialect** (Write = display); expand any house label on first use." |
| "The NFT of the SKL is TBD w.r.t. QoS." | "Skill metadata version is unset; quality targets are not defined yet." |
| Three paragraphs restating the same MUST. | One MUST line; no restatement. |

## Checklist before emit

- [ ] Accurate -- claims match sources or are marked unknown
- [ ] Precise -- terms and bounds are concrete
- [ ] Low noise -- no padding or duplicate instructions
- [ ] Consistent -- one name per concept
- [ ] Coherent -- sequence and cross-references hold
- [ ] Abbreviations -- clear English names first; needless codes removed; house labels glossed once then plain name
- [ ] Positive -- wire structure named positively, then the per-item gate
- [ ] British English for new docs unless the host file already uses another locale
