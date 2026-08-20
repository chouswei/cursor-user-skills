# SysML MemNet -- cookbook bridge (user pack)

Links user-pack MemNet skills to the upstream SysML v2 modeling cookbook. **Do not copy the full cookbook here** -- use this bridge for policy and pointers.

## Upstream source

**Path:** MemNet `docs/application-notes/system/llm-sysml-v2-modeling.md` (do not use leftover root `application-notes/`).

**Package 0.19.2** (tag `v0.19.2`; extras 0.10-0.19 unchanged). **PyPI wheel** still **`memnet-llm==0.19.0`** until twine. **Install:** `pip install memnet-llm==0.19.0` **or** git / `v0.19.2`. Do **not** `pip install memnet-llm==0.19.1` or `==0.19.2` as the current wheel. **1.0** unclaimed.

The cookbook defines worked multi-turn examples, relation vocabulary, and batch sizing. User-pack skills **MUST** follow the canonical tag map in [sysml-memnet-patterns.md](sysml-memnet-patterns.md) -- not legacy alias tags from older cookbook drafts.

## Unified-tag policy (fixed)

| Rule | Detail |
|------|--------|
| Part / port / behaviour | Single tags `@PRT`, `@POR`, `@BEH` with **`kind`** field |
| **MUST NOT** write | `@PARTD`, `@PORTD`, `@BEHD`, `@TASK` in new rows |
| Warm miss over legacy graph | Re-snap into unified tags (full section Initial snap in [sysml-memnet-snap.md](sysml-memnet-snap.md)) |
| satisfy / allocate | **`@EDG` only** (`satisfies`, `allocates`); `@SYM` kind=`satisfy`/`allocate` only when line locator needed |

## Load order (agents)

1. [sysml-memnet-snap.md](sysml-memnet-snap.md) -- mandatory 6-step turn sequence
2. [sysml-memnet-read-policy.md](sysml-memnet-read-policy.md) -- when to read `.sysml` vs warm
3. [sysml-memnet-pipeline.md](sysml-memnet-pipeline.md) -- pipeline wire (`@CLM` type=`pipe`)
4. [sysml-memnet-patterns.md](sysml-memnet-patterns.md) -- canonical map, construct table, EDG list
5. **This file** -- upstream pointer + legacy ban
6. Cookbook (upstream) -- worked turns when pattern/snap insufficient

## What stays in user pack vs cookbook

| Topic | User pack | Cookbook |
|-------|-----------|----------|
| Turn sequence, warm miss, line drift | snap.md | -- |
| Read budget, anti-patterns (no deploy re-read) | read-policy.md | -- |
| Pipeline step wire (`@CLM` type=`pipe`) | pipeline.md | -- |
| 19-tag map, id rules, kind enums | patterns.md | aligned |
| Per-file grep, delta matrix | snap.md | examples |
| Multi-turn dialogue examples | -- | full turns |
| MemNet CLI / MCP tool params | mcp-memnet skill | section Tools |

## Reconciliation checklist

When cookbook and user pack disagree:

1. **Tag names** -- user pack wins (`@POR` not `@PORT`; no `@PARTD`)
2. **Field order** -- canonical map in patterns.md wins
3. **Batch EDG rules** -- patterns construct table wins
4. **Worked examples** -- cookbook for narrative; rewrite examples to unified tags when copying into MemNet

## Session persistence

Cookbook section Snapshot -> [sysml-memnet-snap.md](sysml-memnet-snap.md) section Session `.snap` file. Never paste snap file contents into chat.

## Related skills

- [sysml-memnet-documentation/SKILL.md](../SKILL.md) -- hub
- [memnet-format](../../memnet-format/SKILL.md) -- wire-format cheat sheet
- [sysml-new-project](../../sysml-new-project/SKILL.md) -- step 12 session_open map
