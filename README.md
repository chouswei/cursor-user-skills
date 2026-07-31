# Cursor user skills pack

Personal **Cursor Agent Skills** pack for syncing across devices.

On this machine the live path is:

- **Windows:** `%USERPROFILE%\.cursor\skills`
- **macOS / Linux:** `~/.cursor/skills`

Clone or pull this repository **into that directory** so Cursor can load the skills globally (all workspaces).

## Sync on another device

**First setup (empty skills folder or new machine):**

```bash
# Ensure parent exists
mkdir -p ~/.cursor
# Clone into skills (folder must not already exist as a non-empty non-git dir)
git clone git@github.com:chouswei/cursor-user-skills.git ~/.cursor/skills
# or HTTPS:
# git clone https://github.com/chouswei/cursor-user-skills.git ~/.cursor/skills
```

**Windows (PowerShell), if the folder already exists and is empty:**

```powershell
git clone https://github.com/chouswei/cursor-user-skills.git "$env:USERPROFILE\.cursor\skills"
```

**If skills already exist and you only need updates:**

```bash
cd ~/.cursor/skills   # or %USERPROFILE%\.cursor\skills
git pull
```

If the folder already has content and is not a git clone of this repo, back it up, then either `git init` + add this remote, or replace with a fresh clone.

## What this is

- One repo for the whole personal user-pack under `.cursor/skills/`.
- Includes meta tooling (e.g. **skillfish**, **skill-creator**) and domain skills.
- Some skills are marked **deprecated** in their `SKILL.md` (e.g. TOON/TRON, novel-writer, merged SysML stubs); keep them for trigger resolution, but follow the survivor skill they point to.
- MemNet agent I/O: **shared dialect** only (`memnet-format` + `mcp-memnet`). Do not teach pipe `@TAG` rows as agent format.
- Sub-agents: role->slug in `rules/sub-agent-policy.mdc` (unclear/thinking -> `cursor-grok-4.5-low` never FAST; visual items review -> `kimi-k3-max`; MemNet snapshot -> `gpt-5.6-luna-medium`; clear-step routines -> `composer-2.5`; never `*-fast`).


## Maintain

- Edit skills locally, then `git add` / `git commit --trailer "Co-authored-by: Cursor <cursoragent@cursor.com>"` / `git push`.
- Before publishing individual skills to skill.fish, bump `metadata.version` in that skill's frontmatter (see **skillfish**).
- Do not commit secrets, `.env`, `node_modules`, or `__pycache__`.

## Related

- Project-local skills stay in each repo under `.cursor/skills/` and are **not** this pack.
- Cursor also has built-in skills under `~/.cursor/skills-cursor/` (separate; not in this repo).
- **User rules (IDE-loaded):** live under `~/.cursor/rules/` (Windows: `%USERPROFILE%\.cursor\rules\`). This pack keeps copies in `rules/` for sync — on a new machine, copy or symlink `rules/*.mdc` into `~/.cursor/rules/` after clone/pull.
