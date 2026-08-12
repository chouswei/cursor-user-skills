---
name: memnet-format
description: >-
  MemNet 0.4.2 shared dialect (Write=display) for live pin map and mutate.
  Triggers: memnet format, shared dialect, Write=display, pin map, pin_map, mutate NEW,
  NODE EDGE, atomised rows, Layer, view=shell.
metadata:
  pattern: tool-wrapper
  version: "3.7"
  domain: data-formats,memnet
  product: memnet-llm==0.4.2
---

# MemNet formats (LLM-facing)

**Audience:** model. Pair with [mcp-memnet](../mcp-memnet/SKILL.md) for tools.

**Shared dialect only** (Write = display): same NODE | EDGE shapes for live pin map and mutate. Design docs may gloss this as “Tier A”; prefer **shared dialect** in agent text. Formal productions, golden fixtures, and the ANTLR stub live under MemNet `docs/grammar/` — keep those rules; this skill is the thin agent summary. Do **not** use TOON/TRON. Prefer shared dialect or plain Markdown for handoffs. Do **not** teach pipe `@TAG:…` as agent I/O (legacy store/import only).

Product SSOT: MemNet `README.md`, `docs/grammar/`. Field notes: [references/memnet-wire-format.md](references/memnet-wire-format.md).

---

## Shared dialect

Mutate uses ops (`+` create, `~` update, `-` drop). Live pin map is **bare present** (no leading ops). Formal SSOT: `MemNet.g4`, golden fixtures under `docs/grammar/examples/`.

```text
## Nodes
+ CLM [NEW] ; type=decision ; code=bitrate cap 2000 bps ; recycle=persistent
~ [T42] ; status=in_progress ; phase+=1 ; recycle=persistent

## Edges
+ E77 [N03] --(helps)--> [T42] ; note=labour ; recycle=persistent
+ NEW [S03] --(part_of)--> [ART_pdu] ; recycle=delete_on_settle
~ E77 ; recycle=delete_on_settle
- E77
```

| Op | Shape |
|----|-------|
| Create node | `+ KIND [NEW\|Id] ; fields…` |
| Patch node | `~ [KnownId] ; fields…` — **no kind** on patch |
| Create edge | `+ [NEW\|Eid]? [from] --(rel)--> [to] ; fields…` |
| Patch edge | `~ [from] --(rel)--> [to] ; …` or `~ Eid ; …` |
| Drop edge | `- Eid` |
| Present | `KIND [Id] ; …` / `Eid [from] --(rel)--> [to] ; …` |
| Session schema | `SCHEMA KIND ; fields=id …` — registry only (`session_open` map) |

- **Create:** `[NEW]` / leading `NEW` — engine mints ids; copy them afterwards.
- **Update:** known ids in `[brackets]` only — `[NEW]` illegal on `~`.
- **Fields (R1):** `key=value` or `key+=N` / `key-=N`; atoms only — use edges for membership, not comma lists.
- **Quotes:** `"C:\\Projects\\…"` when paths need `\` or spaces.
- **Ingest pins:** stable locators (`path=`, `qname=`, …); no client `NEW` for those.

Primary read: live **pin map** via MCP `pin_map` / CLI `query pin-map`. Optional `view=shell` (tight budget) or `view=interior`. (`query_warm` is legacy alias.)

**Layer (0.4 additive):** dual EDGE — port↔port teach **`bind`** (`[Node.port] --bind--> [Node.port]`); node↔node = relation label. Law/`ports=` on NODE (`CST`). SSOT: MemNet `docs/grammar/memnet-multi-layer.md`. Coexists with shared-dialect `--(rel)-->` edge labels.

User-pack engine: TCP serve **`10.0.0.10:18765`** — see [mcp-memnet](../mcp-memnet/SKILL.md).

---

## When to use which kind

| Need | Kind |
|------|------|
| Fact / claim | `CLM` (+ edges) |
| Directed relation | edge `--(rel)-->` |
| Flat membership list | edges (`member_of`, `contains`, …) — R1: no id lists in fields |
| Work unit | `TSK` |
| User constraint | `USR` |
| File / symbol | `MOD` / `SYM` |
| Rule / policy | `RUL` |
| SysML model atoms | see **SysML x MemNet** below — do not invent kinds here |

Membership of many ids → multiple **edges**. Directed relation → edge.

**`rel` style (engine):** English verb / snake token (`owns`, `satisfies`, `contains`, …) per MemNet `docs/grammar/`. Session registries may already hold other spellings — **copy from the live pin map**; never invent a second spelling for the same link.

---

## SysML x MemNet

Engine-generic dialect stays above. **SysML construct map, `kind` enums, EDG closed list, and batch rules** are SSOT in [sysml-memnet-documentation](../sysml-memnet-documentation/SKILL.md) → [sysml-memnet-patterns.md](../sysml-memnet-documentation/references/sysml-memnet-patterns.md). Cache loop: [sysml-memnet-cache](../sysml-memnet-cache/SKILL.md).

| SysML v2 textual (grammar) | MemNet | Stable id |
|----------------------------|--------|-----------|
| `package` | `PKG` | `PKG_<suffix>` |
| `part def` / part usage | `PRT` (+ `SYM` locator) | `PRT_<name>` |
| `port def` / port usage | `POR` (+ `SYM`) | `POR_<name>` |
| `connection` / `connect` / link | `CON` (+ `SYM`) | `CON_<name>` |
| `requirement` def/usage | `REQ` (+ `SYM`) | `REQ_<requirementId>` |
| `item def` / flow item | `ITM` **NODE** (see [ITM pattern](../sysml-memnet-documentation/references/sysml-memnet-patterns.md#itm-is-a-node)) | `ITM_<name>` |
| `state def` / action / calc | `BEH` (+ `SYM`) | `BEH_<name>` |
| `assert` … `satisfy` | **edge only** `satisfies` | — |
| `allocate` / `allocation` | **edge only** `allocates` | — |
| `.sysml` file / edit locus | `MOD` / `SYM` | `MOD_<slug>` / `SYM_<name>` |

House anchors (copy, do not mint colliding prefixes): `TSK_model_<short>`, `TSK_diagram_<figureId>`, `USR_*`, plus the `PRT_` / `POR_` / `REQ_` / `BEH_` / `SYM_` / `MOD_` rows above. `satisfy` / `allocate` are never structure nodes — edges only (`@SYM` only if a line locator is needed).

Deep atomisation, closed EDG spellings, and specialist write map → patterns / [relatives-cache-map.md](../sysml-memnet-documentation/references/relatives-cache-map.md).

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
- [sysml-memnet-documentation](../sysml-memnet-documentation/SKILL.md) — SysML atomisation SSOT (patterns, snap, cache)
- MemNet `docs/grammar/` — design SSOT
