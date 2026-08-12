---
name: graph-query-language
description: >-
  Use when writing or reviewing ISO GQL / property-graph queries (MATCH, FILTER,
  RETURN, paths) against graph databases or graph APIs. Triggers: GQL, graph
  query, MATCH RETURN, property graph, Cypher-like read query.
metadata:
  pattern: tool-wrapper
  specialization: graph-query
  domain: data
  version: "1.1"
token_guardrails: |
  - Prefer parameterized values ($id) over string-concatenated literals.
  - Bound match cardinality (labels + filters + LIMIT) before returning rows.
  - Do not emit unbounded variable-length paths in default answers.
---

# Graph Query Language

Solid, thin reference for **ISO GQL** (property-graph query language). Prefer GQL wording; note Cypher only when dialect differs.

## Mental model
- **Graph**: nodes (vertices) + relationships (edges), both can carry labels/types and properties.
- **Pattern**: draw a path shape in the query; the engine binds matching graph pieces.
- **Pipeline**: match → filter → project. Keep side effects (insert/update/delete) explicit and separate from read queries.

## Core read shape
```gql
MATCH (a:Person)-[r:KNOWS]->(b:Person)
FILTER a.name = 'Ada'
RETURN a.name AS from, b.name AS to, r.since AS since
```

## Patterns worth memorizing
| Intent | Pattern sketch |
| --- | --- |
| Node only | `(n:Label)` |
| Directed edge | `(a)-[r:TYPE]->(b)` |
| Any direction | `(a)-[r:TYPE]-(b)` |
| Variable path | `(a)-[:TYPE]->{1,3}(b)` |
| Disjoint match | `MATCH ..., MATCH ...` then join in `FILTER`/`RETURN` |

## RETURN discipline
- Project **only** what the caller needs.
- Alias aggressively (`AS`).
- Aggregate in `RETURN` (`count`, `collect`, `sum`) after patterns are constrained.
- Order with `ORDER BY`, slice with `LIMIT` / `OFFSET` (or dialect equivalents).

## Write ops (use sparingly)
- Insert: `INSERT` / `CREATE` (dialect-dependent keyword).
- Set props: `SET n.prop = value`.
- Delete: detach-delete relationships before nodes when the store requires it.
- Never mix exploratory wide `MATCH` with writes without a tight `FILTER`.

## Safety checklist
1. Is the match cardinality bounded (label + property / limit)?
2. Are relationship directions intentional?
3. Will `RETURN *` or unbounded variable-length paths explode?
4. Are parameters used instead of string-concatenated values?

## Parameters
```gql
MATCH (n:Item { id: $id })
RETURN n
```

## When dialects differ
- **Cypher**: often `WHERE` instead of `FILTER`; `CREATE`/`MERGE` common for writes.
- **GQL**: lean on standard `MATCH` + `FILTER` + `RETURN`; confirm vendor docs for write syntax and path quantifiers.
- If the target engine is unclear, write portable read queries first, then adapt writes.

## Deliverable style
1. One correct query (copy-pasteable).
2. One-line assumption about labels/types.
3. Optional tighter variant if the first is exploratory.

## Related
- Path depth / reachability: [gql-path-patterns](../gql-path-patterns/SKILL.md)
- MemNet agent wire: [memnet-format](../memnet-format/SKILL.md), [mcp-memnet](../mcp-memnet/SKILL.md)
- SysML modeling + MemNet: [sysml-gql](../sysml-gql/SKILL.md)
