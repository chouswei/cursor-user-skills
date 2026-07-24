---
name: memnet-codebase-snap
description: >-
  MemNet-powered snapshot and durable index of a C (or C-like) codebase.
  - Files/modules as @MOD nodes.
  - Functions, variables (gvar/var), defines, structs, enums as first-class @SYM nodes.
  - Relations (defines, calls, includes, owns, uses/reads/writes, constrained_by, etc.) as @EDG edges.
  Supports full initial snap of files + symbols + key relations, plus incremental re-snap.
  Enables low-token queries such as "where is X defined", "who calls Y", "what touches this ring buffer".
  Use for firmware/embedded work when the user asks for snap, memnet index, symbol graph, or "remember the functions and call structure".
  Primary example: weftTree Pico 2 + SIM7600 + IIS2ICLX.
metadata:
  pattern: pipeline
  version: "0.3"
---

# MemNet Codebase Snap

**Shared dialect only** (Write = display) for `add`/`update`. See [memnet-format](../memnet-format/SKILL.md) and [coding-memory](../mcp-memnet/references/coding-memory.md).

**Role:** Provide a repeatable, verifiable procedure to atomise an entire source tree (or delta) into MemNet:
- MOD nodes for files
- SYM nodes for functions and variables (and other symbols)
- Edges for defines, calls, includes, uses, ownership and other relations

This gives fast, low-token navigation ("where is this fn/variable defined?", "who calls it?", "what state does this path touch?").

**Always pair with truth on disk:** Grep (ripgrep), Glob, Read, SemanticSearch first -- then `add`/`update` only confirmed facts.

## Before acting

1. Read the authoritative project guide if present: `AGENTS.md` (PAT) or equivalent.
2. Ensure the MemNet MCP is usable: `serve_status`; start `memnet serve` only if using TCP.
3. Read the tool schema for every MemNet tool before first `CallMcpTool` in a session.
4. Read once per significant snap session: `mcp-memnet` (coding-memory, atomisation) and `memnet-format`.
5. Open (or reuse) a session via `session_open`.
6. Never invent ids -- copy from prior pin map or the first `add` response.

## Core kinds (coding memory)

MOD and SYM are **nodes**. Directed **edges** connect them (and TSK/USR).

| Kind | Typical fields | Notes |
|------|----------------|-------|
| MOD | path, lang, role, loc, recycle | one per `.c`/`.h`; lang=c\|cpp\|h; role=driver\|app\|hal\|calc\|uart\|mqtt\|platform |
| SYM | name, kind, path, line, sig, vis, recycle | kind=fn\|isr\|var\|gvar\|define\|macro\|struct\|enum\|typedef\|const |
| TSK | goal, phase, status, recycle | owning task; hang atoms via owns edges |
| Edge | --(rel)--> + note, recycle | defines, declares, includes, calls, implements, owns, uses, reads, writes, constrained_by, related |

Mutate sketch:

```text
## Nodes
+ MOD [NEW] ; path=src/i2c/iis2iclx_data_calc.c ; lang=c ; role=calc ; loc=~870 ; recycle=persistent
+ SYM [NEW] ; name=iis2iclx_calc_push_sample ; kind=fn ; path=src/i2c/iis2iclx_data_calc.c ; line=108 ; recycle=persistent
+ TSK [NEW] ; goal=Full structural index ; status=in_progress ; recycle=persistent

## Edges
+ E01 [NEW] --(defines)--> [SYM_iis2iclx_calc_push_sample] ; note=impl ; recycle=persistent
```

Stable id rules:
- Module: `MOD_` + path with `/` and `.` -> `_`
- Symbol: `SYM_` + short unique slug
- Edge: `E` + slug; copy ids from pin map / add response
- Task: `TSK_` + short descriptive

Recycle: `persistent` for structural facts; `delete_on_settle` for investigation scratch.


## Snap workflow (initial full or targeted)

1. `serve_status` → confirm OK.
2. `session_open` (once) supplying the tag map above (plus any project @USR seeds). Capture returned session id if given.
3. `query_warm` on a broad but useful anchor (e.g. an existing `TSK_codebase_snap_*` or a top-level `MOD_`) to see what is already known. Never assume the graph is empty.
4. Enumerate targets with `Glob`:
   - C/H focus: `src/**/*.c`, `src/**/*.h`, `include/**/*.h`, `lib/**/ads127*.h`
   - Supporting: `scripts/**/*`, `tools/**/*`, `docs/**/*.md`, `examples/**/README.md`, `.cursor/skills/**/*.md`, `.cursor/rules/**/*.mdc`
5. For each file (batch in mind; do not flood one turn):
   - `Read` the file (or sections via offset/limit for large ones).
   - Extract **nodes** with `Grep` (path-scoped):
     - Function definitions (nodes of kind=fn): `^\s*(static\s+)?(inline\s+)?\w+\s+\**?\w+\s*\(`
     - ISRs / weak handlers: `IRQHandler|Handler\s*\(`
     - Important variables (nodes of kind=gvar|var): file-scope `^\s*(static|volatile|extern)\s+` and key locals that form the architecture (rings, state machines, thresholds).
     - Public #defines / macros (kind=define): `^#define\s+[A-Z0-9_]+`
     - Struct/enum/typedef at file scope (kind=struct|enum|typedef).
   - Note `#include` lines → candidate `includes` edges.
   - Derive one `@MOD` (node) + N `@SYM` (nodes) rows. Keep `sig` short (prototype head or `...`).
   - Verify on disk before emitting.
6. `add` (preferred) or `update` with a large `wire_lines` array (mix of @MOD/@SYM + @EDG). 30–80 atoms comfortably.
7. After the batch: `query_warm(anchor="TSK_...", depth=1 or 2, max_rows=80)` to confirm and obtain ids.
8. **Mark relations with @EDG edges** (this is core to the snap, not optional afterthought):
   - From the same file: `defines` (MOD → SYM, or SYM → SYM for nested), `owns`, `declares`.
   - Cross-file: `includes` (from #include), `calls` (verified call sites: caller SYM calls callee SYM).
   - Data: `uses`, `reads`, `writes`, `touches` for important gvar access across modules.
   - Architecture: `binds`, `constrained_by` where relevant.
   - Always emit at least the ownership (`TSK owns MOD`, `MOD defines SYM`) and the main control-flow / data-flow edges for the architecture (e.g. outer tick → mqtt service → calc service → push_sample path).
   - Full exhaustive call-graph is expensive; focus on the primary execution paths and shared state during the initial snap. Add more targeted call edges on subsequent passes when the work needs them.
   - Use `query_walk` or narrow `query_warm` on a SYM to discover existing neighbours before adding duplicate edges.
9. `housekeep_stats` periodically; settle finished `@TSK` phases with `update` + `delete_on_settle` so warm slices stay small.
10. Record any project conventions discovered as `@USR` atoms (e.g. "periodic burst uses 6 s TX quiesce").

## Capturing the symbol relation graph (edges between nodes)

Functions and variables are **@SYM nodes**. Relations are **@EDG edges** that make the graph queryable.

During the main snap:
- For every significant function @SYM, record the `defines` edge from its @MOD (or from another SYM if it is a static helper).
- For the main execution skeleton, add `calls` edges (and reverse `called_from` when helpful for warm slices):
  - Example: `app_services_inner_tick` calls `iis2iclx_calc_service`
  - Example: `core1_accel_worker` calls `iis2iclx_calc_push_sample`
- For shared state (rings, flags, thresholds stored as gvar @SYM), add `uses` / `reads` / `writes` / `touches` from the modules or functions that access them.
- Record `includes` for the import structure.
- Use `binds` for registration / hook patterns (e.g. coop hook, accel binding).
- Keep edges sparse but architecturally meaningful. The goal is to answer "what calls this", "what touches this buffer", "what is the control flow" via `query_warm(anchor=SYM_..., depth=1..2)` or `query_walk`.

Discovery tips (always verify on disk):
- After you have a list of public function names, `Grep` for `\<name\>\s*\(` (word boundary + call) excluding the definition line itself.
- For variables, `Grep` the bare name (with context) in other translation units.
- For each candidate edge, do a narrow `Read` of the call site or use site before writing the @EDG row.

## Incremental / edit-time snap

When the user edits a file (or you propose an edit):
- `query_warm` anchored on the `MOD_<that_file>` (or the owning `TSK`).
- Re-`Grep` + `Read` only the changed file (or the diff hunks).
- `update` the affected `@SYM` rows (line numbers, signatures) and any new/deleted symbols. @SYM are nodes — keep them current.
- Emit or update `@EDG` for changed or new relations (calls added/removed, variable access changed, etc.). Verify first.
- Never duplicate ids; `update` mutates in place.

After a multi-file refactor: re-snap the modified `MOD`s + their @SYM nodes, then walk the `includes` / `calls` / `uses` edges and spot-check / repair them.

## PAT Nucleo firmware examples (apply the same pattern everywhere)

| intent | anchor | action | notes |
|--------|--------|--------|-------|
| First time full index of quartet path | `TSK_codebase_snap_pat` (create if absent) | Glob + Grep; add `@MOD` nodes + `@SYM` nodes (fns + key gvars) for the quartet files; add `defines` + main `calls` edges | also capture important compile-time knobs as `@SYM` (`kind=define`) or `@USR` |
| Locate the blocking quartet read after context reset | `query_warm(anchor=SYM_ads127_read_quartet_blocking, depth=2)` | returns the defining `@MOD` node, callers via `calls` `@EDG` edges, and related `@TSK` | if absent, Grep → add the `@SYM` node then the call edges |
| Track a pin role change on 86ex5v90x HAT | `query_warm(anchor=MOD_...)` then Grep pins | update `@SYM` nodes for the pins/config; add or repair `@EDG` `constrained_by` or `uses` | cross-ref project docs |
| Remember the control flow that touches a shared ring | add `@SYM` nodes for the ring buffer + the push / pop / service functions; connect with `calls` + `uses` `@EDG` | `query_warm` on the gvar or on the service fn to see the graph neighbourhood | this is exactly what `@SYM` nodes + `@EDG` edges enable |
## Verification and quality rules (non-negotiable)

- Every atom (@MOD node, @SYM node for fn/var/..., or @EDG edge) must be reproducible from a `Grep` or `Read` performed in the same or immediate prior turn.
- `sig` and `note` are short (prototype head, short code). No prose blobs.
- One fact / one node / one directed edge per row. Use extra @EDG rows for multiple relations.
- After any substantial `add`/`update`, run a narrow `query_warm` (on the new @SYM node or @EDG) and spot-check a few @SYM signatures + a couple of @EDG relations against the actual source lines.
- Prefer `update` for existing ids.
- Run `housekeep_stats` when warned; settle transient @TSK work.
- Only persist facts that affect runtime or build behaviour (skip pure compile-time generated noise unless checked in).

## Common anchors during development

- `TSK_*` — owns the @MOD and @SYM nodes for the current mission
- `MOD_<file>` — the file node + its defined @SYM nodes (functions and variables)
- `SYM_<name>` — a function or variable **node**; warm read gives its @MOD plus connected @EDG neighbours (who calls it, what it calls, what state it touches)

Increase `depth` only when you need the extra hop; always cap with `max_rows`. Use `query_walk` when you want the hop list instead of full rows.

## Related skills and references (read as needed)

- `mcp-memnet` (tool usage, goldfish loop, coding-memory.md, atomisation.md)
- `memnet-format` (exact wire grammar, escaping, recycle policies)
- Plain Markdown tables for in-turn handoffs before/after MCP calls (not TOON/TRON)
- PAT-specific: `four-channel-spi-ads127-quartet`, `ads127l11-registers`, `stm32cube-cmake-pat`, `deterministic-cooperative-loop`, AGENTS.md, the various .cursor/rules/*.mdc

## Quick start checklist for a new snap session

- [ ] `serve_status` OK
- [ ] `session_open` with tag map (once); @MOD/@SYM are nodes, @EDG are edges
- [ ] `query_warm` on TSK or a root @MOD to see prior state
- [ ] Glob + Grep plan (functions + variables as @SYM nodes; calls/uses/includes as @EDG)
- [ ] Verify on disk → emit nodes + edges in `add`/`update`
- [ ] `query_warm` + spot `Read` to confirm both @SYM signatures and @EDG relations
- [ ] `housekeep_stats`; settle finished @TSK phases

Use this skill when you need a durable, queryable index of the **functions and variables (as nodes)** and their **call / data / ownership relations (as edges)** across context resets.
