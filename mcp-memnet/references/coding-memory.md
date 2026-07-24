# MemNet for coding memory

Use MemNet when the agent must **remember where things are across turns** — function locations, modules touched, refactor plans — without stuffing paths into chat history.

**Full application note:** when MemNet is the workspace, see `application-notes/llm-software-development.md` (v0.2.12 `session_load`/`session_save` retrospective, `@USR`/`@DEC`, LAW-CODE01–04).

**Atomise first:** one `@MOD` per file, one `@SYM` per symbol, edges for relationships — see [atomisation.md](atomisation.md). Use **short pipe fields** only ([wire-format.md](wire-format.md)).

MemNet is **agent-maintained index + task graph**, not a substitute for `grep`, LSP, or semantic search. **Verify** on disk; **store** confirmed atoms. Cursor codebase indexing finds code; MemNet remembers task state and verified conclusions.

## When to use (coding)

| Situation | Use MemNet? |
|-----------|-------------|
| Multi-file refactor spanning many chat turns | **Yes** — anchor on `@TSK` or `@MOD` |
| “Where is `send_command`?” after you already found it once | **Yes** — `@SYM` row + warm read |
| Tracking files/modules touched for current task | **Yes** — `@MOD` + `@EDG` |
| User-stated API/style constraints | **Yes** — `@USR` + `constrained_by` from `@TSK` |
| Open design fork (default value, naming) | **Yes** — `@DEC`; settle with `chosen` |
| One-shot symbol lookup, never referenced again | **No** — grep / Go to definition |
| Authoritative “what calls X?” | **No** — ripgrep / LSP first; optionally **add** `@EDG` after you verify |

**Open a coding session** at the start of a non-trivial task (or when the user says “remember where things are”). One session per repo/task is enough; reuse ids. Use `session_save` / `session_load` for multi-day work.

## Tag map (session_open map_lines)

```text
@CFG: id|repo|anchor|version|notes
@MOD: id|path|summary|status|recycle
@SYM: id|name|kind|path|line|signature|status|recycle
@TSK: id|goal|anchor|status|recycle
@USR: id|topic|content|status|recycle
@DEC: id|task|question|options|chosen|recycle
@EDG: id|from|rel|to|note|recycle
```

| Tag | Purpose |
|-----|---------|
| `@CFG` | Repo root; `anchor` = synthetic `MOD_repo_root` |
| `@MOD` | File or package (repo-relative path) |
| `@SYM` | Function, class, method, constant (`kind`: fn, class, method, …) |
| `@TSK` | Active coding mission; `anchor` = warm-from `@MOD` or `@SYM` |
| `@USR` | User constraints (`topic`: scope, style, api) — see [user-input-memory.md](user-input-memory.md) |
| `@DEC` | Open fork; settle with `chosen` + `delete_on_settle` |
| `@EDG` | `imports`, `calls`, `tests`, `implements`, `owns`, `constrained_by`, `related` |

## ID conventions

Stable, human-readable, **global per session**:

| Entity | ID pattern | Example |
|--------|------------|---------|
| Module | `MOD_` + slug from path | `MOD_mcp_server` → `src/memnet_mcp/server.py` |
| Symbol | `SYM_` + layer prefix | `SYM_cli_session_load`, `SYM_mcp_session_load` |
| Task | `TSK_` + short name | `TSK_mcp_session_load` |
| User constraint | `USR_` + topic slug | `USR_keep_id` |
| Decision | `DEC_` + slug | `DEC_mcp_keep_id` |
| Edge | `E` + slug or number | `E_mcp_impl_load` |

Copy ids from warm output — never retype from memory.

## Goldfish loop (coding)

1. **`query_warm`** anchor = current `@TSK` id (or `@MOD` / `@SYM` if task unset).
2. **grep/LSP** if you need fresh truth on disk.
3. **`add`** new `@MOD` / `@SYM` / `@USR` / `@DEC` / `@EDG` rows; **`update`** when path/line/signature changes or task status moves.
4. **`session_save`** after substantive turns (multi-day work).
5. **`update`** task to `done` + `recycle=delete_on_settle` when finished.

## MCP examples

### Open coding session

```json
session_open(map_lines=[
  "@CFG: id|repo|anchor|version|notes",
  "@MOD: id|path|summary|status|recycle",
  "@SYM: id|name|kind|path|line|signature|status|recycle",
  "@TSK: id|goal|anchor|status|recycle",
  "@USR: id|topic|content|status|recycle",
  "@DEC: id|task|question|options|chosen|recycle",
  "@EDG: id|from|rel|to|note|recycle"
])
```

### Start task + record a function you found

```json
add(wire_lines=[
  "@TSK: TSK_mcp_session_load|Expose session_load on memnet-mcp|MOD_cli|in_progress|persistent",
  "@MOD: MOD_cli|src/memnet/cli.py|Typer CLI session commands|active|persistent",
  "@SYM: SYM_cli_session_load|session_load|fn|src/memnet/cli.py|351|def session_load(...)|active|persistent",
  "@USR: USR_keep_id|api|keep_id default true on session_load|active|persistent",
  "@DEC: DEC_mcp_keep_id|TSK_mcp_session_load|keep_id default|true / false||persistent",
  "@EDG: E01|TSK_mcp_session_load|owns|MOD_cli|task scope|persistent",
  "@EDG: E02|MOD_cli|defines|SYM_cli_session_load|handler|persistent",
  "@EDG: E03|TSK_mcp_session_load|constrained_by|USR_keep_id|user stated|persistent"
])
```

### Settle decision + task

```json
update(wire_lines=[
  "@DEC: DEC_mcp_keep_id|TSK_mcp_session_load|keep_id default|true / false|true|delete_on_settle",
  "@TSK: TSK_mcp_session_load|Expose session_load on memnet-mcp|MOD_cli|done|delete_on_settle"
])
```

### Next turn — where is that function?

```json
query_warm(anchor="TSK_mcp_session_load", depth=2)
```

Returns `@LAW:` + connected `@TSK`, `@MOD`, `@SYM`, `@USR`, `@DEC`, `@EDG` — small slice, not the whole repo.

### File moved after refactor

```json
update(wire_lines=[
  "@SYM: SYM_cli_session_load|session_load|fn|src/memnet/cli.py|352|def session_load(...)|active|persistent"
])
```

## Anchors to prefer

| Anchor | Warm slice |
|--------|------------|
| `TSK_*` | Task + owned modules/symbols/decisions/constraints |
| `MOD_*` | File + symbols defined there + callers (via `@EDG`) |
| `SYM_*` | Symbol + module + call graph neighbours |
| `MOD_repo_root` | CFG anchor — repo context |

## Limits

- Rows are **not** auto-synced from git — **update** after moves/renames.
- Do not store whole files — store **path, line, short signature, summary**.
- Prefer **one `@TSK` in_progress** per session; settle before starting unrelated work.
- `@WRN` on stderr — respect cap warnings; run `housekeep_stats` if rows grow.

## Pair with codebase tools

```text
Turn N:   query_warm(TSK) → grep/LSP → add/update MOD/SYM
Turn N+1: query_warm(TSK) → edit file → update SYM line if shifted
```

Do not skip verification on the first discovery turn; MemNet remembers **confirmed** atoms.

Cross-ref: [atomisation.md](atomisation.md) · [mcp-policy.md](mcp-policy.md) · [user-input-memory.md](user-input-memory.md)
