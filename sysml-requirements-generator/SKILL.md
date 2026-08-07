---
name: sysml-requirements-generator
description: >-
  Scaffold or extend requirements-*.sysml: requirement def, requirementId, doc (SHALL/SHOULD),
  package ProjectNameRequirements; prefer refine/derive parent→child trees over flat lists; wire
  satisfy on parts/actions. Triggers: requirement def, R1 R2, SHALL, SysML requirements package,
  add requirement, refine requirements, derive requirements, trace to design.
metadata:
  pattern: generator
  output-format: sysml
  secondary: ask-first
  version: "1.1"
  pairs_with: [mcp-sysml-v2, sysml-traceability, sysml-root-config, sysml-requirements-audit]
token_guardrails: |
  - Ask for id scheme and parent package name before bulk generation.
  - Prefer **refine** / **derive** under an existing parent requirementId; do not invent flat peers when a parent already covers the theme.
  - After edits: validate; add satisfy in deploy only when user confirms mapping.
  - Load references/requirements-style-guide.md for patterns.
  - When requirements mention cabling or ports, match deploy / physical names (or say "as allocated in deploy"); see sysml-traceability/references/de-facto-modeling.md.
  - Do not hard-code site IPs or hostnames in skill prose or stubs -- use generic patterns (sticky MAC reservation, ordered commissioning, multi-edge octet bands).
  - After substantive .sysml changes: sysml-memnet-cache delta (`@REQ`/`@SYM`); workflow step 6; sync outputs requirements-traceability section via sysml-traceability / sysml-view-doc-sync.
  - Before multi-file refactor: pin_map(TSK_model_*).
---

# SysML requirements generator

**When:** New or extended **`requirements-<project>.sysml`** with **`requirement def`**, optional **refine** / **derive** children, and optional **`satisfy`** from deploy or behaviour.

## Pipeline

1. **Ask first** — Package name, **ID attribute** (`requirementId`), whether work is **new root**, **refine**, or **derive** under an existing parent id; short names + one-line SHALL each.

2. **Hierarchy first** — Prefer a **parent → child** tree (same id prefix family) via SysML **`refine`** / **`derive`** (or project-equivalent nesting). Flat new peers only when no parent fits. Child ids inherit the parent family (e.g. `PROJ-THEME` → `PROJ-THEME-DHCP`).

3. **Conventions** — [references/requirements-style-guide.md](references/requirements-style-guide.md).

4. **Generate** — [assets/requirement-def-stub.sysml](assets/requirement-def-stub.sysml): `private import ScalarValues::String`; each **`requirement def`** with **`requirementId`** and **`doc /* ... */`**. Cross-reference sibling ids in **doc** only when they clarify scope; hierarchy links belong in **refine** / **derive**.

5. **Root / config** — Ensure **`root-<project>.sysml`** imports requirements **before** deploy if satisfy resolves across packages (**sysml-root-config**).

6. **Satisfy (optional)** — On implementing elements: **`satisfy ReqName;`** only after user maps requirement → element.

7. **Verify + docs** — **SysML v2 MCP validate**. Hand off **sysml-traceability** / **sysml-view-doc-sync** so **`outputs/**/10-requirements-traceability.md`** (or project equivalent) shows parent/child and satisfy coverage.

**Example:** `sysml-v2-models/projects/sysmledgraph/models/requirements-sysmledgraph.sysml`
