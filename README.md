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
- Some skills are marked **deprecated** in their `SKILL.md` (e.g. TOON/TRON); keep them for trigger resolution, but do not use them for new encoding advice.

## Maintain

- Edit skills locally, then `git add` / `git commit --trailer "Co-authored-by: Cursor <cursoragent@cursor.com>"` / `git push`.
- Before publishing individual skills to skill.fish, bump `metadata.version` in that skill's frontmatter (see **skillfish**).
- Do not commit secrets, `.env`, `node_modules`, or `__pycache__`.

## Related

- Project-local skills stay in each repo under `.cursor/skills/` and are **not** this pack.
- Cursor also has built-in skills under `~/.cursor/skills-cursor/` (separate; not in this repo).
