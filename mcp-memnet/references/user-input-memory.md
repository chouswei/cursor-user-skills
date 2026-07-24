# MemNet for user input and preferences

When the agent **must recall what the user said** across turns — atomise each constraint as its own **`@USR`** row (one fact, short `content` field), link to `@TSK` via `@EDG`. See [atomisation.md](atomisation.md), [wire-format.md](wire-format.md).

MemNet is **not** a chat log. Store **distilled atoms**, not messages.

## When to write user input to MemNet

| User said | Store? | Example |
|-----------|--------|---------|
| Hard constraint ("never force push", "British English") | **Yes** — `@USR`, `persistent` | `USR_no_force|git|never force push main|active|persistent` |
| Scope decision ("only touch MCP files") | **Yes** — link to `@TSK` via `@EDG` | |
| One-off clarification for this message only | **No** — act immediately | |
| Preference that affects many turns | **Yes** | `USR_style|prose|concise technical blog|active|persistent` |
| Pipeline input (step 3 in orchestrator loops) | **Yes** — `@USR` or domain tag + `@EDG` to `@TSK` | |

**Rule:** If forgetting it in 5 turns would cause wrong behaviour → **`add` `@USR`** after the user message.

## Tag map (add to session_open map_lines)

General-purpose (coding + pipelines):

```text
@USR: id|topic|content|status|recycle
@TSK: id|goal|deadline|status|recycle
@EDG: id|from|rel|to|note|recycle
```

| Field | Use |
|-------|-----|
| `topic` | Short key: `git`, `scope`, `style`, `decision`, `requirement` |
| `content` | Distilled fact — short phrase, not a paragraph |
| `status` | `active` while in force; `superseded` when user changes mind |
| `recycle` | `persistent` for long-lived prefs; `delete_on_settle` for step-local input |

This general map uses `topic|content|status` for coding/pipeline sessions. Prefer Tier A shapes when mutating via MCP (`add`/`update`).

Cross-ref: [atomisation.md](atomisation.md) · [coding-memory.md](coding-memory.md) · [mcp-policy.md](mcp-policy.md)

## MCP examples

### Capture user constraint at start of task

```json
add(wire_lines=[
  "@TSK: TSK_current|Implement MCP docs|1|in_progress|persistent",
  "@USR: USR_scope|files|only src/memnet_mcp and docs|active|persistent",
  "@USR: USR_lang|style|British English in replies|active|persistent",
  "@EDG: E01|TSK_current|constrained_by|USR_scope|user stated|persistent",
  "@EDG: E02|TSK_current|constrained_by|USR_lang|user stated|persistent"
])
```

### Next turn — recall before acting

```json
query_warm(anchor="TSK_current", depth=2)
```

Warm slice includes `@USR` rows linked to the task.

### User changes mind

```json
update(wire_lines=[
  "@USR: USR_scope|files|memnet repo only, no user-pack edits|active|persistent"
])
```

Same id — **update**, not add.

## Anchors

| Anchor | Recalls |
|--------|---------|
| `TSK_*` | Task + linked `@USR` constraints |
| `USR_*` | Single preference + edges to tasks |

## vs chat history

| Chat history | MemNet `@USR` |
|--------------|---------------|
| May scroll away | Stays until settled or updated |
| Mixed with agent text | User-sourced facts only |
| Hard to query by task | `query_warm` from `@TSK` pulls relevant `@USR` |

## Pair with goldfish loop

Each turn: **`query_warm`** first (includes user constraints) → act → **`add`/`update`** if the user said something new that must persist.

Cross-ref: [atomisation.md](atomisation.md) · [coding-memory.md](coding-memory.md) · [mcp-policy.md](mcp-policy.md)
