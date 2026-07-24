# Atomisation — knowledge graph discipline

MemNet is an **in-memory knowledge graph**: **nodes** + **edges**. Prefer **Tier A** for agent mutate; legacy `@TAG:` / `@EDG:` pipe remains accepted. **`query_warm`** (live **pin map**) traverses edges from an anchor and returns only the connected **atoms** — not the whole store.

**Atomisation is the most important step.** If you dump paragraphs, merged facts, or whole subsystems into one row, warm reads bloat, ids collide, and the graph stops behaving like a graph.

## Core rules

1. **One idea per row** — one function, one constraint, one fact, one task phase
2. **Wire with `@EDG`** — relationships are explicit (`calls`, `owns`, `constrained_by`, `defines`, …)
3. **Short fields only** — ids, paths, line numbers, codes, keys; **no prose blobs**
4. **Split compound state** — if a field needs “and also …”, add another row + edge
5. **Stable ids** — reuse the same id forever; `update` when the atom changes

Bad: one `@MOD` row whose summary is a paragraph of architecture.  
Good: `@MOD` + several `@SYM` rows + `@EDG` linking task → modules → symbols.

## Why it matters for warm reads

```text
query_warm(anchor=TSK_x, depth=2)
  → @LAW rows (always)
  → anchor node
  → EDG-linked neighbours up to depth
  → NOT unrelated atoms elsewhere in the graph
```

Dense monolithic rows force everything into one anchor or tempt bare context reads. Atomisation keeps each turn’s slice **small and relevant** — the wire format stays **token-efficient**. See [wire-format.md](wire-format.md).

## Atomisation by domain

| Domain | Node tags | Edge examples |
|--------|-----------|---------------|
| **Coding** | `@MOD`, `@SYM`, `@TSK`, `@USR` | `defines`, `calls`, `owns`, `constrained_by` |
| **User input** | `@USR` | `constrained_by` from `@TSK` |
| **SysML / models** | `@PKG`, `@PRT`, `@REQ`, … | `declaredIn`, `satisfy`, `connects` |
| **Article breakdown** | `@ART`, `@SEC`, `@CLM`, `@ENT` | `contains`, `part_of`, `mentions`, `contradicts` |
Domain tag maps live in MemNet `docs/application-notes/` and product examples — still **one fact per row**. Novel-writer extras are out of scope.

## MCP write pattern

Prefer **one `add` call, many atom lines**:

```json
add(wire_lines=[
  "@TSK: TSK_api|Expose send_command|1|in_progress|persistent",
  "@MOD: MOD_serve|src/memnet/serve.py|TCP serve|active|persistent",
  "@SYM: SYM_send_command|send_command|fn|src/memnet/serve.py|96|send_command(argv,...)|active|persistent",
  "@EDG: E01|TSK_api|owns|MOD_serve|scope|persistent",
  "@EDG: E02|MOD_serve|defines|SYM_send_command|handler|persistent"
])
```

Five atoms + edges — not one row containing “serve.py has send_command for API work”.

---

## Examples — bad vs good

### 1. Coding: one blob vs atoms

**Bad** (one row, warm pulls everything always):

```text
@NOTE: N01|Architecture|MemNet MCP uses serve.py send_command over TCP stdin; cli.py session_current now takes --session; user wants Pi on LAN|persistent
```

**Good** (query `TSK_mcp` → only linked atoms):

```text
@TSK: TSK_mcp|MCP LAN + session fix|1|in_progress|persistent
@MOD: MOD_serve|src/memnet/serve.py|TCP host|active|persistent
@MOD: MOD_cli|src/memnet/cli.py|CLI|active|persistent
@SYM: SYM_send|send_command|fn|src/memnet/serve.py|96|send_command(argv,stdin?)|active|persistent
@SYM: SYM_sess_cur|session_current|fn|src/memnet/cli.py|307|session_current(session?)|active|persistent
@USR: USR_host|deploy|serve on rpi5-syson LAN|active|persistent
@EDG: E01|TSK_mcp|owns|MOD_serve|scope|persistent
@EDG: E02|TSK_mcp|owns|MOD_cli|scope|persistent
@EDG: E03|MOD_serve|defines|SYM_send|handler|persistent
@EDG: E04|MOD_cli|defines|SYM_sess_cur|handler|persistent
@EDG: E05|TSK_mcp|constrained_by|USR_host|user|persistent
@EDG: E06|SYM_send|uses|MOD_serve|defined_in|persistent
```

---

### 2. Call graph (who calls whom)

Do not put “A calls B calls C” in one field — **one `@EDG` per call**:

```text
@SYM: SYM_run_memnet|run_memnet|fn|src/memnet_mcp/client.py|98|run_memnet(...)|active|persistent
@SYM: SYM_probe|probe|fn|src/memnet/serve.py|126|probe(...)|active|persistent
@SYM: SYM_send_cmd|send_command|fn|src/memnet/serve.py|94|send_command(...)|active|persistent
@EDG: E10|SYM_run_memnet|calls|SYM_probe|if serve up|persistent
@EDG: E11|SYM_run_memnet|calls|SYM_send_cmd|production path|persistent
@EDG: E12|TSK_mcp|owns|SYM_run_memnet|trace|persistent
```

Warm anchor `TSK_mcp` depth 2 → task + client + callees without unrelated modules.

---

### 3. User message → several `@USR` atoms

**User said:** “British English, don’t commit unless I ask, only touch memnet_mcp and docs.”

**Bad:** one `@USR` with the whole sentence.

**Good:**

```text
@USR: USR_lang|style|British English|active|persistent
@USR: USR_git|commit|only when user asks|active|persistent
@USR: USR_scope|files|memnet_mcp + docs only|active|persistent
@EDG: E20|TSK_docs|constrained_by|USR_lang|user|persistent
@EDG: E21|TSK_docs|constrained_by|USR_git|user|persistent
@EDG: E22|TSK_docs|constrained_by|USR_scope|user|persistent
```

User revises scope → **`update`** `USR_scope` only; other atoms unchanged.

---

### 4. Pipeline steps (orchestrator)

Parent task + **one `@TSK` per step** + `@STEP`-style focus via edges (coding map uses `@TSK` + `goal` field):

```text
@TSK: TSK_pipeline|Refactor auth module|6|in_progress|persistent
@TSK: TSK_s1|Map call sites|1|settled|delete_on_settle
@TSK: TSK_s2|Extract interface|2|in_progress|persistent
@TSK: TSK_s3|Update tests|3|pending|delete_on_settle
@EDG: E30|TSK_pipeline|has_step|TSK_s1|done|delete_on_settle
@EDG: E31|TSK_pipeline|has_step|TSK_s2|current|persistent
@EDG: E32|TSK_pipeline|has_step|TSK_s3|next|delete_on_settle
@MOD: MOD_auth|src/auth/service.py|auth core|active|persistent
@EDG: E33|TSK_s2|owns|MOD_auth|focus|persistent
```

Step 2 done → `update` `TSK_s2` to `settled` + `recycle=delete_on_settle`; warm no longer pulls settled step unless anchored.

---

### 5. Bug investigation (transient + persistent)

**Persistent** (keep finding): root cause module/symbol. **Transient** (settle when fixed): repro notes, hypothesis.

```text
@TSK: TSK_bug|Fix warm empty stdout|1|in_progress|persistent
@SYM: SYM_warm|query_warm|fn|src/memnet_mcp/server.py|81|query_warm(...)|active|persistent
@TSK: TSK_hyp|Hypothesis: Pi on 0.2.6 no stdin|1|in_progress|delete_on_settle
@USR: USR_repro|steps|add via MCP then warm PLR99|active|delete_on_settle
@EDG: E40|TSK_bug|owns|SYM_warm|symptom|persistent
@EDG: E41|TSK_bug|investigates|TSK_hyp|scratch|delete_on_settle
@EDG: E42|TSK_bug|constrained_by|USR_repro|user|delete_on_settle
```

Fixed → settle `TSK_hyp`, `USR_repro`; keep `SYM_warm` if still relevant to docs.

---

### 6. SysML-style atoms (minimal)

One requirement, one part, one port — not one “model paragraph” row:

```text
@PKG: PKG_PDU|pdu.deploy|deploy package|active|persistent
@REQ: REQ_01|pdu.power|SHALL limit inrush|active|persistent
@PRT: PRT_CTRL|PatController|controller part|active|persistent
@PRT: PORT_PWR|powerIn|port|active|persistent
@EDG: E50|PRT_CTRL|declaredIn|PKG_PDU|origin|persistent
@EDG: E51|PRT_CTRL|satisfies|REQ_01|design|persistent
@EDG: E52|PRT_CTRL|hasPort|PORT_PWR|ibd|persistent
@TSK: TSK_sysml|PDU model slice|1|in_progress|persistent
@EDG: E53|TSK_sysml|owns|PKG_PDU|scope|persistent
```

Anchor `REQ_01` → pulls satisfied part + package via EDG; unrelated PKG stays out.

Full maps: MemNet `application-notes/llm-sysml-v2-modeling.md`.

---

### 7. Novel / beat atoms (domain tags)

Prose lives in the **generated turn**; graph stores codes only:

**Bad:**

```text
@CHR: C01|Alice|protagonist|She is curious and fell through a rabbit hole yesterday|wondering|active|persistent
```

**Good:**

```text
@CHR: C01|Alice|prot|cur:3|wonder|active|persistent
@LORE: L01|rabbit_hole|place|under_hr|persistent
@RULE: R01|voice|scene|close_second|persistent
@SCN: S01|hall_of_doors|beat1|delete_on_settle
@EDG: E60|S01|features|C01|focus|delete_on_settle
@EDG: E61|S01|applies|R01|tone|delete_on_settle
@EDG: E62|C01|knows|L01|memory|persistent
```

Turn outcome as separate atoms (not one sentence in `@SCN`):

```text
@EVT: EV01|try|C01|S01|door_locked|delete_on_settle
@COST: CO01|C01|stress|patience|-1|delete_on_settle
@EDG: E63|EV01|costs|CO01|beat|delete_on_settle
```

---

### 8. Splitting “and also” in one fact

**User:** “Use pytest and pin mcp>=1.2; serve must be 0.2.7+.”

```text
@USR: USR_test|tool|pytest|active|persistent
@USR: USR_dep|mcp|>=1.2|active|persistent
@USR: USR_serve|version|>=0.2.7|active|persistent
@EDG: E70|TSK_mcp|constrained_by|USR_test|user|persistent
@EDG: E71|TSK_mcp|constrained_by|USR_dep|user|persistent
@EDG: E72|TSK_mcp|constrained_by|USR_serve|user|persistent
```

Three atoms — warm can omit `USR_test` if a later step only edges `USR_serve`.

---

### 9. Refactor: file moved (update atoms, don’t duplicate)

**Wrong:** `add` new `@SYM` with new id for same function.

**Right:** `update` path/line on existing id:

```text
@SYM: SYM_send|send_command|fn|src/memnet/serve.py|102|send_command(argv,stdin?)|active|persistent
```

Optional edge note:

```text
@EDG: E80|SYM_send|moved_from|MOD_serve_old|refactor|delete_on_settle
```

---

### 10. Warm anchor choice (what you get)

Same graph; different anchors → different slices:

| Anchor | Typical warm slice |
|--------|-------------------|
| `TSK_mcp` | Task + owned MOD/SYM + user constraints |
| `MOD_serve` | File + symbols defined there + callers/callees (depth 2) |
| `SYM_send` | One function + module + call edges |
| `USR_scope` | One preference + tasks that link to it |
| `REQ_01` | Requirement + satisfying parts (SysML) |
| `S03` | One article section + its `@CLM` claims |
| `CLM_31` | Single claim + linked `@ENT` / contradict edges |

Pick the **smallest anchor** that covers the current decision.

---

### 11. Article breakdown (document → sections → claims)

**Bad** — full article in one field:

```text
@ART: A01|Design doc|file.md|report|active|persistent
@NOTE: N01|text|The system uses 120W peak. Battery is 400Wh. Section 4 contradicts §2 on ambient...|persistent
```

**Good** — document tree + atomic claims:

```text
@ART: A01|PDU design report|outputs/design.md|report|active|persistent
@SEC: S03|A01|Power budget|3|active|persistent
@CLM: C31|S03|stat|peak 120W launch|active|persistent
@CLM: C32|S03|fact|battery 400Wh|active|persistent
@ENT: EN1|PDU|component|power|persistent
@EDG: X01|A01|contains|S03|struct|persistent
@EDG: X02|S03|contains|C31|claim|persistent
@EDG: X03|C31|mentions|EN1|subject|persistent
```

Summarise §3 only: `query_warm(anchor="S03", depth=2)` — not the whole `@ART`.

Full pipeline: [article-breakdown.md](article-breakdown.md).

---

## When ingesting user or LLM output

| Source | Atomise how |
|--------|-------------|
| User constraint | One `@USR` per constraint; edge to `@TSK` |
| Function discovered | Separate `@MOD` + `@SYM`; line/signature on `@SYM` only |
| Design decision | `@USR` or domain tag; link via `@EDG` |
| Long explanation | **Do not store** — distill to codes/keys or skip |
| Article paragraph | One `@CLM` per claim; `@SEC` per section — see [article-breakdown.md](article-breakdown.md) |

## Recycle and settlement

- **`persistent`** — long-lived atoms (modules, prefs, structure)
- **`delete_on_settle`** — mission-local atoms removed when `@TSK` settles
- **`delete_on_expire`** — transient edges (common for scratch links)

Settle finished work so warm reads stay focused — see goldfish loop in [memnet-goldfish-loop.mdc](../../../rules/memnet-goldfish-loop.mdc).

## Checklist before every `add`/`update`

- [ ] Can this be split into more rows?
- [ ] Are relationships `@EDG` instead of cramming into one field?
- [ ] Are field values short and structured?
- [ ] Is there a stable id copied from warm output (not invented from memory)?

Cross-ref: [wire-format.md](wire-format.md) · [article-breakdown.md](article-breakdown.md) · [coding-memory.md](coding-memory.md) · [user-input-memory.md](user-input-memory.md) · MemNet `LLM-GUIDE.md`
