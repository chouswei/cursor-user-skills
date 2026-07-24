# Cursor basement (required)

This skill targets **Cursor** as the IDE for vibe coding. Scaffold **project-local** Cursor files. Global user-pack skills remain in `~/.cursor/skills/`; the repo still **must** have `.cursor/skills/` for project skills.

## Always create

```text
AGENTS.md                 # repo purpose, type code(s), build/run, Agent do/don't
.cursor/rules/            # 1 thin alwaysApply or glob rule (build/run/board only)
.cursor/skills/           # REQUIRED — project skill pack (at least a stub)
.cursorignore             # optional: build/, .pio/, node_modules/, large SDKs
```

### `AGENTS.md` minimum

1. One-line purpose + type code(s)  
2. How to build / flash / run  
3. Agent constraints (no secrets; basement vs features; board TBD rules)  
4. Skills: project `.cursor/skills/` + global `~/.cursor/skills/` (do not dump the whole user pack into the repo)

### `.cursor/rules/`

- **One** project `.mdc`, under ~40 lines, precise  
- Prefer `globs` for language files when useful; else `alwaysApply: true` for board/run only  
- Do not copy the full user-pack rule set into the repo

### `.cursor/skills/` (required)

- **Must exist** after scaffold (empty pack is not enough — include a minimal project skill or README stub that states the pack is intentional)
- Default basement: one thin project skill, e.g. `.cursor/skills/repo-context/SKILL.md` — purpose, type code(s), build/run, non-goals (orchestration only; no feature logic)
- Add further project skills only when the domain needs them
- **Do not** copy the entire `~/.cursor/skills/` user pack into the repo
- Point `AGENTS.md` at both project and user-pack skill roots

### Do not create unless asked

- `.vscode/` as the primary IDE story (Cursor can read it; do not present VS Code as the target)
- Copilot / JetBrains / Windsurf-specific configs

## Optional

| Path | When |
|------|------|
| `.cursor/rules/<lang>.mdc` | Extra language globs after first rule exists |
| `.cursor/skills/<id>/` | Extra project skills beyond `repo-context` |
| `.memnet/` | MemNet session snaps for this repo |
| `tasks/lessons.md` | If user wants a lessons file |

## Hybrid

Root owns `AGENTS.md` + `.cursor/` (including `.cursor/skills/`); slices do not each get a full Cursor tree unless the user wants monorepo-per-slice agents.
