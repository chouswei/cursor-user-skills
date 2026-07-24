# Skill-creator quality checklist

## First principles (must hold for every generated skill)

1. **Truth over Convention** — Valid for Google ADK `load_skill_from_dir`, portable Agent Skills layout ([agentskills.io](https://agentskills.io)), and typical **skill.fish** installs; not merely stylistic copy.
2. **Progressive Disclosure** — L1 description; L2 SKILL body; L3 refs/assets. No bulk L3 in L2.
3. **Specificity Beats Generality** — `description`: third person, WHAT + WHEN, concrete triggers.
4. **Separation of Concerns** — Flow in SKILL; bulk content in references/assets.
5. **Self-Consistency** — Output could be re-validated with this same checklist.
6. **Feedback & Validation** — This checklist applied before final delivery.
7. **Composition over Monoliths** — One primary `metadata.pattern`; secondary noted in one line if needed.

## Google ADK

- [ ] Skill folder has required `SKILL.md`; optional `references/`, `assets/`, `tools/` or `scripts/` as needed.
- [ ] `description` is specific enough for SkillToolset / agent discovery (L1 index) and for registry search (skill.fish) when publishing.
- [ ] `metadata` values are strings only (`pattern`, optional `domain`, `version`).
- [ ] If `tools/*.py` exists: `tool_spec` dict with `name`, `description`, `parameters`; name matches SKILL "register ADK tool" / Tool Wrapper line.
- [ ] SKILL mentions running from skill dir: `python tools/...` or ADK registration where applicable.

## Frontmatter and naming

- [ ] `name` matches folder name; lowercase-hyphen; max 64 chars.
- [ ] `metadata.pattern` matches primary pattern: `tool-wrapper` | `generator` | `reviewer` | `inversion` | `pipeline` | or documented hybrid.
- [ ] No duplicate `pattern:` / `version:` keys unless intentional parity with sibling skills.

## Structure and links

- [ ] `SKILL.md` under ~500 lines; prefer concise orchestration.
- [ ] Links from SKILL use forward slashes; one level deep to references/assets.
- [ ] `Folder_Structure.md` lists created paths.

## Pipeline-style children (when applicable)

- [ ] `pipeline_steps` ordered; retrieval step not skipped when specified.
- [ ] `system_instruction` and `token_guardrails` present if matching repo pipeline skills.

## skill.fish and portability (when user targets registry, broad agents, or team sync)

Registry and CLI context: **[skill.fish](https://skill.fish)**; commands: **skillfish** (`npx skillfish …` or global install). Repo reference skill: [skillfish/SKILL.md](../../skillfish/SKILL.md).

- [ ] **Install path** documented when helpful: `skillfish add owner/repo` or `owner/repo/path/to/skill` for monorepos; Cursor global dir `~/.cursor/skills/` (per skillfish).
- [ ] **Submit** path noted if user will list publicly: `skillfish submit owner/repo` or GitHub URL; remind that listings are reviewed and consumers should still read source.
- [ ] **Version bump**: for any update that will be pushed to GitHub repo backing the user pack (skillfish consumers), increment `metadata.version` in frontmatter before the push. Initial skills start at 1.0 or 1.0-<slug>; subsequent publishes always bump.
- [ ] **Team sync**: if user asked, mention `skillfish bundle` -> `skillfish.json` and `skillfish install` / `--dry-run` per skillfish docs.
- [ ] **Safety**: generated skill does not rely on opaque trust; no exfil-by-default patterns; align with skill.fish upstream warning that third-party skills are not fully vetted.

## Hybrid pipeline (when applicable)

- [ ] Primary `metadata.pattern` is still `pipeline`; secondary composition noted in one line (`metadata.secondary` or explicit sentence in body).
- [ ] `pipeline_steps` name any **delegated** skills by id and relative `../<skill>/SKILL.md` path — no pasted full sibling SKILL bodies.
- [ ] If **reasoning-strategy-selector** is used: step text points to `reasoning-strategy-selector/SKILL.md` and says to honor returned `order` (or documents a fixed override).
- [ ] Gates are explicit (when selector runs, when sub-skills run, when final template is filled).
- [ ] `wants_selector_update` considered if the new skill should appear in repo selector lists.

## Output contract (skill-creator run)

- [ ] Final user-visible block matches `assets/skill-output-template.md` only (no extra sections).
- [ ] Selector update snippets, if any, are consistent across all three selector files and avoid duplicate YAML list entries.

## Retrieval seeds in principle files (when applicable)

- [ ] `references/core-*-principles.md` ends with retrieval seeds line for keyword retriever.
