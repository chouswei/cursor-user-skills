# MemNet wire format — detailed reference

This is the authoritative format guide for writing and reading the compact pipe-row language that MemNet exposes to LLMs.

It is the sibling of the in-prompt formats (TOON / TRON) — use it when you need **durable, queryable, atomised state** that lives outside the current context window.

## Line syntax

```text
@TAG: field1|field2|field3|...|recycle
```

- Tag is always uppercase, starts with `@`.
- Exactly one `:` (no space before it, one space after).
- Fields separated by literal `|`.
- Escape a literal `|` inside any field value as `\|`.
- No trailing `|` at end of record.
- One record per line.
- Order of fields per tag is **stable** — see tables below. Do not invent new positions.

Control / meta lines (usually appear on stderr or prepended by the serve):
- `@LAW:` — protocol laws / invariants (prepended to every `query_warm` response)
- `@ERR:`, `@WRN:`, `@STAT:`, `@SESSION:`

All normal data rows travel on stdout (inside the MCP JSON envelope's `stdout` field).

## Design principles (why this shape)

| Principle | Token / behaviour benefit |
|-----------|---------------------------|
| Pipe rows, not JSON trees | `@MOD: M1\|path\|summary` is ~1/3 the tokens of a nested object for the same info |
| One atom per row | `query_warm` can return a tiny relevant subgraph instead of everything |
| Explicit `@EDG` rows | No arrays or repeated key lists inside a record; relations are first-class and filterable |
| Short structured fields only | ids, paths, short codes, numbers, enums — zero prose |
| Recycle policy on every atom | Transient work (`delete_on_settle`) automatically drops out of future warm slices |
| Anchor + depth reads | You pay only for the connected component you asked for |

## Recycle policies (last field on most tags)

- `persistent` — lives until explicitly deleted or the whole store is reset. Use for modules, enduring claims, user prefs, model structure.
- `delete_on_settle` — the row is removed when its owning `@TSK` is updated to `status=settled`. Use for step-local tasks, hypotheses, scratch edges.
- `delete_on_expire` — time- or use-based (less common in agent flows).

## Core tags and field order

### Meta / policy rows (rules, skills, catalog — in-file wire)

Use in LLM-only skills and `.mdc` rules (not necessarily pushed to `memnet serve`):

```text
@RUL: id|kind|directive|priority
@PRC: step|action|then
@ROU: anchor|condition|target
@SEL: use_case|tag_or_pattern|note
@CHK: id|check|pass|fail
@TRG: phrase|skill-id
@IDX: id|kind|count|recycle
@SET: id|csv_payload
```

- `@RUL.kind`: `MUST` | `MUSTNOT` | `SHOULD` | `MAY`
- `@RUL.priority`: `high` | `med` | `low`
- `@IDX` + `@SET`: flat enumeration without N× `@EDG memberOf` rows; verify count via `@IDX` field 3
- Cross-doc relations still use `@EDG` (delegates, governs, overrides, documents, …)

### Universal / orchestration

```text
@TSK: id|goal|phase|status|recycle
@USR: id|topic|value|status|recycle
@EDG: id|from|rel|to|note|recycle
```

- `phase` / `status` are short enums (e.g. `model|in_progress`, `sync|settled`).
- `rel` on `@EDG` is a verb: `owns`, `defines`, `satisfies`, `contains`, `mentions`, `constrained_by`, `calls`, `documents`, `maps_to`, etc. Choose one that will still make sense when read 20 turns later.

### Coding memory

```text
@MOD: id|path|summary|status|recycle
@SYM: id|name|kind|file|line|signature|status|recycle
```

Use one `@MOD` per file you care about, one `@SYM` per function/class/symbol whose location or call graph matters. Link with `@EDG`.

### Article / document / report breakdown (outputs, specs, papers)

```text
@ART: id|title|source|kind|status|recycle
@SEC: id|art|heading|order|status|recycle
@CLM: id|sec|type|code|status|recycle
@ENT: id|name|kind|code|recycle
```

- `kind` on `@ART`: `report|interconnection|behaviour|requirements|traceability|paper`
- `type` on `@CLM`: `fact|stat|decision|assumption|conclusion|quote|convention|method`
- `code` on `@CLM` is the distilled payload (≤ ~12–15 words). The actual prose is generated at use time from the warm slice.
- One `@CLM` per atomic, checkable statement. Never put a whole paragraph in `code`.

### SysML / MBSE elements (canonical map — copy verbatim to `session_open`)

Use with [sysml-memnet-patterns.md](../../sysml-memnet-documentation/references/sysml-memnet-patterns.md). **MUST NOT** write legacy `@PARTD`, `@PORTD`, `@BEHD`, or `@TASK`.

```text
@ART: id|title|source|kind|status|recycle
@SEC: id|art|heading|order|status|recycle
@CLM: id|sec|type|code|status|recycle
@ENT: id|name|kind|code|recycle
@PKG: id|qname|kind|status|recycle
@PRT: id|name|kind|role|status|recycle
@POR: id|name|kind|dir|typeRef|status|recycle
@CON: id|name|kind|ends|status|recycle
@BEH: id|name|kind|owner|status|recycle
@ITM: id|name|kind|status|recycle
@REQ: id|requirementId|text|status|recycle
@MOD: id|path|pkg|role|status|recycle
@SYM: id|name|kind|path|line|owner|status|recycle
@CONV: id|topic|rule|status|recycle
@DEC: id|task|question|options|chosen|recycle
@ISSUE: id|task|code|status|recycle
@TSK: id|goal|phase|status|recycle
@USR: id|topic|value|status|recycle
@EDG: id|from|rel|to|note|recycle
```

Field notes:

- `@PRT.kind`: `partDef|partUsage`; `@POR.kind`: `portDef|portUsage`; `@CON.kind`: `connectionDef|connectionUsage|linkUsage`
- `@BEH.kind`: `stateMachine|action|calculation`; `@ITM.kind`: `itemDef|flowItem`
- `@PKG.kind`: `deploy|requirements|connections|behaviour|root|library|common`
- `@POR.dir`: `in|out|inout` for usages; empty for defs. `@POR.typeRef` for `typedBy` EDG.
- `@CON.ends`: `endA|endB` usage path. `@BEH.owner`: owning `@PRT` id or package qname.
- Use **exact** names from `.sysml` or MCP. `satisfy`/`allocate` → `@EDG` only (`satisfies`, `allocates`).
- Every new `@PRT`/`@POR`/`@CON` **MUST** include `declaredIn` + `inFile` EDGs in the same batch.

## Good vs bad (token and graph-behaviour examples)

**Bad (monolithic, defeats warm reads):**

```text
@NOTE: N42|The PDU design uses a 24 V rail. ModemTX is on linkPowerToModemTX. We decided on 2000 bps because of harbour noise. Battery is 400 Wh. This contradicts the earlier 120 W peak assumption in section 3.|persistent
```

**Good (atomised + linked):**

```text
@ART: ART_pdu|PDU system design|outputs/design.md|report|active|persistent
@SEC: S03|ART_pdu|Power budget|3|active|persistent
@CLM: C10|S03|fact|24 V rail feeds both modems via F3|active|persistent
@CLM: C11|S03|decision|acoustic bitrate capped at 2000 bps for harbour reliability|active|persistent
@CLM: C12|S03|stat|battery 400 Wh nominal|active|persistent
@CON: CON_pwr_tx|linkPowerToModemTX|linkUsage|ModemPowerOut|ModemTX.powerIn|active|persistent
@EDG: E10|S03|contains|C10|claim|persistent
@EDG: E11|C10|mentions|CON_pwr_tx|subject|persistent
@EDG: E12|CON_pwr_tx|declaredIn|PKG_deploy_pdu|origin|persistent
```

Now `query_warm(anchor="S03", depth=2)` returns only the relevant power section atoms.

## Escaping and batching

- Inside any field: `|` becomes `\|`, and if you ever need a literal backslash before a pipe you double it.
- Prefer **one `add` / `update` call with many lines** in the `wire_lines` array rather than many round-trips.
- The MCP envelope is JSON; the wire rows inside `stdout` are plain text (parse line-by-line).

## Warm read behaviour

Every `query_warm` response (via MCP) contains:
1. Zero or more `@LAW:` rows (immutable protocol rules for this session).
2. The anchor atom (if it exists).
3. All `@EDG` rows connected to the anchor up to the requested `depth`.
4. The neighbour atoms reached by those edges (subject to `max_rows`).

You only ever pay for the connected slice you asked for. Wide anchors or deep traversals are expensive — choose the smallest useful anchor.

## Relationship to other formats in this pack

- **TOON** (`toon-prompt-format`): best for uniform tabular data inside the prompt for the current or next step.
- **TRON** (`tron-format`): best for lists of objects that share the same property names (key repetition).
- **MemNet wire**: best when the data must be queryable later, possibly after many turns or a context reset, and when the natural shape is a graph of small facts + explicit relations.

You will often use all three in one long session:
- **Serve up:** `@CLM` type=`pipe` rows on server for pipeline steps ([sysml-memnet-pipeline.md](../../sysml-memnet-documentation/references/sysml-memnet-pipeline.md)).
- MemNet `add` to record durable atoms (`@CLM`, `@EDG`, …).
- Later: `query_warm` on the relevant `@TSK` or `@ART` to recall what was decided.
- **Serve down:** TOON/TRON for ephemeral same-turn handoff only.

## Checklist before emitting wire rows

- [ ] I have a stable id for this atom (copied from warm output or a prior add).
- [ ] The row is one indivisible fact / decision / link.
- [ ] All values are short and will still be meaningful without the surrounding chat.
- [ ] I have (or will immediately add) the necessary `@EDG` rows so the atom is reachable from useful anchors.
- [ ] The recycle policy matches the expected lifetime of the information.

Cross-references (in the user pack):
- `mcp-memnet` (tools, session lifecycle, goldfish loop)
- `mcp-memnet/references/atomisation.md` (the write discipline)
- `mcp-memnet/references/article-breakdown.md` (document → claims pattern)
- `memnet-goldfish-loop.mdc` (orchestration rule)
- `toon-prompt-format` and `tron-format` (the in-prompt siblings)

Upstream: MemNet package `LLM-GUIDE.md` and the `application-notes/` directory (especially the SysML one).