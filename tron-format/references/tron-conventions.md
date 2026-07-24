# TRON Format Conventions

> **DEPRECATED.** Do not use TRON (or TOON) for handoffs. Prefer plain Markdown or MemNet **shared dialect** (Write = display). See [../SKILL.md](../SKILL.md). Everything below is historical only — **not** encoding advice.

**Audience:** Historical reference only (not active encoding advice).

## Core idea

~~TRON reduces token redundancy by extracting repeated property names into reusable class definitions.~~ **Do not encode handoffs in TRON.**

## Comparison (historical)

| Aspect           | JSON                  | TRON                          | TOON                     |
|------------------|-----------------------|-------------------------------|--------------------------|
| Token efficiency | Baseline              | Excellent for repeated keys   | Excellent for tables     |
| Human readable   | Good                  | Moderate                      | Very good (tabular)      |
| Random access    | Full parse            | HAMT supported                | Full parse               |
| Best for         | General interchange   | Structured repeated objects   | Prompt tables / records  |

## Pipeline and skill handoffs — TOMBSTONED

~~Default TOON / use TRON between steps / Mermaid DiagramPlan in TRON / JSON only at boundaries.~~

**Current rule:** durable agent handoffs → MemNet **shared dialect** (or plain Markdown when MemNet is down). Mermaid placement when serve is down → Markdown tables per [mermaid-placement-by-degree.md](../../mermaid/references/mermaid-placement-by-degree.md). JSON only when a tool requires it.

## Usage rules — TOMBSTONED

~~Prefer TRON when keys dominate; evaluate TOON for grids; cite playground savings; use `@tron-format/tron` / `trongo`.~~ **Do not follow.**

## When not to use TRON

Always — TRON is deprecated for this pack. Prefer shared dialect or Markdown.

## Playground

https://tron-format.github.io/#/playground — historical demos only; not a handoff format for this pack.
