# MemNet for article breakdown

Use MemNet to **atomise a long article** (paper, report, blog, spec, **instrument manual**) into a knowledge graph — one **claim/fact per row**, sections as nodes, **`query_warm`** to load only the slice you need for summarising, comparing, or writing derived content.

**Do not** store the full article text in the graph. Store **structure + atomic claims** (codes/keys). Prose summaries are generated in the agent turn from warm atoms.

Pair with [atomisation.md](atomisation.md) and [wire-format.md](wire-format.md).

**Full instrument-manual / SCPI pattern:** see MemNet repo [`application-notes/llm-tech-docs-decomposition.md`](../../../../Projects/MemNet/application-notes/llm-tech-docs-decomposition.md) — `@CMD` rows, procedure layers, RTO remote-mode worked example.

## When to use

| Situation | Use MemNet? |
|-----------|-------------|
| Long article; summarise section-by-section across turns | **Yes** |
| Compare claims across sections or two papers | **Yes** — `@CLM` + `supports` / `contradicts` edges |
| Cross-check article against your project (code, SysML) | **Yes** — link `@CLM` to `@SYM` / `@REQ` via `@EDG` |
| Instrument manual; drive SCPI remotely | **Yes** — extend map with `@CMD`; see [tech-docs note](../../../../Projects/MemNet/application-notes/llm-tech-docs-decomposition.md) |
| Read once, never reference again | **No** |
| Need exact verbatim quotes often | Store **short** `@CLM` code + source locator; not full paragraphs |

## Tag map (session_open map_lines)

```text
@ART: id|title|source|kind|status|recycle
@SEC: id|art|heading|order|status|recycle
@CLM: id|sec|type|code|status|recycle
@ENT: id|name|kind|code|recycle
@TSK: id|goal|deadline|status|recycle
@EDG: id|from|rel|to|note|recycle
```

| Tag | Role |
|-----|------|
| `@ART` | Document root (title, URL/file, `kind`: paper\|blog\|spec) |
| `@SEC` | Section — `heading` short, `order` numeric |
| `@CLM` | **One atomic claim** — `type`: fact\|stat\|method\|conclusion\|quote; `code` = distilled (≤ ~12 words) |
| `@ENT` | Entity — person, org, concept, metric (`kind` + short `code`) |
| `@TSK` | Analysis job — e.g. “summarise §3”, “extract methods” |
| `@EDG` | `contains`, `part_of`, `mentions`, `supports`, `contradicts`, `cites`, `owns` |

## Breakdown pipeline

```text
1. session_open(map_lines=[...])     # tag map above
2. add ART + TSK_breakdown
3. Per section:
     add SEC
     split into CLM rows (one idea each)
     add ENT for named entities
     add EDG: ART→SEC, SEC→CLM, CLM→ENT
4. Each turn: query_warm(anchor=SEC_xx or TSK_xx)
5. Generate summary / synthesis from warm slice only
6. settle TSK when article pass is done
```

## Example — bad vs good

**Bad** (whole article in one row — destroys token efficiency):

```text
@ART: A01|MemNet paper|memnet.md|spec|active|persistent
@NOTE: N01|body|MemNet is a goldfish brain graph. You query warm. Atomisation matters. MCP uses serve...|persistent
```

**Good** (hierarchy + atoms):

```text
@ART: A01|MemNet agent memory|README.md|doc|active|persistent
@TSK: TSK_read|Break down README|1|in_progress|persistent
@SEC: S01|A01|Goldfish loop|1|active|persistent
@SEC: S02|A01|Wire format|2|active|persistent
@CLM: C01|S01|fact|external graph not chat|active|persistent
@CLM: C02|S01|method|query_warm anchored read|active|persistent
@CLM: C03|S02|fact|pipe TAG rows not JSON|active|persistent
@CLM: C04|S02|fact|atomisation required|active|persistent
@ENT: E01|query_warm|concept|anchor_read|persistent
@ENT: E02|EDG|concept|graph_edge|persistent
@EDG: X01|TSK_read|owns|A01|scope|persistent
@EDG: X02|A01|contains|S01|struct|persistent
@EDG: X03|A01|contains|S02|struct|persistent
@EDG: X04|S01|contains|C01|claim|persistent
@EDG: X05|S01|contains|C02|claim|persistent
@EDG: X06|S02|contains|C03|claim|persistent
@EDG: X07|S02|contains|C04|claim|persistent
@EDG: X08|C02|mentions|E01|term|persistent
@EDG: X09|C04|mentions|E02|term|persistent
```

## MCP: open + ingest one section

```json
session_open(map_lines=[
  "@ART: id|title|source|kind|status|recycle",
  "@SEC: id|art|heading|order|status|recycle",
  "@CLM: id|sec|type|code|status|recycle",
  "@ENT: id|name|kind|code|recycle",
  "@TSK: id|goal|deadline|status|recycle",
  "@EDG: id|from|rel|to|note|recycle"
])
```

```json
add(wire_lines=[
  "@ART: A01|Design report §3|outputs/design.md|report|active|persistent",
  "@TSK: TSK_s3|Summarise section 3|1|in_progress|persistent",
  "@SEC: S03|A01|Power budget|3|active|persistent",
  "@CLM: C31|S03|stat|peak 120W at launch|active|persistent",
  "@CLM: C32|S03|fact|battery 400Wh nominal|active|persistent",
  "@CLM: C33|S03|conclusion|margin 15% at P99|active|persistent",
  "@ENT: EN1|PDU|component|power_unit|persistent",
  "@EDG: X31|TSK_s3|owns|S03|focus|persistent",
  "@EDG: X32|A01|contains|S03|struct|persistent",
  "@EDG: X33|S03|contains|C31|claim|persistent",
  "@EDG: X34|S03|contains|C32|claim|persistent",
  "@EDG: X35|S03|contains|C33|claim|persistent",
  "@EDG: X36|C31|mentions|EN1|subject|persistent"
])
```

Next turn — summarise **only** section 3:

```json
query_warm(anchor="S03", depth=2)
```

Returns `@LAW` + `S03` + linked `CLM` + `ENT` — not sections 1–2.

## Cross-section reasoning

Link claims across sections with `@EDG`:

```text
@CLM: C10|S01|fact|assumed ambient 25C|active|persistent
@CLM: C40|S04|stat|measured ambient 32C|active|persistent
@EDG: X40|C40|contradicts|C10|measurement|persistent
@EDG: X41|C40|mentions|C10|revises|persistent
```

Warm anchor `C40` → both claims if edge-linked within depth.

## Link article to project work

Bridge reading to coding or SysML:

```text
@CLM: C50|S05|requirement|SHALL log power each orbit|active|persistent
@REQ: REQ_PWR|orbit|SHALL log power|active|persistent
@EDG: X50|C50|maps_to|REQ_PWR|trace|persistent
@EDG: X51|TSK_sysml|informed_by|C50|article|persistent
```

## Quote handling

Store **locator + short code**, not block quotes:

```text
@CLM: C99|S02|quote|warm not context|active|persistent
```

If verbatim text is required occasionally, keep it outside MemNet or in a file; the graph holds **where** and **what kind**, not the full quote.

## Anchors

| Anchor | Use for |
|--------|---------|
| `TSK_read` | Whole breakdown job + linked `@ART` |
| `S03` | One section’s claims |
| `C31` | Single claim + neighbours |
| `ENT` id | All claims mentioning an entity (via `mentions` edges) |

## Limits

- Re-read source when precision matters — atoms are **your distillation**, not OCR
- Very long papers: one `@SEC` per H2/H3, not per paragraph
- Settle `TSK_read` when breakdown pass is complete; keep `@ART`/`@CLM` if still citing later

## Instrument manual / SCPI remote mode

For PDF user manuals (oscilloscopes, spectrum analysers, etc.), extend the tag map with `@CMD`:

```text
@CMD: id|sec|scpi|role|params_code|status|recycle
```

One SCPI command per row; `scpi` field uses **mixed-case long+short** canonical form (e.g. `:CHANnel1:SCALe`, `:MEASurement1:RESult?`). Wire automation order with `@CLM type=procedure` + `precedes` / `requires` EDGs.

Mini example:

```text
@CMD: CMD_idn|S_cmd_common|*IDN?|query|-|active|persistent
@CMD: CMD_run|S_acq_remote|:RUN|set|-|active|persistent
@CLM: CLM_capture_seq|S_acq_remote|procedure|acq_mode_run_opc|active|persistent
@EDG: E_cap_1|CLM_capture_seq|precedes|CMD_run|step2|persistent
```

Full walkthrough (R&S RTO rev 29, **4 584 `@CMD` full dictionary**, hello + capture/measure turns): MemNet [`application-notes/llm-tech-docs-decomposition.md`](../../../../Projects/MemNet/application-notes/llm-tech-docs-decomposition.md). Regenerate: `python scripts/extract_rto_scpi.py`.

Cross-ref: [atomisation.md](atomisation.md) · [user-input-memory.md](user-input-memory.md) · [coding-memory.md](coding-memory.md)
