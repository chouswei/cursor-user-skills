# Agent Skill review checklist

Use for folders containing `SKILL.md` (and optional `references/`, `assets/`, `tools/`). Aligns with **portable Agent Skills** ([agentskills.io](https://agentskills.io)) and practical **skill.fish** / **skillfish** registry use ([skill.fish](https://skill.fish); see repo [skillfish/SKILL.md](../../skillfish/SKILL.md)).

## Folder layout (L2 / L3)

- [ ] **Skill root** is one directory; entrypoint **`SKILL.md`** at root (not nested).
- [ ] **`Folder_Structure.md`** present **or** body of **`SKILL.md`** explicitly states expected tree — reviewers flag “layout unclear” when neither exists and the skill has many files.
- [ ] **Heavy content** lives under **`references/`** or **`assets/`**, not pasted into **`SKILL.md`** (progressive disclosure).
- [ ] Links from **`SKILL.md`** to **`references/`** / **`assets/`** are **one hop** (`references/…`, `assets/…`), forward slashes, no `..` escape from skill root except to **repo** docs (then `../../../docs/…` etc. is OK if stable).

## Format and discovery (L1 / L2)

- [ ] **SKILL.md** body is **orchestration** (steps, when to load what), not a dump of all reference text.
- [ ] **Frontmatter** includes at least **`name`** and **`description`** (non-empty). **`name`** matches **folder** name: lowercase, hyphens, max ~64 chars.
- [ ] **`description`**: **WHAT + WHEN**, with **concrete trigger phrases** agents and registries can match (contrast: “helps with tasks”).
- [ ] **Primary reader is the LLM** — optimise for agent parsing (tight steps, **plain Markdown tables** for dense structured data); prose-for-humans only when the deliverable is explicitly non-agent. Do not use TOON/TRON.
- [ ] **`SKILL.md` length** manageable (aim **well under ~500 lines** unique rules; split into `references/` if not).

## `metadata` and pattern

- [ ] **`metadata.pattern`** is exactly **one** primary value from the **canonical set**: **`tool-wrapper`** | **`generator`** | **`reviewer`** | **`inversion`** | **`pipeline`**. Do **not** invent ad-hoc values (e.g. `tool-cli`) unless the repo documents an extension — prefer **`tool-wrapper`** + **`metadata.secondary`** for CLI-only tools.
- [ ] **Behavior matches pattern** (e.g. reviewer → severities + rubric; generator → template in `assets/`; pipeline → ordered steps / gates).
- [ ] **Hybrid skills:** primary stays **`pipeline`** (or the dominant pattern); composition is one line: **`metadata.secondary`** or a single sentence in the body (not two competing `pattern` keys).
- [ ] **ADK:** Prefer **`metadata`** string-shaped values; avoid duplicate YAML keys for `pattern` / `version`.
- [ ] **`token_guardrails`**: if present, belongs in **frontmatter** (before closing `---`) **or** as a normal **`## Guardrails`** markdown section — not raw `key: |` text **after** frontmatter (renders as garbage in some clients).

## Pattern conformance (declared `metadata.pattern` vs skill body + folder)

Read **`metadata.pattern`** first, then verify the **whole package** matches. Mismatch = at least **warning**; if users/agents would be misled (e.g. `generator` with no template) = **error**.

| Declared pattern | Expect (minimum) | Mismatch signals |
|------------------|------------------|------------------|
| **`generator`** | **`assets/`** holds a **template**; body says load template + fill + **return only** that artifact; optional `references/` style guide. | Numbered pipeline + JSON phases but no template path; output shape undefined. |
| **`reviewer`** | **Checklist/rubric** in **`references/`** (or explicit inline list); **severity** scheme in frontmatter or body; output structure (summary, findings, score, …) stated. | Claims “review” but only vague prose; no severities or rubric. |
| **`inversion`** | **Phased questions / gates** before synthesis; then **`assets/*-template.md`** (or equivalent) filled after intake — not a single-shot dump. | Same shape as **pipeline** (`pipeline_steps` + JSON) without inversion gates — likely should be **`pipeline`** (or body rewritten). |
| **`pipeline`** | **Ordered steps** (`pipeline_steps` in YAML or numbered body steps); **gates** where skipping breaks correctness; optional **`system_instruction`** / **`token_guardrails`**. | Only two bullets and no order; or **tool-wrapper** content with mis-tagged `pipeline`. |
| **`tool-wrapper`** | **Conventions** in **`references/`**; apply when coding/reviewing; optional **`tools/*-retriever.py`**. Optional short “how to invoke” for a CLI. | Full multi-step pipeline and final template — probably **`pipeline`** or **`generator`**, not primary **tool-wrapper**. |

**Hybrid:** If the skill is **mostly ordered steps** but embeds another pattern, primary should be **`pipeline`** with **`metadata.secondary`** (or one body sentence) naming the mix — not a second `pattern:` key.

## Output contract (orchestration skills)

- [ ] **Reviewer / selector** skills: final answer format is stated (e.g. table by severity, JSON block).
- [ ] **Generator** skills: states **one artifact** shape (template path + “return only filled template”).
- [ ] **Tool-wrapper** skills: says how to **invoke** CLI/API (cwd, executable, required args).

## Safety and trust (skill.fish warns: skills are not fully vetted)

- [ ] No **opaque** “run this curl/shell” from **untrusted** URLs without risk callout.
- [ ] No instructions to **exfiltrate secrets**, **disable safety**, or bypass policies.
- [ ] **Scripts:** purpose clear; **no hardcoded secrets**; env vars / gitignore documented where needed.
- [ ] **Dependencies** (npm, pip, Docker) named; **pin versions** when reproducibility matters.

## Registry and portability (skill.fish / skillfish)

- [ ] **Monorepo:** install path explicit if non-root skill dir — e.g. `owner/repo/.cursor/skills/<name>` for **skillfish add**.
- [ ] **License / authorship** noted if user may **`skillfish submit`** or publish.
- [ ] **Version bump on GitHub push / publish**: if the reviewed skill will be pushed to a GitHub repo (for `skillfish add owner/repo`, `skillfish submit`, or any user-pack distribution), `metadata.version` MUST have been incremented since last publish. Same version on changed content is **error**. Use semver or pack suffix style (e.g. `1.2`, `1.1-foo`).
- [ ] Optional **skillfish.json** / **bundle** / **install** — mention only if user asked for team sync or registry.

## Tools and Python (when `tools/` present)

- [ ] **`tool_spec`** (or ADK equivalent) matches **`SKILL.md`** tool name and parameters.
- [ ] Runnable path documented: `python tools/<script>.py` from skill dir (or repo root — say which).
- [ ] **Retriever scripts:** **retrieval seeds** at end of principle files; Windows **cp1252** / Unicode cautions if CLI prints keywords.

## Deep quality (optional)

- [ ] Cross-check [skill-creator/references/skill-creator-quality.md](../../skill-creator/references/skill-creator-quality.md) for ADK-heavy, hybrid-pipeline, or selector-linked skills.
- [ ] Core pattern doctrine: [skill-creator/references/core-skill-patterns.md](../../skill-creator/references/core-skill-patterns.md)

## Severity guide

| Level | When to use | Examples |
|-------|-------------|----------|
| **error** | Breaks discovery, misleads automation, or unsafe default | Missing `name`/`description`; `pattern` contradicts body; broken link to **required** asset; instruction to run unvetted remote script blindly; `metadata.version` unchanged when pushing skill update to GitHub (user pack / skillfish publish) |
| **warning** | Weak maintainability, routing, or portability | Vague triggers; whole checklist inlined in `SKILL.md`; monorepo install path missing; undeclared hybrid pattern |
| **info** | Polish, consistency, optional improvements | Typos; suggest `Folder_Structure.md`; pair with **skill-creator** / **skillfish**; add `secondary` line for CLI vs MCP |

## Quick anti-patterns

- Wall of **L3** inside **L2** `SKILL.md`.
- **`metadata.pattern: tool-cli`** (or other non-canonical) without repo-wide convention.
- **`token_guardrails`** as stray YAML after frontmatter.
- Pasting **full sibling `SKILL.md`** bodies — link **`../other-skill/SKILL.md`** instead.
- **Two primary patterns** in one skill without a single declared primary + secondary.
- Unchanged `metadata.version` when content changes are destined for a GitHub push (user-pack publish via skillfish).
