---
name: mcp-novel-writer
description: Use the novel-writer MCP for structured interactive novel writing. Provides beat_turn_begin / beat_turn_finish (the two-call pipeline) and bootstrap_from_seed. Follows LAW-PIPE20 (OLN → SBD → SCR → prose with optional no_bundle strict mode). Always use this for story progression instead of raw memnet calls.
---

# Novel Writer MCP

This MCP is the orchestrator for interactive novels on top of a MemNet graph. It enforces the 4-stage pipeline and presentation contracts defined in the seed.

## The Contract

One player story beat = 1 to 4 micro-cycles (depending on `no_bundle`).

With `LAW-PIPE20 no_bundle` (recommended for quality):

```
beat_stage=oln   → beat_turn_begin → draft @OLN → beat_turn_finish(oln_lines only) → sbd
beat_stage=sbd   → beat_turn_begin → draft @SBD → beat_turn_finish(sbd_lines only) → scr
beat_stage=scr   → beat_turn_begin → draft @SCR → beat_turn_finish(scr_lines only) → prose
beat_stage=prose → beat_turn_begin → draft prose → beat_turn_finish(prose + option_lines + updates) → oln + STEP.n+1
```

Only the final `prose` turn usually returns visible story + options to the player.

## Essential Tools

- `bootstrap_from_seed(md_path)` — Open a session from an `application-notes/*-initial-state.md`. Preferred for starting fresh stories.
- `beat_turn_begin(session)` — Returns `pipeline`, `presentation`, and `writing_contract`. This is the main context for the current micro-turn.
- `beat_turn_finish(session, ...)` — The single atomic commit tool. Pass only the data appropriate for the current stage.

### Key beat_turn_finish parameters (use the right ones)

| Current stage | What to send on finish                  | Notes |
|---------------|-----------------------------------------|-------|
| `oln`         | `oln_lines=[...]`                       | Only the @OLN wire |
| `sbd`         | `sbd_lines=[...]`                       | Only the @SBD wire |
| `scr`         | `scr_lines=[...]`                       | Only the @SCR wire |
| `prose`       | `prose=...`, `option_lines=[...]`, `update_lines=[STEP, SYS, PLR, ...]` | Full narrative turn |

Additional useful flags:
- `since_modified` — Pass the value from the previous `beat_turn_begin.session_modified` to detect concurrent changes.
- `option_lines` — Validated 1–6 options (only on prose turns).
- `pipeline_bypass` — Only for legacy / special paths (tests, ledger, library).

## Recommended Workflow (per micro-cycle)

1. Call `beat_turn_begin(session=...)`.
2. Read `pipeline.beat_stage` and `presentation.contracts[0]` (the stage hint).
3. Draft only what the current stage allows (see LAW-PIPE20 in seed).
4. Call `beat_turn_finish` with the matching `*_lines` parameter (and nothing else for intermediate stages).
5. On the final prose turn, also provide `prose`, `option_lines`, and necessary `update_lines`.
6. After a successful prose turn, consider `session_save`.

## Critical Rules (LAW-PIPE20 + no_bundle)

- Never send multiple wire types in one `beat_turn_finish` when `no_bundle` is active.
- Do not write chapter prose before `beat_turn_finish` returns `exit_code=0`.
- Prefer `presentation` returned by `beat_turn_begin` over raw `warm_stdout`.
- The same `session` id must be used for both `memnet` and `novel-writer` MCPs.
- `USR23|beat_stage` is the source of truth for the current micro-stage (read via `read_get` inside the pipeline for reliability).

## Bootstrap

Use `bootstrap_from_seed` with the path to the active `application-notes/*-initial-state.md`.

After bootstrap:
- Immediately do a `beat_turn_begin`.
- Check `pipeline.pc_name_unset` or `USR03` if the player name still needs to be set.

## Common Patterns

### First beat (awakening)
- `beat_turn_begin`
- Write `@OLN` → `finish(oln_lines)`
- Write `@SBD` → `finish(sbd_lines)`
- Write `@SCR` → `finish(scr_lines)`
- Write prose + first options + STEP update → `finish(...)`
- `session_save`

### Normal story beat
Follow the stage machine strictly. Only the last micro-cycle returns visible prose + options.

### Library or ledger turns
These are often `no_time_advance` and may use `pipeline_bypass` or special handling. Check the seed USR30/OPT01–03.

## Anti-Patterns

- Calling `query_warm` directly on the memnet MCP during a novel turn (use `beat_turn_begin` instead).
- Sending `prose` on an `oln`/`sbd`/`scr` turn.
- Bundling all four stages in one finish when `no_bundle` is on.
- Forgetting to advance `STEP` and other state only on the prose turn.
- Using deprecated tools (`prose_metrics`, `beat_prose_finalize`, etc.).

## Relationship to memnet MCP

`novel-writer` is a thick orchestrator. It still talks to the same MemNet store via the memnet MCP under the hood. Use `memnet` tools only when you need raw access (debugging, custom tags, housekeep). All narrative progression should go through `beat_turn_begin` + `beat_turn_finish`.