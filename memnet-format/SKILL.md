---
name: memnet-format
description: >-
  MemNet formats for agents: Tier A (Write=display) preferred for live pin map and
  mutate; legacy @TAG pipe for store/snapshots. Triggers: memnet format, Tier A,
  pin map, @TAG, pipe rows, @EDG, atomised rows, memnet wire.
metadata:
  pattern: tool-wrapper
  version: "2.0"
  domain: data-formats,memnet
  product: memnet-llm==0.3.1
---

# MemNet formats (LLM-facing)

**Audience:** model. Pair with [mcp-memnet](../mcp-memnet/SKILL.md) for tools.

- **Preferred agent dialect:** **Tier A** — same NODE | EDGE shapes for live pin map and mutate (Write = display).
- **Legacy store dialect:** `@TAG:` pipe rows — still accepted on mutate; used in older snapshots.
- **Do not** use TOON/TRON. Prefer Tier A or plain Markdown for handoffs.

Product SSOT: MemNet `README.md`, `docs/grammar/`. Pipe field tables: [references/memnet-wire-format.md](references/memnet-wire-format.md).

---

## Tier A (agent)

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

Primary read: live **pin map** (`query_warm` is the legacy MCP/CLI name).

---

## Legacy pipe (store)

```text
@TAG: id|field2|field3|...|recycle
```

```text
@RUL: F01|MUST|one atom per line; exactly one : after tag|high
@RUL: F02|MUST|relations as separate @EDG rows (never embedded arrays)|high
@RUL: F03|MUST|escape literal | as \| inside field values|high
@RUL: F04|MUST|last field = recycle: persistent|delete_on_settle|delete_on_expire|high
@RUL: F05|MUSTNOT|prose blobs or nested JSON on the wire|high
@RUL: F06|SHOULD|query_warm(anchor, depth≤2) before inventing ids|high
```

### Tag selection (pipe)

```text
@SEL: fact_or_claim|@CLM + @ENT + @EDG|atomic verifiable statement
@SEL: relationship|@EDG|from|rel|to
@SEL: flat_enumeration|@SET or @IDX|membership list
@SEL: work_unit|@TSK|goal, phase, status, recycle
@SEL: user_constraint|@USR|lasting scope, style, preference
@SEL: file_or_symbol|@MOD @SYM|coding memory
@SEL: sysml_element|@PRT @POR @CON @REQ @SYM|sysml patterns
@SEL: rule_or_policy|@RUL|normative directive with priority
```

**@EDG vs @SET:** membership of many ids → `@SET`. Directed relation → `@EDG`.

---

## Handoff tiers

```text
@ROU: handoff_0|LLM/author-facing|Tier A Write=display (or English pins)
@ROU: handoff_1|durable store write|Tier A mutate preferred; @TAG pipe legacy
@ROU: handoff_2|no session / same-turn scratch|plain Markdown tables or short prose
@ROU: handoff_3|tool/MCP/CLI boundary|JSON envelope only
@ROU: handoff_4|human operator deliverable|prose Markdown
```

---

## Atomisation (before every mutate)

```text
@RUL: A01|MUST|split fat row into multiple rows + edges if possible|high
@RUL: A02|MUST|field values = short ids, paths, codes, numbers (no sentences)|high
@RUL: A03|MUST|stable id from prior pin map or add response|high
@RUL: A04|MUSTNOT|prose paragraphs on the wire|high
```

Full discipline: [mcp-memnet/references/atomisation.md](../mcp-memnet/references/atomisation.md).

---

## Pre-write checklist

```text
@CHK: w1|pin map (query_warm) on tight anchor|pass|fail
@CHK: w2|values short and structured|pass|fail
@CHK: w3|relations are edges|pass|fail
@CHK: w4|recycle matches lifetime|pass|fail
@CHK: w5|atom reachable from useful anchor|pass|fail
```

---

## Further reading

- [references/memnet-wire-format.md](references/memnet-wire-format.md) — pipe grammar detail
- [mcp-memnet](../mcp-memnet/SKILL.md) — tools and session loop
- MemNet `docs/grammar/` — Tier A SSOT
