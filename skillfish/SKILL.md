---
name: skillfish
description: >-
  Guides installing, searching, syncing, and publishing Agent Skills via the
  skillfish CLI and skill.fish registry. Triggers: skill.fish, skillfish,
  npx skillfish, install skill from GitHub, skillfish.json manifest, bundle
  team skills, submit skill to registry, search community skills, sync Cursor
  skills.
metadata:
  pattern: tool-wrapper
  domain: skillfish
  version: 1.1-skillfish
---

# skill.fish / skillfish CLI

**Role:** Run the right **skillfish** commands safely; point users to **https://skill.fish** for discovery.

## Defaults

- **One-off install:** `npx skillfish add owner/repo` (installs to detected agents, including Cursor under `~/.cursor/skills/`).
- **Daily use:** `npm i -g skillfish` then `skillfish <command>`.
- **Automation / scripts:** add `--json`; use `--yes` when non-interactive. See [references/skillfish-reference.md](references/skillfish-reference.md) for exit codes and CI notes.

## When the user wants to

| Goal | Command (run from a shell; user cwd often project root) |
|------|--------------------------------------------------------|
| Install a skill from GitHub | `skillfish add owner/repo` or `npx skillfish add owner/repo` |
| Install all skills in a repo | `skillfish add owner/repo --all` |
| Search registry | `skillfish search <query>` |
| List installed | `skillfish list` (optional `--agent "Cursor"`, `--project`, `--global`) |
| Update installed | `skillfish update` or `skillfish update --yes` |
| Remove | `skillfish remove <name>` |
| Scaffold new skill | `skillfish init` or `skillfish init --name my-skill --description "..."` |
| Team manifest (create) | `skillfish bundle` -> writes `skillfish.json` |
| Team manifest (apply) | `skillfish install` (respects manifest; `--dry-run` to preview) |
| Publish to skill.fish | `skillfish submit owner/repo` or full GitHub URL (always bump `metadata.version` first if pushing changes) |

Path / sub-skill forms: `owner/repo/path/to/skill`, `owner/repo@tag`, `--path`, `--project`, `--global`, `--force` as in reference.

## Agent-specific (Cursor)

- Cursor global skills directory: **`~/.cursor/skills/`** (per skillfish upstream mapping).
- Project-local skills: use `skillfish init --project` / `skillfish add ... --project` when the user wants skills only in the repo.

## Safety (non-negotiable)

- Skills are **instructions to the agent**. Tell the user to **review** repo/source before `add` / `install`, especially third-party. skillfish does not fully vet submissions.
- Do **not** fabricate `owner/repo` or registry URLs; use what the user provides or what `skillfish search` returns.

## Version discipline for published user pack skills (MUST when editing + pushing)

- Before any `git push` that affects a published skill folder (i.e. the GitHub repo will be consumed by `skillfish add` or `submit`), always bump the `metadata.version` value in that skill's `SKILL.md` frontmatter.
- Consumers rely on version change to know an update exists; unchanged version on content change breaks update flow.
- For new skills: set an initial `version: "1.0"` (or `1.0-<slug>` per local convention).
- This rule applies to all skills under the user pack (`~/.cursor/skills/`) that back a registry entry.

## Deeper detail

- Full command flags, manifest JSON shape, non-interactive rules: [references/skillfish-reference.md](references/skillfish-reference.md).

## Pairing

- Authoring skill structure from scratch in-repo: [skill-creator](../skill-creator/SKILL.md).
