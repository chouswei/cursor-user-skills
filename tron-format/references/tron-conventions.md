# TRON Format Conventions

> **DEPRECATED.** Do not use TRON (or TOON) for handoffs. Prefer plain Markdown or MemNet Tier A. See [../SKILL.md](../SKILL.md). Historical notes below are not encoding advice.

**Audience:** Historical reference only (not active encoding advice).

## Core idea

TRON reduces token redundancy by extracting repeated property names into reusable class definitions. Instances then only carry values + a class reference.

## Comparison

| Aspect           | JSON                  | TRON                          | TOON                     |
|------------------|-----------------------|-------------------------------|--------------------------|
| Token efficiency | Baseline              | Excellent for repeated keys   | Excellent for tables     |
| Human readable   | Good                  | Moderate                      | Very good (tabular)      |
| Random access    | Full parse            | HAMT supported                | Full parse               |
| Best for         | General interchange   | Structured repeated objects   | Prompt tables / records  |

## Pipeline and skill handoffs

- **Default in this workspace:** tabular / uniform rows → **TOON** (skill **toon-prompt-format** in repo `.cursor/skills/` or user pack `~/.cursor/skills/`).
- **Use TRON** between steps when the handoff is **many objects of the same schema** (not a single flat table) and **key names dominate** token count.
- **Mermaid diagram placement** (serve down): historical note said TRON `DiagramPlan` — **do not**; use Markdown tables per [mermaid-placement-by-degree.md](../../mermaid/references/mermaid-placement-by-degree.md).
- **JSON** only when a tool or API requires it; use `TRON.stringify` / `TRON.parse` in code at boundaries when you standardise on TRON.

## Usage rules

- Prefer TRON when a large share of tokens are repeated keys in a JSON-like payload (benchmark in the [playground](https://tron-format.github.io/#/playground)).
- For **uniform row grids**, evaluate **TOON** first (often clearer to models).
- When justifying format choice, cite relative size or token estimate where possible.
- Official JS lib: `@tron-format/tron`
- Go: `github.com/visionik/trongo`

## When not to use TRON

- **One-off** shallow objects with few repeated instances — JSON overhead may not matter.
- **Highly irregular** schemas (different keys per object) — TRON’s class reuse wins less; benchmark.
- **Human-maintained** prose tables — keep Markdown unless token cost is the priority.

## Playground

https://tron-format.github.io/#/playground — use to demonstrate savings on real data.
