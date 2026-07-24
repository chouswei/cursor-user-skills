---
name: memnet-format
description: >-
  MemNet 0.3.1 shared dialect (Write=display) for live pin map and mutate.
  Triggers: memnet format, shared dialect, Write=display, pin map, mutate NEW,
  NODE EDGE, atomised rows.
metadata:
  pattern: tool-wrapper
  version: "3.0"
  domain: data-formats,memnet
  product: memnet-llm==0.3.1
---

# MemNet formats (LLM-facing)

**Audience:** model. Pair with [mcp-memnet](../mcp-memnet/SKILL.md) for tools.

**Shared dialect only** (Write = display): same NODE | EDGE shapes for live pin map and mutate. Design docs may still say “Tier A” once; use **shared dialect** thereafter. Do **not** use TOON/TRON. Prefer shared dialect or plain Markdown for handoffs.

Product SSOT: MemNet `README.md`, `docs/grammar/`. Field notes: [references/memnet-wire-format.md](references/memnet-wire-format.md).

---

## Shared dialect

Mutate uses ops (`+` create, `~` update, `-` drop). Live pin map is **bare present** (no leading ops).

```text
## Nodes
+ CLM [NEW] ; type=decision ; code=bitrate cap 2000 bps ; recycle=persistent
~ TSK [T42] ; status=in_progress ; recycle=persistent

## Edges
+ E77 [N03] --(helps)--> [T42] ; note=labour ; recycle=persistent
```

- **Create:** `[NEW]` / leading `NEW` — engine mints ids; copy them afterwards.
- **Update:** known ids only.
- **Ingest pins:** stable locators (`path=`, `qname=`, …); no client `NEW` for those.

Primary read: live **pin map**. (MCP tool may still be named `query_warm`.)

---

## When to use which kind

| Need | Kind |
|------|------|
| Fact / claim | `CLM` (+ edges) |
| Directed relation | edge `--(rel)-->` |
| Flat membership list | `SET` or `IDX` |
| Work unit | `TSK` |
| User constraint | `USR` |
| File / symbol | `MOD` / `SYM` |
| SysML element | `PRT` / `POR` / `CON` / `REQ` / `SYM` |
| Rule / policy | `RUL` |

Membership of many ids → `SET`. Directed relation → edge.

---

## Handoff tiers

| Priority | When | Format |
|----------|------|--------|
| 1 | Durable / multi-step with MemNet up | Shared dialect mutate |
| 2 | No session / same-turn scratch | Plain Markdown |
| 3 | Tool / MCP / CLI boundary | JSON envelope |
| 4 | Human deliverable | Prose Markdown |

---

## Atomisation (before every mutate)

1. Split fat rows into multiple rows + edges when possible.
2. Field values = short ids, paths, codes, numbers — no sentences.
3. Stable id from prior pin map or `add` response.
4. No prose paragraphs on the wire.

Full discipline: [mcp-memnet/references/atomisation.md](../mcp-memnet/references/atomisation.md).

---

## Pre-write checklist

- [ ] Pin map on a tight anchor
- [ ] Values short and structured
- [ ] Relations are edges
- [ ] Recycle matches lifetime
- [ ] Atom reachable from a useful anchor

---

## Further reading

- [references/memnet-wire-format.md](references/memnet-wire-format.md) — shared-dialect field notes
- [mcp-memnet](../mcp-memnet/SKILL.md) — tools and session loop
- MemNet `docs/grammar/` — design SSOT
