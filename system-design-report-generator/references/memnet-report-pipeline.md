# System design report — MemNet pipeline

Use when **generating**, **scaffolding**, or **maintaining** a `system-design-report/` pack. Pair with [sysml-memnet-documentation](../../sysml-memnet-documentation/SKILL.md) and [sysml-memnet-patterns.md](../../sysml-memnet-documentation/references/sysml-memnet-patterns.md).

## Three stores (report turn)

| Store | Authority | Report rule |
|-------|-----------|-------------|
| `models/*.sysml` | Structure, links, requirements | **Source** for section content |
| `outputs/system-design-report/*.md` | Human-readable narrative | **Derived** — tables/diagrams from model |
| MemNet `:ART` / `:SEC` / `:CLM` | Claim index, section map, cross-links | **Atomised facts** -- not full prose |

**Do not** duplicate topology tables in MemNet; **do** atomise one fact per `:CLM` and link to `:CON` / `:PRT` / `:REQ` via typed relationships.

## Prerequisites

1. `serve_status`. If `running: false`, generate report from warm miss grep only; pipeline steps use plain Markdown in-prompt; skip MemNet write.
2. Read **`AGENT-CONTEXT.md`** — session id, anchor (`TSK_model_<short>`), cross-artifact `ART_*` (manuals).
3. **`pin_map(anchor=TSK_model_<short>, depth=2, max_rows=80)`** — prefer warm rows over memory for part/link/req names.

**Remote serve:** when `MEMNET_SERVE_HOST` is not localhost, local `memnet session load --file` may fail (path on dev machine only). Push wire via repo `tools/memnet_push_wire.py` with `MEMNET_SERVE_HOST` set (see project `AGENT-CONTEXT.md`).

## Generate pack (greenfield or first report)

| Step | Action | MemNet |
|------|--------|--------|
| **G0** | `serve_status` | `@CLM` `G0:serve` |
| **G1** | `pin_map(TSK_model_<short>)`. Warm miss → run initial model snap ([sysml-memnet-snap.md](../../sysml-memnet-documentation/references/sysml-memnet-snap.md) §Initial snap) before prose. | READ + `@CLM` `G1:warm_*` |
| **G2** | Hub `index.md` + `config.yaml` load order only. Deploy file list from warm `@MOD_*` — not full deploy read. | `@CLM` `G2:hub` |
| **G3** | Create `outputs/system-design-report/` + hub `index.md` with `llm_toc`, optional `memnet:` block (below). | `@CLM` `G3:scaffold` |
| **G4** | Write section files **from model + warm graph**: exact `link*` names, `@REQ` ids, `@BEH` action names. One `##` per `llm_toc` entry. | `@CLM` `G4:sections` |
| **G5** | **sysml-view-doc-sync** — Mermaid per interconnection rules; `mmdc` if rendering. | `@CLM` `G5:mmdc` |
| **G6** | Atomise report graph (§Report atomisation). | WRITE + `@CLM` `G6:*` |
| **G7** | Update `outputs/README.md` pointer; thin `AGENT-CONTEXT.md` if missing. | `@CLM` `G7:done` + settle `TSK_report_*` |

**Pipeline wire:** parent `TSK_report_<short>` + `@CLM` type=`pipe` per G/M step — [sysml-memnet-pipeline.md](../../sysml-memnet-documentation/references/sysml-memnet-pipeline.md). Prefer wire rows over chat-only scratch when serve is up.

## Maintain pack (after deploy edit)

Follow [sysml-modeling-workflow](../../sysml-modeling-workflow/SKILL.md) steps 1–4 first (warm → edit → validate).

| Step | Action | MemNet |
|------|--------|--------|
| **M1** | `query_warm` on touched `@PRT`/`@CON`/`@REQ`/`@BEH` | READ + `@CLM` `M1:warm` |
| **M2** | Open hub → **one** section `file` from `llm_toc` for the changed topic only | `@CLM` `M2:sec_*` |
| **M3** | Patch section from warm `@CON`/`@PRT`/`@REQ` + narrow deploy grep at `@SYM.line`; sync Mermaid in owning section | `@CLM` `M3:patch` |
| **M4** | Model delta already written in modeling step 6 | `@CLM` `M4:model_delta` |
| **M5** | Update/add `@SEC`/`@CLM` for changed claims; `mentions` EDG to model ids | WRITE + `@CLM` `M5:*` |

## Hub `memnet:` block (optional, recommended)

In the same YAML fence as `llm_toc` (or adjacent fence):

```yaml
memnet:
  anchor: TSK_model_vfdl2
  art_id: ART_vfdl2-design
  session: mn_3555a9ec   # from AGENT-CONTEXT; omit if unknown
  cross_artifacts:
    - art_id: ART_asco8262
      session: mn_0aa36317
      note: de-facto valve manual
```

Agents: **`pin_map(art_id)`** or **`pin_map(anchor)`** before opening section files when serve is up.

## `:ART` / `:SEC` / `:CLM` mapping

**One report pack -> one `:ART`:**

```cypher
CREATE (a:ART {id: 'ART_vfdl2-design', title: 'VFDL2 system design', source: 'outputs/system-design-report/index.md', kind: 'report', status: 'active', recycle: 'persistent'})
CREATE (:TSK {id: 'TSK_model_vfdl2'})-[:OWNS {id: 'NEW', note: 'scope', recycle: 'persistent'}]->(a)
```

**Each `llm_toc` entry -> one `:SEC`:**

| Hub field | MemNet row |
|-----------|------------|
| `llm_toc[].id` | `:SEC.id` suffix (e.g. `S02-interconnection`) |
| `llm_toc[].title` | `:SEC.heading` |
| list order (1-based) | `:SEC.order` |
| `llm_toc[].file` | `:CLM` / prose lives in that path -- store path on `:ART.source` only |

```cypher
CREATE (s1:SEC {id: 'S01', heading: 'Scope and sources', order: 1, status: 'active', recycle: 'persistent'})
CREATE (s4:SEC {id: 'S04', heading: 'Interconnection view', order: 4, status: 'active', recycle: 'persistent'})
CREATE (:ART {id: 'ART_vfdl2-design'})-[:CONTAINS {id: 'NEW', recycle: 'persistent'}]->(s4)
```

**Section content -> `:CLM` (one fact per row, <=15 words in `code`):**

| Section topic | Atomise as |
|---------------|------------|
| Interconnection table row | `:CLM` type=`fact` + `mentions` -> `:CON_<linkName>` |
| De-facto part (e.g. ASCO 8262) | `:CLM` type=`convention` + `mentions` -> `:PRT_valveController` + optional `dependsOn` -> `ART_asco8262` |
| Requirement summary row | `:CLM` type=`fact` + `mentions` -> `:REQ_<id>` |
| Open BOM gap | `:CLM` type=`assumption` or `:ISSUE` |
| Design choice in prose | `:DEC` if still open; `:CLM` type=`decision` when settled |

```cypher
CREATE (c:CLM {id: 'C81', type: 'fact', code: 'ValveController switched via relay4p2t twoPoleB', status: 'active', recycle: 'persistent'})
CREATE (c)-[:MENTIONS {id: 'NEW', note: 'subject', recycle: 'persistent'}]->(:CON {id: 'CON_linkRelay4p2tTwoPoleBToValveController'})
CREATE (c)-[:MENTIONS {id: 'NEW', note: 'subject', recycle: 'persistent'}]->(:PRT {id: 'PRT_valveController_vfdl2'})
```

**Do not** store Mermaid source or full markdown tables in `CLM.code`.

## Read strategy (token-efficient)

1. Hub `index.md` only (~80 lines).
2. `pin_map(TSK_model_<short>, depth=2)` — structural facts (**primary**).
3. **One** section `file` for the task.
4. Narrow `Read` at `@SYM.line` or **one** scoped `Grep` if warm row missing or line drift suspected.
5. Cross-manual: `pin_map(ART_<manual>, depth=1)` — do not load PDF into chat.

**Do not** read full `deploy-*.sysml` to refresh report tables when warm has `@CON`/`@PRT`. See [sysml-memnet-read-policy.md](../../sysml-memnet-documentation/references/sysml-memnet-read-policy.md).

## llm_keywords ↔ MemNet

Hub `llm_keywords` route agents to **section ids**; MemNet `@PRT`/`@CON`/`@REQ` ids route to **model atoms**. Keep both:

```yaml
llm_keywords:
  relay4p2t: relay-valve-chain
  linkGs305epUplinkToTopLevelSwitch: interconnection-view
```

Add MemNet-only lookups via warm on `PRT_relay4p2t`, `CON_linkGs305epUplinkToTopLevelSwitch`.

## Incremental report snap (after large generate)

Batch `add` 20–60 lines:

1. `@ART` + `@SEC` rows for all hub sections
2. Top **N** `@CLM` facts per section (interconnection links, req ids, de-facto parts, behaviour names)
3. `@EDG`: `owns`, `contains`, `mentions`, `documents` (CLM → SEC → ART → TSK)

Optional: write wire to `projects/<slug>/.memnet/report-wire.txt`; push with `memnet_push_wire.py` if serve is remote.

**Do not** paste wire into chat.

## Validation order

```
.sysml validate (mcp-sysml-v2) → section .md sync → mmdc (if diagrams) → MemNet report delta
```

Report markdown **must not** invent structure absent from validate-passing model.

## AGENT-CONTEXT.md

After first report + MemNet atomisation, ensure project stub lists:

- `TSK_model_<short>`, session id, serve host if non-default
- One line: `ART_<short>-design` for report pack
- Cross-artifact `ART_*` (manuals) — **not** duplicated topology

Max 40 lines — see [sysml-memnet-snap.md](../../sysml-memnet-documentation/references/sysml-memnet-snap.md) §AGENT-CONTEXT.
