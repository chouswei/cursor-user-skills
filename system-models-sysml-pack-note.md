# system-models-and-architecture — skills in user pack

**Audience:** LLM + human maintaining **system-models-and-architecture**.

## What moved out of the repo’s `.cursor/skills/`

These skill folders live **only** under **`~/.cursor/skills/`** (user pack), not under **`<repo>/.cursor/skills/`**:

- **SysML:** all **`sysml-*`**, **`mcp-sysml-v2`**, **`mcp-sysmledgraph`**, **`traceability-footprint-to-sysml`** (open-issue; pack SSOT in that skill’s `references/` — ignore stale `../../../docs` paths)
- **Doc / diagrams / PCBA readers:** **`mermaid`** (cluster entry → **`mmdc`**, **`pretty-mermaid`**, **`mermaid-doc-readability`**), **`project-output-article`**, **`system-design-report-generator`**, **`toon-prompt-format`**, **`tron-format`**, **`pcba-netlist-reader`**, **`pcba-design-reviewer`**

## What still ships **in** the repo (`.cursor/skills/`)

**`reasoning-strategy-selector`**, **`md-to-tex`**, **`mmdc`**, **`hardware-custom-pcba-workflow`**. Their `SKILL.md` bodies link to user-pack ids above (e.g. Mermaid, TOON) for pairing.

## Markdown links inside user-pack skills

Many bodies still contain **repo-relative** paths such as `../../../sysml-v2-models/...` that were correct when the skill lived under **`<repo>/.cursor/skills/<id>/`**.

**When this repository is the Cursor workspace:** resolve those paths from the **repository root** (the folder that contains `sysml-v2-models/`, `hardware/`, `docs/`), not from the skill file’s location on disk.

**Prefer:** open targets from the repo tree (e.g. `sysml-v2-models/libs/common/README.md`) instead of relying on broken relative links from the user-pack path.

## Repo hub

- **`SKILL-MAP-REPO.md`** (under **`.cursor/skills/`** in the repo) — lists the four in-repo skills; full id catalogues: **`SKILL-MAP-USER-PACK.md`** at the repo root.

