---
name: skill-creator
description: >-
  Scaffolds new Agent Skills for Google ADK, portable Agent Skills (agentskills.io), and a project-local **`.cursor/skills/`** pack (or a path the user names);
  aligns output with skill.fish / skillfish installs and team manifests when the user cares. Chooses among
  tool-wrapper, generator, reviewer, inversion, pipeline, hybrid pipeline (meta-orchestration: pipeline +
  selector / sibling skills), or generic; emits full folder specs and optional reasoning-strategy-selector
  updates. Triggers: create skill, scaffold SKILL.md, new agent skill, skill-creator, ADK skill, SkillToolset,
  skill.fish, skillfish, submit skill, skillfish.json bundle install, hybrid pipeline, nested pipeline,
  meta pipeline, orchestrate skills, pattern tool-wrapper generator reviewer inversion pipeline.
metadata:
  pattern: pipeline
  version: 1.1-skill-creator
  domain: agent-skills

pipeline_steps:
  1. Clarify / intake
     - Emit one short structured block (plain Markdown list or table — not TOON/TRON): job_summary, proposed_skill_name, target_root (default **`.cursor/skills/`** relative to workspace root unless user specifies another pack root), wants_retriever (bool), wants_selector_update (bool), wants_hybrid_pipeline (bool), user_triggers (string[]), constraints (string). JSON only if a tool requires it at the boundary.
  2. Pattern selection
     - Call Tool Wrapper: skill-pattern-retriever with query = job_summary + user_triggers + constraints.
     - If tool unavailable, load references/core-skill-patterns.md and apply same keyword logic as tools/skill-pattern-retriever.py.
     - Choose primary pattern; if ambiguous ask one clarifying question then continue. Honor first principles in references/core-skill-patterns.md.
     - If wants_hybrid_pipeline is true or job clearly needs nested/orchestration (meta-pipeline, pipeline inside pipeline, routes via reasoning-strategy-selector): primary pattern = **pipeline**, scaffold source = **stub-hybrid-pipeline.md** (see "Pattern: hybrid pipeline" in core-skill-patterns.md).
  3. Scaffold
     - If hybrid pipeline (step 2): load assets/stub-hybrid-pipeline.md. Else load assets/stub-<pattern>.md (stub-generic.md if generic). Instantiate folder name, file names, optional retriever path.
  4. Content generation
     - Produce minimal real references/*.md and assets/*.md; retrieval seeds on principle files when retriever exists. Keep generated SKILL.md orchestration-only (Separation of Concerns; Progressive Disclosure).
     - If user mentions skill.fish, skillfish, public registry, submit, or team skill sync: add **Post-create** guidance using commands and paths from [skillfish/SKILL.md](../skillfish/SKILL.md) (e.g. `npx skillfish add owner/repo`, `skillfish submit`, `skillfish bundle` / `skillfish install`, Cursor `~/.cursor/skills/`). Do not invent repo URLs.
  5. Validation
     - Apply every item in references/skill-creator-quality.md (include **skill.fish and portability** when registry/team/publish intent is present); max one revision.
  6. Final output
     - Fill assets/skill-output-template.md exactly; no extra sections.
  7. Selector snippets (conditional)
     - If wants_selector_update: append edits to `reasoning-strategy-selector/references/skill-graph-seed.wire` (`@SKL` + ≥2 `@TRG` + ≥1 typed `@EDG` per skill-graph.md density contract); run `python tools/bootstrap_skill_graph.py --regenerate-views`; update `related_skills.txt` if router subset changes then `python tools/sync_related_skills_from_txt.py --write`; `python tools/validate_selector_pack.py --check-views`.

system_instruction: |
  Respond in concise mode. Prefer plain Markdown tables or short prose for steps 1–2 structured handoffs; do not use TOON/TRON. JSON only when a tool requires it. Each intermediate step ≤ 400 tokens.
  Never repeat the user verbatim in bulk. Final user-visible output must follow assets/skill-output-template.md exactly.
  Generated skills must be ADK-loadable (load_skill_from_dir), follow the seven first principles in references/core-skill-patterns.md,
  and stay compatible with the portable Agent Skills shape (agentskills.io); skill.fish / skillfish workflows come from ../skillfish/SKILL.md when relevant.

token_guardrails: |
  - Load core-skill-patterns.md at most once per run unless revising; prefer skill-pattern-retriever over full paste.
  - response_format: plain Markdown for internal clarify/selection when used; final = skill-output-template only.
---

# Skill creator

**Role:** Meta pipeline — scaffold ADK-loadable skills per [references/core-skill-patterns.md](references/core-skill-patterns.md).

Run **pipeline_steps** in order; do not skip step 2 or 5.

**Resources:** [references/core-skill-patterns.md](references/core-skill-patterns.md) · [references/skill-creator-quality.md](references/skill-creator-quality.md) · [assets/skill-output-template.md](assets/skill-output-template.md) · stubs `stub-*.md` in `assets/` · [skill.fish / skillfish CLI](../skillfish/SKILL.md)

**Step 2 tool:** `python tools/skill-pattern-retriever.py "<query>"` or ADK `skill-pattern-retriever`.

**Non-goals:** No silent disk writes; link https://google.github.io/adk-docs/skills/ instead of pasting ADK docs.

**Pairing:** [reasoning-strategy-selector](../reasoning-strategy-selector/SKILL.md) for downstream routing; [skillfish](../skillfish/SKILL.md) for install/submit/manifest; [skill-reviewer](../skill-reviewer/SKILL.md) before publish. For hybrid skills, suggest selector before locking `pipeline_steps` if embedded siblings unclear, and after for the next task — document in generated principles **Pairing** when relevant.
