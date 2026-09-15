---
name: skill-graph-workflow
description: >-
  Bind and maintain skill graphs: pack seed vs the open repo seed. Repo graph
  holds project SKL; pack graph holds pack SKL; repo rows MAY point at pack
  skill ids as relatives. Triggers: skill graph, repo skill graph, relative
  skills, skill-graph-seed.wire, SKG_repo, bind which graph. Skip: domain
  SysML/PCBA/report work (open that skill); inventing repo SKL in the pack seed.
metadata:
  pattern: pipeline
  version: "1.0"
  domain: meta
  secondary: "hybrid: bind graph, then one relative (selector / creator / reviewer / skillfish)"
  pairs_with: [reasoning-strategy-selector, skill-creator, skill-reviewer, skillfish, vibe-repo-init]
token_guardrails: |
  - Bind one graph per turn. MUST NOT merge repo SKL into the pack seed.
  - Membership: pack SKL from pack seed; repo SKL from repo seed. Pointer SKL rows (pack=user, path under ~/.cursor/skills/) are relatives, not copies of bodies.
  - One relative skill after bind. MUST NOT paste sibling SKILL.md bodies.
  - Load references/bind-graph.md when the live path or SKG id is unclear.
pipeline_steps:
  1. Bind graph
     - Live repo seed: <repo>/.cursor/skills/skill-graph-seed.wire (SKG_repo unless the file names another id).
     - Pack seed: ~/.cursor/skills/reasoning-strategy-selector/references/skill-graph-seed.wire (SKG_global is pack-scoped).
     - Fill assets/bind-handoff.md.
  2. Route or maintain
     - Route pack skills: ../reasoning-strategy-selector/SKILL.md
     - New pack or repo skill folder: ../skill-creator/SKILL.md
     - Audit a skill folder: ../skill-reviewer/SKILL.md
     - Registry install/submit: ../skillfish/SKILL.md
     - Greenfield repo seed: ../vibe-repo-init/SKILL.md then copy assets/repo-skill-graph-seed.wire
  3. Seed edit
     - Same GQL CREATE shape. Density: >=2 TRG and >=1 typed rel per SKL (skill-graph.md).
     - Repo COMPLEMENTS/PRECEDES pack ids: add a thin pack=user SKL pointer, do not duplicate the pack body.
  4. Validate
     - Pack: python tools/validate_selector_pack.py --check-views from reasoning-strategy-selector.
     - Repo: parse the repo wire; refuse pack-seed --write of repo scans.
  5. Self-check
     - Which graph; no merge; relatives are edges or pointer SKL rows.
system_instruction: |
  Concise British English. ASCII. Pack graph is pack skills; each repo has its own graph.
  Bind first. One relative skill after. JSON only at tool boundaries.
---

# Skill-graph relatives

**When:** Bind, route, or edit a **skill graph**. Pack owns the graph **tooling** cluster. Each open repo owns **its** seed.

**Not:** Solving SysML, PCBA, or report tasks. Open that domain skill. Not a dump of every pack SKL into a repo seed.

## Two graphs

| Graph | Seed | SKG id | Owns |
|-------|------|--------|------|
| Pack | `~/.cursor/skills/reasoning-strategy-selector/references/skill-graph-seed.wire` | `SKG_global` (pack-scoped) | User-pack SKL |
| Repo | `<repo>/.cursor/skills/skill-graph-seed.wire` | `SKG_repo` (or id in that file) | Project SKL |

Hub rules: [SKILL-GRAPH.md](../SKILL-GRAPH.md). Schema: [skill-graph.md](../reasoning-strategy-selector/references/skill-graph.md). Bind detail: [references/bind-graph.md](references/bind-graph.md).

## Relatives (one per turn after bind)

| Skill | When |
|-------|------|
| [reasoning-strategy-selector](../reasoning-strategy-selector/SKILL.md) | Which **pack** skill; explicit multi-match |
| [skill-creator](../skill-creator/SKILL.md) | New `SKILL.md` folder |
| [skill-reviewer](../skill-reviewer/SKILL.md) | Audit a skill package |
| [skillfish](../skillfish/SKILL.md) | Install / submit / bundle |
| [vibe-repo-init](../vibe-repo-init/SKILL.md) | Blank repo; then seed the repo wire |

## Trigger match (max 2 passes)

1. If the repo seed exists, match **repo** TRG.
2. If no match, match **pack** TRG.

Repo SKL wins for project work (`vfdl2-*` and other `.cursor/skills/` ids). Pack SKL wins for pack methods (OOSEM, SysML hub, this cluster).

## Gates

| MUST | MUST NOT |
|------|----------|
| Bind pack vs repo before edit | `scan_skills_to_wire.py --repo-skills ... --write` into the pack seed |
| Point at pack skills with `pack: 'user'` pointer rows | Copy pack `SKILL.md` bodies into the repo |
| Keep density contract on every new SKL | Invent ids absent from the bound seed |

Handoff: [assets/bind-handoff.md](assets/bind-handoff.md). Repo stub: [assets/repo-skill-graph-seed.wire](assets/repo-skill-graph-seed.wire).
