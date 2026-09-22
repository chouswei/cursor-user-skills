---
name: sysmledge-repo-management
description: >-
  Open and check a SysMLEdgePrj-* git repo: submodule init, project.toml identity,
  README single source of truth kind, then hand off. Triggers: SysMLEdgePrj,
  open SysMLEdgePrj, SysMLEdge repo management, SysMLEdgePrj submodule.
metadata:
  pattern: pipeline
  version: "1.0"
  domain: sysml
  secondary: "hybrid: open gate, then sysmledge-workflow; repo overlay if the tree has one"
pipeline_steps:
  1. Classify
     - Continue only when the git repo root directory name matches SysMLEdgePrj-*.
     - If the root matches modelbasedPrj-*, stop. That class is outside this skill.
  2. Submodule gate
     - If .gitmodules exists, run git submodule update --init --recursive from the repo root.
     - Record the exit code. If .gitmodules is absent, record that and continue.
  3. Identity
     - Read project.toml [project] name and repo. name is the only projectId candidate.
     - Read README.md for the single source of truth kind. Read AGENT-CONTEXT.md when present.
  4. Layout
     - Check references/layout.md. Record missing paths. Do not invent model structure.
  5. Face status
     - Call product rev_status with projectId from project.toml. Do not call openProject.
  6. Hand off
     - Modelling day loop: ../sysmledge-workflow/SKILL.md.
     - If both product sysmledge and tip memnet-pi are visible: ../sysmledge-cursor-multitask/SKILL.md.
     - If the repo has an overlay under .cursor/skills/, follow that overlay after this gate.
  7. Report
     - Fill assets/open-report-template.md.
system_instruction: |
  Concise British English. ASCII. This skill owns the open gate for SysMLEdgePrj-* repos.
  SysMLEdgePrj-* is the git repo directory prefix. SysMLEdge is the product face.
  Do not invent projectId. Do not call openProject. Do not paste sibling skill bodies.
  Final user-visible report matches assets/open-report-template.md.
token_guardrails: |
  - Load references/core-repo-principles.md once per run.
  - Load references/layout.md once at the layout step.
  - Do not paste sibling SKILL.md bodies; link ids only.
---

# SysMLEdgePrj repo management

**Role:** Open gate for a git repo whose root directory name matches `SysMLEdgePrj-*`. Record identity, submodule state, and product-face status, then hand off.

**Not this skill:** the modelling day loop ([sysmledge-workflow](../sysmledge-workflow/SKILL.md)), a tree overlay (for example `sysmledge-pd-tree` in one repo), or a `modelbasedPrj-*` tree.

## Execution contract

Follow `pipeline_steps` in order. Stop at step 1 when the root is not `SysMLEdgePrj-*`. Do not write model files in this skill.

## Names

| Term | Meaning |
|------|---------|
| `SysMLEdgePrj-*` | Git repo root directory prefix |
| SysMLEdge | Product face `sysmledge` / `user-sysmledge` |
| projectId | `[project].name` in `project.toml` |
| SSOT | Single source of truth. README states **repo-based** or **SysMLEdge-based** |

## Delegated skills

| Id | Path | When |
|----|------|------|
| `sysmledge-workflow` | [../sysmledge-workflow/SKILL.md](../sysmledge-workflow/SKILL.md) | After the open report, for propose / Save / file edits |
| `sysmledge-cursor-multitask` | [../sysmledge-cursor-multitask/SKILL.md](../sysmledge-cursor-multitask/SKILL.md) | Product face and tip `memnet-pi` are both visible |
| Repo overlay | `<repo>/.cursor/skills/<overlay>/SKILL.md` | That tree ships an overlay |

## Resources

- [references/core-repo-principles.md](references/core-repo-principles.md)
- [references/layout.md](references/layout.md)
- [assets/open-report-template.md](assets/open-report-template.md)

## Pairing

Open-repo `AGENTS.md` wins for that tree's packages and part paths. This skill does not restate them.
