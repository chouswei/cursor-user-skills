# MemNet shared dialect — field notes

**Audience:** model. Agent I/O for **memnet-llm 0.3.5** is the **shared dialect** only (Write = display). See [../SKILL.md](../SKILL.md) and MemNet `docs/grammar/`.

Do **not** emit `@TAG: field|field|…` pipe rows as agent format.

## Line shapes

**Mutate** (ops required):

```text
## Nodes
+ KIND [NEW] ; field=value ; … ; recycle=persistent
~ [KnownId] ; field=value ; recycle=persistent
- Eid

## Edges
+ [NEW|Eid]? [FromId] --(rel)--> [ToId] ; note=… ; recycle=persistent
~ [FromId] --(rel)--> [ToId] ; …
~ Eid ; recycle=delete_on_settle
```

Patch nodes: **`~ [Id]` only** — do not repeat kind (`~ TSK [T42]` is invalid). Re-id: `~ [OldId] ; id=NewId` (optional `; merge=true` on nodes).

**Pin map** (bare present — copy these shapes on the next mutate, without leading ops):

```text
## Laws
LAW01 kind=engine ; text=one_row_per_id_tag ; recycle=persistent

## Nodes
CLM [C12] ; type=decision ; code=bitrate cap 2000 bps ; recycle=persistent
TSK [T42] ; goal=Clear warehouse ; status=in_progress ; recycle=persistent

## Edges
E77 [N03] --(helps)--> [T42] ; note=labour ; recycle=persistent
```

**Session schema** (`session_open` map — not graph rows):

```text
SCHEMA MOD ; fields=id path summary status recycle
```

## Fields (R1 atoms-only)

- Join with `;` — `key=value`
- Numeric patch ops: `phase+=1`, `risk-=0.5` (numbers only)
- Values: bare atoms, `NUMBER`, or `"quoted strings"` (paths with `\` or spaces)
- No nested lists/maps in one field — use EDGE lines for membership

## Recycle

- `persistent` — enduring structure and facts
- `delete_on_settle` — drop when owning task settles
- `delete_on_expire` — time-based (rare in agent flows)

## Common kinds (fields are English keys)

| Kind | Typical fields |
|------|----------------|
| `CLM` | `type`, `code`, `status`, `recycle` |
| `TSK` | `goal`, `phase`, `status`, `recycle` |
| `USR` | `topic`, `content`, `status`, `recycle` |
| `RUL` | `kind`, `code`, `priority`, `recycle` |
| `MOD` | `path`, `lang`, `role`, `loc`, `recycle` |
| `SYM` | `name`, `kind`, `path`, `line`, `sig`, `vis`, `recycle` |
| `PRT` / `POR` / `CON` / `REQ` | SysML patterns — see sysml-memnet-patterns |
| Edge | `--(rel)-->` plus optional `note`, `recycle` |

Keep field values short. Relations are separate edges, never embedded arrays or comma id-lists.

## Design principles

| Principle | Why |
|-----------|-----|
| Atomisation | Pin map returns only connected atoms |
| Short fields | ids, codes, paths, numbers — no prose |
| Explicit edges | Filterable relations |
| Recycle / settle | Finished work drops out of pin maps |
| Batch mutate | One `add`/`update` with many lines |

Primary read: live **pin map** via MCP `pin_map`. (`query_warm` is legacy alias.)

Cross-ref: MemNet `README.md` · `docs/grammar/` · [mcp-memnet](../../mcp-memnet/SKILL.md)
