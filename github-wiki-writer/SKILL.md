---
name: github-wiki-writer
description: >-
  Write and publish a real GitHub Wiki: many encyclopedic pages, Home as hub
  only, `_Sidebar` with WikiLinks, then clone owner/repo.wiki.git and push.
  Use when the user asks for a GitHub wiki, write wiki, publish wiki, wiki
  pages, `_Sidebar`, WikiLinks, or wiki.git. Not GitHub Skills courses
  (https://github.com/skills). Not a stub Home, link dump, or one concatenated page.
metadata:
  pattern: pipeline
  version: "1.0"
  domain: documentation
  secondary: "hybrid: generator for pages then wiki git publish"
---

# GitHub Wiki writer

**Role:** Author a **multi-page GitHub Wiki** (operator / field handbook) and **publish** it to `owner/repo.wiki.git`. Orchestration lives here. Git steps: [references/github-wiki-git.md](references/github-wiki-git.md). Page rules: [references/core-wiki-principles.md](references/core-wiki-principles.md) and [references/page-quality.md](references/page-quality.md). Shell: [assets/page-shell.md](assets/page-shell.md).

**MUSTNOT** confuse this skill with **https://github.com/skills** (GitHub Skills **courses**).

## Pipeline

1. **Intake** -- Repo (`owner/repo`), audience, whether a **system model** exists, versioned mirror path (default `docs/wiki/` in the project git). List topics that need **their own URLs**.
2. **IA** -- One concern per page. Draft `_Sidebar` order. **Home is a hub only** (short intro + table of `[[WikiLinks]]`). **MUSTNOT** dump all topics into `Home.md`.
3. **Generate pages** -- Fill [assets/page-shell.md](assets/page-shell.md) per topic. Body **MUST** stand alone. Sources footer **MAY** cite model/paths. Pointer-only pages ("open SysML") are **not** a wiki.
4. **Truth gate** -- **MUSTNOT** invent plant topology, host roles, or port maps. If a system model exists, **the model wins** on conflict; still **explain** in wiki prose. Verify numbers against the project SSOT (a switch uplink port is an **example** of a fact to check, not a universal law).
5. **Quality** -- Apply [references/page-quality.md](references/page-quality.md). Max one revision.
6. **Mirror then publish** -- Write versioned `.md` at the repo mirror (often `docs/wiki/`). Then follow [references/github-wiki-git.md](references/github-wiki-git.md): wiki git is **unprovisioned** until someone saves the first page in the browser (`/wiki/_new`); REST/GraphQL often cannot create that first page. Copy `.md` to the wiki **root**, commit, push. Private repos: logged-out wiki URLs 404; verify with authenticated clone / `git ls-tree`.
7. **Handoff** -- Fill [assets/handoff-template.md](assets/handoff-template.md) for the user.

## MUST / MUSTNOT

| MUST | MUSTNOT |
|------|---------|
| Many pages + `_Sidebar` with `[[WikiLinks]]` | Treat a single concatenated page as a wiki |
| Home as hub only | Stub Home, link-dump Home, or all topics in Home |
| Stand-alone body on every topic page | Pointer-only pages; send readers only to SysML |
| Copy files to wiki **root** (no nested dirs) | Assume GitHub REST created the wiki git |
| Authenticated verify on private wikis | Treat a logged-out 404 as "wiki missing" without `git ls-tree` |
| Model wins; wiki still explains | Invent topology; bake one plant's ports as law |

## Pairing

SysML / deploy SSOT stays in the **project** model and rules. This skill publishes the handbook; it does not become a second architecture.

## Install path

User pack: `~/.cursor/skills/github-wiki-writer/`. Initial `metadata.version` is `1.0`. Bump version before any git push of this pack (skillfish consumers). Do not `skillfish submit` unless the user names a public `owner/repo`.
