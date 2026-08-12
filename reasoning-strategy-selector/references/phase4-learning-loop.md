# Phase 4 — Learning loop (`led_to_success`)

**Status:** activated. Graph routing reads empirical edges; parent agent writes on settle.

## Goal

Strengthen routing edges from empirical outcomes: `TSK_route_* -[:LED_TO_SUCCESS]-> SKL_<id>` (openCypher-shaped mutate).

## Write ownership

| Actor | Responsibility |
|-------|----------------|
| **Parent agent** | On task settle, emit `led_to_success` edges via `memnet.add` (not the selector) |
| **Selector** | Read-only writer; ranks existing `led_to_success` edges (+0.6 weight per edge) |
| **memnet-goldfish-loop** | [memnet-goldfish-loop.mdc](~/.cursor/rules/memnet-goldfish-loop.mdc) — settle hook |

## Success signal (default)

Downstream skill output includes `pass: true`, or task completed without error.

## Recycle policy

| Tag | recycle |
|-----|---------|
| `TSK_route_*` | `delete_on_settle` |
| `led_to_success` | `persistent` (note field may hold `pass` or frequency) |

## Helper

```bash
python tools/record_routing_success.py TSK_route_<slug> <skill-id> [more-ids...]
```

Paste output into `memnet.add` with `allow_new_relation=true`.

### Settle example (store write; not always-on rule body)

When `reasoning-strategy-selector` `order[]` succeeds, **parent** writes openCypher-shaped mutate (GQL wire):

```cypher
CREATE (:TSK {id: $tid})-[:LED_TO_SUCCESS {id: 'NEW', note: 'pass', recycle: 'persistent'}]->(:SKL {id: $skillId})
```

(Engine seed / import may still use compact store rows; do not teach pipe `@EDG:` as agent I/O.)

## Validation

- `led_to_success` dst must be existing `@SKL` id (`record_routing_success.py` checks seed)
- Bootstrap `--sync` emits seed rows only — **merge** into MemNet; never delete empirical edges

## Activation checklist

- [x] memnet-goldfish-loop updated with settle hook
- [x] Selector SKILL.md cites protocol (pipeline step 6)
- [x] `route_graph()` applies `led_to_success` rank boost
- [x] `record_routing_success.py` helper
- [ ] Golden set re-run after 10+ empirical edges collected (ongoing)
- [x] Graph-only routing remains default (no convolution)
