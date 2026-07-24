---
name: mcp-memnet
description: >-
  MemNet MCP — generic in-memory graph: session management, query_warm, wire-format add/update.
  For SysML v2 projects use as the modeling-relatives cache (topology, locators, reqs) via
  sysml-memnet-cache; this skill covers low-level tool mechanics. Triggers: memnet mcp, query_warm,
  session_open, wire format, sysml memnet tools.
---

# MemNet MCP (memnet server)

The `memnet` MCP provides the generic graph engine. It is the source of truth for all state. The `novel-writer` MCP is built on top of it and shares the same session.

## Core Principles

- A session lives in `memnet serve` (in-memory). It expires by TTL unless saved.
- Always pass the same `session` id on every call.
- Primary read is `query_warm` (returns LAW rows prepended + connected subgraph).
- Mutations use the `@TAG: ...` wire format via `add` or `update`.
- `session_open` + `seed_lines` is the standard way to bootstrap a new graph.
- Use `session_save` / `session_load` for persistence.

## Essential Tools

| Tool              | When to use                              | Key notes |
|-------------------|------------------------------------------|---------|
| `serve_status`    | Check if the server is running           | |
| `session_open`    | Create a new session from a tag map      | Pass `map_lines` + optional `seed_lines`. Set `allow_new_relation=true` if using custom EDG relations. |
| `session_save`    | Persist current graph to disk            | Usually `--file novel-output/.../session_snap.json` |
| `session_load`    | Resume from snapshot                     | |
| `query_warm`      | Main read for context                    | `--anchor` + `--depth`. This is what agents read most often. |
| `query_walk`      | Hop-based view (`@WALK` lines)           | Useful for traversal debugging. |
| `add` / `update`  | Write wire rows                          | `--stdin` with one or more `@TAG:...` lines. |
| `read_get`        | Fetch one specific row by id             | Authoritative reads (e.g. USR23 for pipeline stage). |
| `housekeep_stats` | Inspect row counts, caps, stale data     | |

## Typical Workflows

### Bootstrap a fresh session
1. `session_open` with `map_lines` (from Tag map) + `seed_lines`.
2. Immediately `session_save`.

### Read + mutate loop (generic)
1. `query_warm --anchor <focus>` (or the novel-writer `beat_turn_begin`).
2. Reason over the wire rows.
3. `add` or `update` with wire lines.
4. `session_save` when you want durability.

### Authoritative single-row read
Use `read_get` (especially for `USR23` in novel pipelines) because `query_warm` can be truncated.

## Important Rules

- Never call `query_warm` on memnet in the same turn as `beat_turn_begin` on novel-writer (use the presentation it returns instead).
- LAW rows are engine invariants — they are automatically prepended on warm reads.
- Sessions are cheap to open but expensive to let grow stale. Prune with housekeep when needed.
- The wire format (`@TAG: field|field|...`) is the canonical token-efficient representation.

## SysML v2 modeling (relatives cache)

**Policy skill:** [sysml-memnet-cache](../sysml-memnet-cache/SKILL.md) — MemNet is the **cache** for all SysML modeling relatives; specialist `sysml-*` skills defer here.

| Turn phase | Tool |
|------------|------|
| Preflight | `serve_status` |
| Read cache | `query_warm(anchor=TSK_model_<short>, depth=2, max_rows=50)` |
| Bootstrap project | `session_open` + `map_file` (no `@EDG` in map — fixed tag) + `seed_lines`; `allow_new_relation=true` for `owns` |
| Write delta | `add` / `update` with `@PRT`/`@SYM`/`@REQ`/… wire lines |
| Persist | `session_save` → `projects/<slug>/.memnet/<short>.snap` |
| Resume | `session_load` or `MEMNET_SESSION` in mcp.json |

Tag vocabulary and delta table: [sysml-memnet-documentation](../sysml-memnet-documentation/SKILL.md) · [relatives-cache-map.md](../sysml-memnet-documentation/references/relatives-cache-map.md).

**Do not** use chat or `AGENT-CONTEXT.md` for topology when `serve_status` is true and warm hits.

## When to Use This MCP vs novel-writer

- Use **memnet** when you need raw graph power, custom tags, SysML cache I/O, or debugging.
- Use **novel-writer** (beat_turn_begin / finish) for all story progression in a LAW-PIPE20 novel.

Always share the exact same `session` id between the two MCPs.