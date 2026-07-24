# Skill graph (MemNet wire schema)

**Audience:** LLM + tooling. Canonical routing store is [`skill-graph-seed.wire`](skill-graph-seed.wire).

## Pre-Phase-1 decisions (D1–D4)

| # | Decision |
|---|----------|
| D1 | Selector lives **only** in user-pack (`~/.cursor/skills/reasoning-strategy-selector/`). Repo copy is a thin pointer. |
| D2 | `skill-graph-seed.wire` is **single source**. `SKILL-GRAPH.md` is a **wire hub** (routing rules + `@EDG` pointers). `core-strategy-principles.md` is a **generated audit view** (`bootstrap --regenerate-views`). |
| D3 | **Graph-only routing.** No 6D convolution fallback. MemNet down → parse seed wire locally. |
| D4 | **Phase 4 active:** parent agent writes `led_to_success` on settle; selector reads +0.6 boost per edge. |

## Prior art

[`engineering-practices-learner`](../../engineering-practices-learner/SKILL.md): stable slug ids, typed edges (`depends_on`, `conflicts_with`, `complements`), retriever closure. Borrow id discipline and `complements` subset.

---

## Node tags

| Tag | Fields (pipe order) | Notes |
|-----|---------------------|-------|
| `@SKG` | `id\|version\|scope\|recycle` | Graph root: `SKG_global` |
| `@SKL` | `id\|pack\|pattern\|dir\|domain\|cx\|stakes\|ev\|tension\|path\|recycle` | Skill node; `id` = folder name |
| `@TRG` | `id\|phrase\|recycle` | Trigger phrase |
| `@TSK` | existing MemNet task shape | Ephemeral routing: `TSK_route_<slug>` |

- **pack:** `user` \| `repo`
- **pattern / dir:** G \| R \| P \| T
- **domain:** user \| sysml \| sysml-tool \| pcba \| doc \| meta \| coding
- **cx / stakes / tension:** low \| medium \| high
- **ev:** conceptual \| structural \| measured

---

## Edge relations (`@EDG`)

Format: `@EDG: edge_id\|from\|relation\|to\|note\|recycle`

| Relation | Meaning |
|----------|---------|
| `triggers` | `@TRG` → `@SKL` |
| `precedes` | Ordered workflow step |
| `default_stack` | Hub → mandatory entry skill |
| `complements` | Often paired in one turn |
| `specializes` | Narrower under broader / domain member |
| `requires` | Hard prerequisite |
| `shares_domain` | Weak same-domain signal (auto-derived; **not** density minimum) |
| `conflicts_with` | Mutually exclusive (rare) |
| `led_to_success` | Phase 4 empirical edge |

---

## Edge-density contract

Every `@SKL` before seed acceptance:

- ≥ **2** `@TRG` rows (via `triggers` edges)
- ≥ **1** of: `precedes`, `complements`, `default_stack`, `specializes`, `requires`
- `shares_domain` does **not** count toward minimum

---

## Anchor strategy

| Situation | Anchor | depth | max_rows |
|-----------|--------|-------|----------|
| Trigger matched | `SKL_<id>` | 2 | 30 |
| Multiple triggers | each `SKL_<id>` | 1 | 15 |
| Cold start | `SKG_global` | 2 | 50 |
| Disambiguation | `SKL_<top>` | 1 | 20 |

Never `SKG_global` at depth 3.

---

## Ranking weights (v0)

```
triggers hit          +1.0
precedes (1-hop)      +0.8
default_stack         +0.7
complements           +0.5
specializes           +0.4
shares_domain         +0.2
led_to_success        +0.6
hop penalty           −0.15 per hop beyond 1
```

No 6D convolution. `@SKL` dir/domain/cx fields are audit metadata on nodes, not a flat-table ranker.

Return `order[]` when top score ≥ **0.55**. Calibrate via `tools/score_routing.py` + [`routing-golden-set.toon`](routing-golden-set.toon).

### Changelog

| Version | Change | Golden top-1 / top-3 |
|---------|--------|----------------------|
| v0 | Initial edge weights | — |
| v1 | Graph-only; removed convolution | 40% / 87% |
| v2 | Direct-trigger pin + edge-only traverse; 8 SKG default_stacks | **100% / 100%** |
| v3 | Phase 4 `led_to_success` read/write protocol activated | 100% / 100% |
| v4 | Mermaid placement-by-degree: TSK_diagram triggers + complements stack | 100% / 100% |
| v5 | `sysml-interconnection-mermaid` skill hub + graph nodes | 100% / 100% |

---

## Query patterns

1. Match intent tokens against `@TRG.phrase` (case-insensitive substring).
2. `query_warm(anchor=SKL_<hit>, depth=2, max_rows=30)`.
3. Rank neighbours by edge type + hop; apply 6D boost from `@SKL` fields.
4. Output TOON handoff (`order[]`, optional `graph_path[]`).
5. Fallback: MemNet empty → parse `skill-graph-seed.wire` locally (same graph walk). Never convolution.

---

## Maintenance

New skill:

1. Add `@SKL` + ≥2 `@TRG` + ≥1 typed `@EDG` to `skill-graph-seed.wire`.
2. `python tools/bootstrap_skill_graph.py --regenerate-views`
3. `python tools/validate_selector_pack.py`
4. Optional: `python tools/bootstrap_skill_graph.py --sync` (MemNet)
