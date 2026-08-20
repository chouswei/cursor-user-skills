# MemNet for article breakdown

Use MemNet to **atomise a long article** into a knowledge graph -- one claim per node, **`pin_map`** to load only the slice you need.

**Do not** store the full article text in the graph. Store **structure + atomic claims** (codes/keys). Prose summaries are generated in the agent turn from pin-map atoms.

Agent I/O is the **GQL wire** (shaped pin_map + openCypher-shaped mutate) only. Do **not** emit pipe `@TAG:...` rows as mutate input.

Pair with [atomisation.md](atomisation.md) and [wire-format.md](wire-format.md).

**Full instrument-manual / SCPI pattern:** see MemNet repo `docs/application-notes/domains/llm-tech-docs-decomposition.md` -- `CMD` rows, procedure layers, RTO remote-mode worked example.

## When to use

| Situation | Use MemNet? |
|-----------|-------------|
| Long article; summarise section-by-section across turns | **Yes** |
| Compare claims across sections or two papers | **Yes** -- `CLM` + `supports` / `contradicts` edges |
| Cross-check article against your project (code, SysML) | **Yes** -- link `CLM` to `SYM` / `REQ` via edges |
| Instrument manual; drive SCPI remotely | **Yes** -- extend map with `CMD`; see tech-docs note above |
| Read once, never reference again | **No** |
| Need exact verbatim quotes often | Store **short** `CLM` code + source locator; not full paragraphs |

## Tag map (session_open map_lines)

Map lines declare kind schemas (field names). Prefer shared-dialect style keys:

```text
SCHEMA ART ; fields=title source kind status recycle
SCHEMA SEC ; fields=heading order status recycle
SCHEMA CLM ; fields=type code status recycle
SCHEMA ENT ; fields=name kind code recycle
SCHEMA TSK ; fields=goal deadline status recycle
```

| Kind | Role |
|------|------|
| `ART` | Document root (title, URL/file, `kind`: paper\|blog\|spec) |
| `SEC` | Section -- `heading` short, `order` numeric |
| `CLM` | **One atomic claim** -- `type`: fact\|stat\|method\|conclusion\|quote; `code` = distilled (<= ~12 words) |
| `ENT` | Entity -- person, org, concept, metric (`kind` + short `code`) |
| `TSK` | Analysis job -- e.g. "summarise section 3", "extract methods" |
| `EDG` | `contains`, `part_of`, `mentions`, `supports`, `contradicts`, `cites`, `owns` |

## Breakdown loop

```text
1. session_open(map_lines=[...])
2. mutate ART + TSK_breakdown (GQL / openCypher-shaped)
3. Per section:
     mutate SEC
     split into CLM rows (one idea each)
     mutate ENT for named entities
     mutate edges: ART->SEC, SEC->CLM, CLM->ENT
4. Each turn: pin_map(kind='SEC', locators=['heading=...'])  # or TSK by goal
5. Generate summary / synthesis from pin-map slice only
6. settle TSK when article pass is done
```

## Example -- bad vs good

**Bad** (whole article in one row -- destroys token efficiency):

```cypher
CREATE (:ART {title: 'MemNet paper', source: 'memnet.md', kind: 'spec'})
CREATE (:CLM {type: 'blob', code: 'MemNet is a goldfish brain graph. You query warm. Atomisation matters...'})
```

**Good** (hierarchy + atoms):

```cypher
CREATE (:ART {title: 'MemNet agent memory', source: 'README.md', kind: 'doc'})
CREATE (:TSK {goal: 'Break down README', status: 'in_progress'})
CREATE (:SEC {heading: 'Goldfish loop', order: 1})
CREATE (:SEC {heading: 'Wire format', order: 2})
CREATE (:CLM {type: 'fact', code: 'external graph not chat'})
CREATE (:CLM {type: 'method', code: 'pin map from a cue'})
CREATE (:ENT {name: 'pin_map', kind: 'concept', code: 'primary_read'})
MATCH (a:ART {title: 'MemNet agent memory'}), (s:SEC {heading: 'Goldfish loop'})
CREATE (a)-[:contains {note: 'struct'}]->(s)
MATCH (s:SEC {heading: 'Goldfish loop'}), (c:CLM {code: 'pin map from a cue'})
CREATE (s)-[:contains {note: 'claim'}]->(c)
MATCH (c:CLM {code: 'pin map from a cue'}), (e:ENT {name: 'pin_map'})
CREATE (c)-[:mentions {note: 'term'}]->(e)
```

Cue the next turn by labels+properties. leftover `[NEW]` mint is leftover.

## MCP: open + ingest one section

```text
session_open(map_lines=[
  "SCHEMA ART ; fields=title source kind status recycle",
  "SCHEMA SEC ; fields=heading order status recycle",
  "SCHEMA CLM ; fields=type code status recycle",
  "SCHEMA ENT ; fields=name kind code recycle",
  "SCHEMA TSK ; fields=goal deadline status recycle"
])
```

```cypher
CREATE (:ART {title: 'Design report section 3', source: 'outputs/design.md', kind: 'report', recycle: 'persistent'})
CREATE (:TSK {goal: 'Summarise section 3', status: 'in_progress', recycle: 'persistent'})
CREATE (:SEC {heading: 'Power budget', order: 3, recycle: 'persistent'})
CREATE (:CLM {type: 'stat', code: 'peak 120W at launch', recycle: 'persistent'})
CREATE (:CLM {type: 'fact', code: 'battery 400Wh nominal', recycle: 'persistent'})
CREATE (:ENT {name: 'PDU', kind: 'component', code: 'power_unit', recycle: 'persistent'})
MATCH (a:ART {title: 'Design report section 3'}), (s:SEC {heading: 'Power budget'})
CREATE (a)-[:contains {note: 'struct'}]->(s)
MATCH (s:SEC {heading: 'Power budget'}), (c:CLM {code: 'peak 120W at launch'})
CREATE (s)-[:contains {note: 'claim'}]->(c)
```

Product write is **`mutate(wire_lines=...)`**. leftover `add` / `+ ART [NEW]` pipe named leftover.

Next turn -- summarise **only** section 3:

```text
pin_map(kind='SEC', locators=['heading=Power budget'], depth=2)
```

Returns LAW pins + that section + linked `CLM` / `ENT` -- not other sections. leftover `anchor=` named leftover.

## Cross-section reasoning

```cypher
CREATE (:CLM {type: 'fact', code: 'assumed ambient 25C', recycle: 'persistent'})
CREATE (:CLM {type: 'stat', code: 'measured ambient 32C', recycle: 'persistent'})
MATCH (a:CLM {code: 'measured ambient 32C'}), (b:CLM {code: 'assumed ambient 25C'})
CREATE (a)-[:contradicts {note: 'measurement'}]->(b)
```

Cue `pin_map` on the later claim -- both claims if edge-linked within depth.

## Link article to project work

```cypher
CREATE (:CLM {type: 'requirement', code: 'SHALL log power each orbit', recycle: 'persistent'})
CREATE (:REQ {requirementId: 'REQ_PWR', code: 'SHALL log power', recycle: 'persistent'})
MATCH (c:CLM {code: 'SHALL log power each orbit'}), (r:REQ {requirementId: 'REQ_PWR'})
CREATE (c)-[:maps_to {note: 'trace'}]->(r)
```

## Quote handling

Store **locator + short code**, not block quotes:

```cypher
CREATE (:CLM {type: 'quote', code: 'pin map not full context', recycle: 'persistent'})
```

If verbatim text is required occasionally, keep it outside MemNet or in a file; the graph holds **where** and **what kind**, not the full quote.

## Cues

| Cue | Use for |
|-----|---------|
| `kind=TSK` + `goal=` | Whole breakdown job + linked `ART` |
| `kind=SEC` + `heading=` | One section's claims |
| `kind=CLM` + `code=` | Single claim + neighbours |
| `kind=ENT` + `name=` | All claims mentioning an entity (via `mentions` edges) |

## Limits

- Re-read source when precision matters -- atoms are **your distillation**, not OCR
- Very long papers: one `SEC` per H2/H3, not per paragraph
- Settle the breakdown `TSK` when the pass is complete; keep `ART`/`CLM` if still citing later

## Instrument manual / SCPI remote mode

Extend the map with `CMD` (`SCHEMA CMD ; fields=scpi role params_code status recycle`). One SCPI command per row. leftover `+ CMD [NEW]` pipe named leftover.

```cypher
CREATE (:CMD {scpi: '*IDN?', role: 'query', recycle: 'persistent'})
CREATE (:CMD {scpi: ':RUN', role: 'set', recycle: 'persistent'})
CREATE (:CLM {type: 'procedure', code: 'acq_mode_run_opc', recycle: 'persistent'})
MATCH (p:CLM {code: 'acq_mode_run_opc'}), (c:CMD {scpi: ':RUN'})
CREATE (p)-[:precedes {note: 'step2'}]->(c)
```

Full walkthrough: MemNet `docs/application-notes/domains/llm-tech-docs-decomposition.md`.

Cross-ref: [atomisation.md](atomisation.md) * [user-input-memory.md](user-input-memory.md) * [coding-memory.md](coding-memory.md)
