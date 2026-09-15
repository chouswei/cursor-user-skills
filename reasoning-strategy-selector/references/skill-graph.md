# Skill graph (schema for MemNet + seed export)

**Audience:** LLM + tooling. Canonical live graph is in **MemNet** (`SKG_global` / `SKL` nodes, queried via `pin_map` and `find`). Agent I/O uses the GQL wire (shaped pin_map + openCypher-shaped mutate); wire SSOT: [memnet-format](../../memnet-format/SKILL.md) (see also [SKILL-GRAPH.md](../../SKILL-GRAPH.md)). Optional offline export: [`skill-graph-seed.wire`](skill-graph-seed.wire).

## Pre-Phase-1 decisions (D1-D4)

| # | Decision |
|---|----------|
| D1 | Selector lives **only** in user-pack (`~/.cursor/skills/reasoning-strategy-selector/`). Repo copy is a thin pointer. |
| D2 | **MemNet graph is live authority**. `SKILL-GRAPH.md` is a **hub** (routing rules + stack definitions). `skill-graph-seed.wire` is an **optional export artifact**. |
| D3 | **Graph-only routing.** Primary via MemNet `pin_map`/`find`. MemNet down -> fallback to `SKILL-GRAPH.md` hub. |
| D4 | **Phase 4 active:** parent agent writes `LED_TO_SUCCESS` on settle; selector reads +0.6 boost per edge. |

## Prior art

[`engineering-practices-learner`](../../engineering-practices-learner/SKILL.md): stable slug ids, typed edges (`depends_on`, `conflicts_with`, `complements`), retriever closure.

---

## Node kinds (GQL labels)

| Kind | Typical fields | Notes |
|------|----------------|-------|
| SKG | version, scope, recycle | Graph root: `SKG_global` |
| SKL | pack, pattern, dir, domain, path, recycle | Skill node; id = folder name |
| TRG | phrase, recycle | Trigger phrase |
| TSK | goal, phase, status, recycle | Ephemeral routing: `TSK_route_<slug>` |

- **pack:** `user` | `repo`
- **pattern / dir:** G | R | P | T
- **domain:** user | sysml | sysml-tool | pcba | doc | meta | coding

Agent-facing edge shape:

```cypher
(:TRG {id: 'trg-id'})-[:TRIGGERS {id: 'E01', note: '...', recycle: 'persistent'}]->(:SKL {id: 'skill-id'})
```

| Relation | Meaning |
|----------|---------|
| `TRIGGERS` | TRG -> SKL |
| `PRECEDES` | Ordered workflow step |
| `DEFAULT_STACK` | Hub -> mandatory entry skill |
| `COMPLEMENTS` | Often paired in one turn |
| `SPECIALIZES` | Narrower under broader / domain member |
| `REQUIRES` | Hard prerequisite |
| `SHARES_DOMAIN` | Weak same-domain signal |
| `CONFLICTS_WITH` | Mutually exclusive (rare) |
| `LED_TO_SUCCESS` | Phase 4 empirical edge |

**Engine seed:** `skill-graph-seed.wire` is GQL `CREATE` rows. Tools parse that file; agents `mutate` the same shape.

## Edge-density contract

Every SKL before seed acceptance:

- >= **2** TRG rows (via `TRIGGERS` edges)
- >= **1** of: `PRECEDES`, `COMPLEMENTS`, `DEFAULT_STACK`, `SPECIALIZES`, `REQUIRES`

## Maintenance

See [SKILL-GRAPH.md](../../SKILL-GRAPH.md) maintenance rules. Validate with `python tools/validate_selector_pack.py --check-views` when available.
