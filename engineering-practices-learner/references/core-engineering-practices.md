# Engineering practices library (structured)

## Stable id (required)

- Format: **`ep-<facet>-<shortSlug>`** in lowercase kebab-case (e.g. `ep-deploy-feature-flags`, `ep-reliability-circuit-breaker`). **Facet** = primary tag or first taxonomy segment.
- **Immutable** once published to the corpus: do not rename ids; add a **refines** edge to a new id if guidance supersedes old.
- **Corpus lines:** starter bullets below start with **`id: <id> |`** so retriever output stays identifiable.
- **Relations:** `from_id` / `to_id` must match these ids (or ids from the same namespace in `entries`).

## Record shape (classify step)

Each practice: **id** (stable slug), **label** (short human title), **practice**, **conditions**, **observed_result**, **confidence** (high|med|low), **tags** (facets), optional **taxonomy_path** (ordered facets, coarse -> fine, e.g. reliability -> deploy).

## Classification and labeling

- **Tags** = search facets; **taxonomy_path** = where the practice sits in a small hierarchy (use 2-4 path segments max).
- **Label** = one line; must disambiguate from siblings under the same taxonomy_path.
- Prefer one **primary** taxonomy_path per entry; extra tags for cross-cutting concerns (security, perf).

## Relation edges (canonical types)

Use only these **type** strings in JSON `relations` (directed **from_id** -> **to_id**):

- **depends_on** - A is viable only if B is already true (infra, policy, prior practice).
- **prerequisite_of** - Do B before A in rollout or learning order (synonym-ish to depends_on but process-ordered).
- **refines** - A narrows, updates, or supersedes guidance in B (keep both ids; note what changed).
- **conflicts_with** - A and B pull different directions; name the **context** where each wins in `note`.
- **complements** - A and B reinforce each other; often applied together.
- **same_family** - Cluster / alias / variant; weak link for retrieval grouping.

Rules: **no orphan edges** (both ids must exist in `entries` or corpus); **acyclic** preferred for depends_on/prerequisite_of; **conflicts_with** must always carry a short **note**.

## Retrieval + relations (token cap)

- After keyword retrieval, expand **at most 5** extra items by **1-hop** edges from top hits only (follow depends_on, complements, conflicts_with first if present).

## Starter patterns (examples)

- id: ep-deploy-feature-flags | Feature flags + gradual rollout - Conditions: user-facing change, measurable error budget. Result: blast radius contained. Tags: deploy, reliability.
- id: ep-data-idempotent-workers | Idempotent workers + dedupe keys - Conditions: async jobs, double-submit risk. Result: safe retries. Tags: data, reliability.
- id: ep-api-contract-tests | Contract tests at boundaries - Conditions: multiple services, evolving APIs. Result: catch drift early. Tags: api, team_process.
- id: ep-reliability-structured-logs | Structured logs + trace id - Conditions: distributed system, incident response. Result: faster root cause. Tags: reliability, data.
- id: ep-team-small-prs | Small PRs + vertical slices - Conditions: large codebase, review bottleneck. Result: faster review, less rework. Tags: team_process.
- id: ep-reliability-circuit-breaker | Circuit breaker on flaky deps - Conditions: external dependency, cascading failure risk. Result: protect core path. Tags: reliability, api.

## Anti-patterns

- Missing or duplicate **id** across entries.
- Tags without taxonomy_path when hierarchy matters for disambiguation.
- **conflicts_with** without **note** (which context picks which side).
- Graphs deeper than **1-hop** in retrieval expansion (token blow-up).

## Export to a dedicated skill (tool-wrapper is common)

- When a **closed set** of practices is stable: copy **ids + conditions + results + relations** into a new skill's `references/core-*-principles.md` (one bullet per practice, keep **`id:`** prefix for traceability).
- **Review** the draft with **skill-reviewer**, then **scaffold** with **skill-creator** (`metadata.pattern: tool-wrapper` unless you need a pipeline).
- Trim corpus to the **smallest** set that still covers the skill's `description` triggers; avoid pasting the whole learner library.

## Retrieval seeds

engineering practice, playbook, lessons learned, pattern library, taxonomy, label, relation, stable id, slug ep-, depends on, conflicts with, complements, knowledge graph, classify practice, tags, conditions, observed outcome, confidence
