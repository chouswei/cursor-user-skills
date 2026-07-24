# Skill Graph (LLM-only hub)

**Audience:** model. Wire rows are canonical. **Do not** treat this file as the graph — it routes you to the graph.

---

## Architecture (three tiers)

```text
@EDG: E_sg_01|SKILL-GRAPH.md|canonical_graph|skill-graph-seed.wire|single_source_D2|persistent
@EDG: E_sg_02|SKILL-GRAPH.md|schema_docs|reasoning-strategy-selector/references/skill-graph.md|persistent
@EDG: E_sg_03|SKILL-GRAPH.md|runtime_graph|memnet:SKG_global|optional_sync|persistent
@EDG: E_sg_04|SKILL-GRAPH.md|membership_index|skill-graph-seed.wire|@SKL_rows|persistent
@EDG: E_sg_05|SKILL-GRAPH.md|audit_view|reasoning-strategy-selector/references/core-strategy-principles.md|generated|persistent
@EDG: E_sg_06|reasoning-strategy-selector|traverses|skill-graph-seed.wire|route_graph|persistent
```

| Tier | Artifact | Role |
|------|----------|------|
| 1 | [`skill-graph-seed.wire`](reasoning-strategy-selector/references/skill-graph-seed.wire) | **Canonical graph** — `@SKG`, `@SKL`, `@TRG`, `@EDG` (~100 skills, triggers, typed edges) |
| 2 | `memnet serve` → `SKG_global` | **Runtime graph** — `query_warm(SKG_global)` when serve up; merge seed via `bootstrap --sync` |
| 3 | This file + slim catalog rule | **Routing hub** — rules only; no duplicate node/edge payload |

**D2:** Seed wire is single source. Markdown tables here were a generated view — **removed**; regenerate audit table only via `python tools/bootstrap_skill_graph.py --regenerate-views`.

---

## Routing procedure

```text
@RUL: SG01|MUST|trigger routing via graph traversal (seed wire or MemNet warm), not flat table scan|high
@RUL: SG02|MUST|≤2 trigger-match passes on @TRG phrases connected to @SKL via triggers edges|high
@RUL: SG03|MUST|open matched <skill-id>/SKILL.md only|high
@RUL: SG04|MUST|ambiguous after 2 scans → ask user or repo AGENTS; optional reasoning-strategy-selector only for explicit multi-match|high
@RUL: SG05|MUSTNOT|invent skill-ids; membership = @SKL rows in skill-graph-seed.wire|high
@RUL: SG06|MUSTNOT|iterate related_skills.txt as checklist|high
@RUL: SG07|MAY|serve down → parse skill-graph-seed.wire locally (D3 graph-only)|med
```

```text
@PRC: sg1|extract keywords from user phrase|sg2
@PRC: sg2|serve up? query_warm(SKG_global, depth=2) : parse seed.wire locally|sg3
@PRC: sg3|match @TRG phrase → follow triggers @EDG → @SKL|sg4
@PRC: sg4|rank: led_to_success boost + complements/precedes/default_stack edges|sg5
@PRC: sg5|open top @SKL id SKILL.md; SysML hub stack if sysml domain|done
```

---

## Graph node shapes (summary)

Full schema: [`skill-graph.md`](reasoning-strategy-selector/references/skill-graph.md).

```text
@SKG: SKG_global|version|user_pack|recycle
@SKL: id|pack|pattern|dir|domain|cx|stakes|ev|tension|path|recycle
@TRG: id|phrase|recycle
@EDG: id|from|relation|to|note|recycle
```

Key relations: `triggers`, `precedes`, `default_stack`, `complements`, `specializes`, `requires`, `conflicts_with`, `led_to_success`.

Pattern codes: `G`=Generator · `R`=Reviewer · `P`=Pipeline · `T`=Tool-wrapper.

---

## SysML default stack (graph edges, not prose)

```text
@EDG: E_sys_01|sysml-modeling-session-checklist|default_stack|sysml-modeling-workflow|hub|persistent
@EDG: E_sys_02|sysml-modeling-workflow|default_stack|sysml-memnet-documentation|memnet|persistent
```

Then ≤1 specialist `@SKL` from `triggers` match. Repo `AGENTS.md` may add project overrides.

---

## Maintenance

```text
@RUL: SG_M01|MUST|graph edits in skill-graph-seed.wire only (or scan_skills_to_wire.py --write)|high
@RUL: SG_M02|MUST|after seed change: bootstrap_skill_graph.py --regenerate-views|high
@RUL: SG_M03|SHOULD|bootstrap --sync to merge into MemNet (preserve led_to_success)|med
@RUL: SG_M04|MUST|validate: python tools/validate_selector_pack.py --check-views|high
```

---

## Why not duplicate the graph in this file?

```text
@SEL: flat_100_row_table|NO|duplicates @SKL+@TRG+triggers @EDG; drifts from seed; ~3k tokens every load
@SEL: wire_hub + seed.wire|YES|single source; traversable; warm-read slice; edges queryable
@SEL: @SET in alwaysApply catalog|NO|burns tokens every turn; membership already @SKL in seed
```


**End.** Open [`skill-graph-seed.wire`](reasoning-strategy-selector/references/skill-graph-seed.wire) or `query_warm(SKG_global)` for the actual graph.
