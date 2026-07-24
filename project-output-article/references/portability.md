# Portability — project-output-article

## Copying this skill

The normative spec is **`references/PROJECT_OUTPUT_ARTICLE_STANDARD.md`** next to this file. To reuse in another workspace:

1. Copy the folder **`~/.cursor/skills/project-output-article/`** (entire tree: `SKILL.md`, `references/`, `assets/`) into the target machine’s **`~/.cursor/skills/`** (or your team’s skills bundle path).
2. Add **Map** alias and **Edges** in that repo’s **`.cursor/skills/SKILL-GRAPH.md`** (see this repo’s graph for **`poa`** → **`project-output-article`**).
3. Patch **sysml-view-doc-sync** (or your doc-sync skill) with **`pairs_with`** / a short **Pairing** line pointing to **`project-output-article`**.

## Optional siblings

If **mermaid**, **mmdc**, or **sysml-view-doc-sync** are missing, either install those skills from the same pack or trim **`pairs_with`** in **`SKILL.md`** so validation tools do not expect missing folders.

## skillfish

If you publish via [skillfish](../../skillfish/SKILL.md), keep **`metadata.pattern: pipeline`** and relative links consistent, or replace them with your hub paths after install.
