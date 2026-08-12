---
name: gql-path-patterns
description: >-
  Use when building or debugging variable-length paths, reachability,
  shortest/cheapest path, or fan-out control in GQL/Cypher-like graph queries.
  Triggers: variable-length path, reachability, DEPENDS_ON walk, path explode,
  bounded hops.
metadata:
  pattern: tool-wrapper
  specialization: graph-paths
  domain: data
  version: "1.1"
token_guardrails: |
  - Always bound hop depth (e.g. {1,4}); never bare unbounded walks by default.
  - Anchor at least one endpoint with label + selective property.
  - Prefer DISTINCT + LIMIT when projecting nodes from fan-out paths.
---

# GQL Path Patterns

Thin skill for **paths and reachability**. Pair with [graph-query-language](../graph-query-language/SKILL.md) for basics.

## Rules of thumb
- Bound every variable-length hop (`{1,3}` not bare `*`).
- Anchor at least one end with label + selective property.
- Prefer typed relationships (`:REL`) over untyped walks.
- Decide **directed vs undirected** before writing the pattern.

## Bounded walk
```gql
MATCH (start:System { id: $id })-[:DEPENDS_ON]->{1,4}(dep:System)
RETURN DISTINCT dep.id AS dependency
LIMIT 200
```

## Exists / reachability
```gql
MATCH (a:Node { id: $a })
FILTER EXISTS {
  MATCH (a)-[:LINK]->{1,6}(b:Node { id: $b })
}
RETURN a.id AS reachable_from
```
(If `EXISTS` subquery is unsupported, use a bounded `MATCH` + `count(*) > 0`.)

## Fan-out control
1. Filter early (`FILTER` / `WHERE` on start node).
2. Constrain rel types.
3. Cap depth.
4. `DISTINCT` + `LIMIT` on projection.
5. For analytics, aggregate (`count`, `collect`) instead of returning every path.

## Path objects
```gql
MATCH p = (a:Person)-[:KNOWS]->{1,3}(b:Person)
FILTER a.id = $a AND b.id = $b
RETURN p
LIMIT 20
```
Return nodes/rels extracted from `p` if the client cannot render path values.

## Common failure modes
| Symptom | Likely cause |
| --- | --- |
| Timeout / OOM | Unbounded depth or missing labels |
| Empty result | Wrong direction or tighter type than data |
| Duplicate rows | Missing `DISTINCT` on node projection |
| Wrong end node | Undirected pattern absorbing reverse edges |

## Deliverable style
Give the bounded query first. State max depth and relationship types assumed. Add a stricter variant if the first is for exploration.

## Related
- Core GQL: [graph-query-language](../graph-query-language/SKILL.md)
- MemNet agent wire: [memnet-format](../memnet-format/SKILL.md), [mcp-memnet](../mcp-memnet/SKILL.md)
- SysML modeling + MemNet: [sysml-gql](../sysml-gql/SKILL.md)
