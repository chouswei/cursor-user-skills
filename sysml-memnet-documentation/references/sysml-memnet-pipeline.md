# SysML + MemNet — pipeline handoffs

**Audience:** LLM agents. Structured state **between pipeline steps** uses MemNet **shared dialect** (Write = display — same NODE|EDGE shapes for pin-map read and mutate) when `serve_status` is true — not TOON/TRON blocks in chat. Dialect: [memnet-format](../../memnet-format/SKILL.md), [mcp-memnet](../../mcp-memnet/SKILL.md).

Pair with [sysml-memnet-snap.md](sysml-memnet-snap.md) (6-step turn), [memnet-report-pipeline.md](../../system-design-report-generator/references/memnet-report-pipeline.md).

**Legacy:** `@TAG:` pipe rows and `@CLM` type=`pipe` field tables below remain **accepted store shapes** (older snaps / import). Prefer shared-dialect mutate for new step atoms.

---

## Tiered handoff (mandatory)

| Situation | Format | Where it lives |
|-----------|--------|----------------|
| **SysML modeling turn** (steps 1–6) | Shared dialect mutate (`+`/`~`/`-`); step `code` = `sN:payload` | `add` / `update` each step |
| **Report generate/maintain** (G/M steps) | Same + ART/SEC when prose settles | Server graph |
| **Skill routing** (`order[]`, picks) | Task + claim atoms + `led_to_success` edges | Server graph |
| **Serve down** | Plain Markdown tables or short prose | Ephemeral — not durable |
| **MCP / CLI tool boundary** | JSON envelope | Tool response only |

**Rule:** If `serve_status.running` and the handoff must survive context shrink or the next sub-step → **atoms on server**, not a Markdown-only scratch in the assistant message.

---

## Preferred: shared-dialect step atoms

Mutate after each step (or batch s1–s2, then s3, then s4–s6). Pin map is bare present; mutate keeps ops.

```text
## Nodes
+ TSK [NEW] ; goal={goal ≤8 words} ; phase=pipe ; status=in_progress ; recycle=delete_on_settle
+ CLM [NEW] ; type=decision ; code=s1:up ; recycle=delete_on_settle
+ CLM [NEW] ; type=decision ; code=s2:hit ; recycle=delete_on_settle

## Edges
+ E01 [NEW] --(childOf)--> [TSK_model_<short>] ; note=turn ; recycle=delete_on_settle
```

Copy assigned ids from the pin map / mutate response for later `~` updates. Settle the turn with `~ TSK […] ; status=settled`.

### Step `code` vocabulary (shared and legacy)

| Step | `code` prefix | Example `code` |
|------|---------------|----------------|
| s1 serve | `s1:` | `s1:up` · `s1:down` |
| s2 warm | `s2:` | `s2:hit` · `s2:miss` |
| s3 edit | `s3:` | `s3:SYM_mcuHeaderHarness` · `s3:skip` |
| s4 validate | `s4:` | `s4:pass` · `s4:fail` |
| s5 sync | `s5:` | `s5:done` · `s5:skip` · `s5:report_delta` |
| s6 delta | `s6:` | `s6:Nrows` · `s6:skip` · `s6:stale` |

**Step 2 skip** (`serve` down): `s1:down`, omit s2 or `s2:skip`, note `s6:stale` if no delta.

**Step 5 skip** (no outputs): `s5:skip`.

**Step 6 skip** (comment-only): `s6:skip` + settle turn.

**Resume next turn:** pin map on `TSK_model_<short>` (`query_warm` is the **legacy alias** for that read) — latest in-progress turn or last step atoms; **do not** re-derive from chat.

---

## Legacy accepted shapes (`@TAG` pipe)

Field tables and examples below are **legacy / store** — still accepted on mutate and useful for reading older snaps. Prefer the shared-dialect sketch above for new agent I/O.

### Turn container (`@TSK`)

```text
@TSK: TSK_turn_<short>|{goal ≤8 words}|pipe|in_progress|delete_on_settle
@EDG: E…|TSK_turn_<short>|childOf|TSK_model_<short>|turn|delete_on_settle
```

On completion: `status` → `settled` (same row `update`).

### Step outcome (`@CLM` type=`pipe`)

Field order: `id|sec|type|code|status|recycle` — for pipeline, **`sec`** = parent `TSK_turn_*` id; **`code`** = `sN:payload`.

```text
@CLM: C_s2|TSK_turn_vfdl2_harness|pipe|s2:hit|active|delete_on_settle
@EDG: E…|C_s2|documents|TSK_turn_vfdl2_harness|step|delete_on_settle
```

### Router / skill pick (`@TSK` phase=`route`)

```text
@TSK: TSK_route_<slug>|{intent ≤8 words}|route|in_progress|delete_on_settle
@CLM: C_r1|TSK_route_<slug>|pipe|pick:sysml-modeling-workflow|active|delete_on_settle
@CLM: C_r2|TSK_route_<slug>|pipe|pick:sysml-memnet-documentation|active|delete_on_settle
@EDG: E…|TSK_route_<slug>|led_to_success|sysml-modeling-workflow|pass|persistent
```

Phase-4 learning: `led_to_success` edges are **`persistent`**; route `@TSK` is **`delete_on_settle`**.

### Six-step template (legacy pipe)

```text
@TSK: TSK_turn_<id>|{goal}|pipe|in_progress|delete_on_settle
@EDG: E_turn_01|TSK_turn_<id>|childOf|TSK_model_<short>|turn|delete_on_settle
@CLM: C_s1|TSK_turn_<id>|pipe|s1:up|active|delete_on_settle
@CLM: C_s2|TSK_turn_<id>|pipe|s2:hit|active|delete_on_settle
@CLM: C_s3|TSK_turn_<id>|pipe|s3:SYM_<symbol>|active|delete_on_settle
@CLM: C_s4|TSK_turn_<id>|pipe|s4:pass|active|delete_on_settle
@CLM: C_s5|TSK_turn_<id>|pipe|s5:sync:done|active|delete_on_settle
@CLM: C_s6|TSK_turn_<id>|pipe|s6:24rows|active|delete_on_settle
```

---

## Report pipeline — G / M steps

Parent: `TSK_model_<short>` or `TSK_report_<short>` (`phase=report`, `delete_on_settle`). Prefer shared-dialect mutate; pipe examples are legacy-accepted.

| Phase | Step | `code` |
|-------|------|--------|
| Generate | G0 | `G0:serve` |
| Generate | G1 | `G1:warm_hit` |
| Generate | G2 | `G2:hub` |
| Generate | G3 | `G3:scaffold` |
| Generate | G4 | `G4:sections` |
| Generate | G5 | `G5:mmdc` |
| Generate | G6 | `G6:art_atoms` |
| Generate | G7 | `G7:done` |
| Maintain | M1 | `M1:warm` |
| Maintain | M2 | `M2:sec_<id>` |
| Maintain | M3 | `M3:patch` |
| Maintain | M4 | `M4:model_delta` |
| Maintain | M5 | `M5:clm_delta` |

```text
# Legacy pipe example (accepted store shape)
@TSK: TSK_report_vfdl2|Sync relay section|report|in_progress|delete_on_settle
@CLM: C_M1|TSK_report_vfdl2|pipe|M1:warm|active|delete_on_settle
@CLM: C_M2|TSK_report_vfdl2|pipe|M2:sec_S05-relay|active|delete_on_settle
@CLM: C_M5|TSK_report_vfdl2|pipe|M5:8clm|active|delete_on_settle
```

Link report atoms: edge from the M5 claim → `mentions` → `@CON_*` / `@PRT_*` (same batch as model delta).

---

## Diagram placement task (`TSK_diagram_*`)

Use when building or updating **interconnection Mermaid** in `outputs/**/*.md`. Full algorithm: [mermaid/references/mermaid-placement-by-degree.md](../../mermaid/references/mermaid-placement-by-degree.md).

**Parent:** `TSK_diagram_<figureId>` `childOf` → `TSK_model_<short>` · `documents` → section atom · `delete_on_settle` until `p6:settle`.

**Pipe codes** (legacy `@CLM` type=`pipe`, `sec` = `TSK_diagram_*`):

| Code | Action | Touches `.md`? |
|------|--------|----------------|
| `p0:types` | `typedBy` histogram → intent bucket | No |
| `p1:scope` | `figure_includes` / `figure_uses` EDG batch | No |
| `p2:place` | Ranks, anchor, `adjacent_to`, claim stat `deg rank lane declare#` | No |
| `p2b:bary` | Barycenter lane iteration ≤2 | No |
| `p2c:spans` | Per-CON `rank_span`; fail if >1 except uplink | No |
| `p3:edges` | Ordered `CON_*` (spokes → chains → chords) | No |
| `p4:materialise` | Patch section `.md`; `mmdc` | **Yes** |
| `p5:review` | Visual check; `ok` / `adjust` | Re-p4 only |
| `p6:settle` | Method claim on section; recycle pipe rows | No |

**Serve down:** Markdown `DiagramPlan` tables in-prompt ([mermaid-placement-by-degree](../../mermaid/references/mermaid-placement-by-degree.md)); backfill MemNet before `p4`.

```text
# Legacy pipe example
@TSK: TSK_diagram_vfdl2-edgeside-panel-eth|panel L2 graph|pipe|in_progress|delete_on_settle
@EDG: E…|TSK_diagram_vfdl2-edgeside-panel-eth|childOf|TSK_model_vfdl2|diagram|delete_on_settle
@CLM: C_p2c|TSK_diagram_vfdl2-edgeside-panel-eth|pipe|p2c:spans ok:5 warn:0|active|delete_on_settle
@CLM: C_p3|TSK_diagram_vfdl2-edgeside-panel-eth|pipe|p3:edges CON_linkRelayControllerToGs305epPort1,…|active|delete_on_settle
```

---

## Between-step execution (goldfish)

```
step N:   pin map (query_warm = legacy alias) on TSK_model_* OR TSK_turn_*
          → act
          → add/update step atom for step N (shared dialect preferred)
step N+1: pin map (same anchor) — read step atoms, not chat
```

**MUST NOT** paste pipeline state only as chat Markdown when serve is up.

**MAY** echo a **single-line** summary for the user (`Turn settled: s4:pass s6:24rows`).

---

## Serve down fallback

When `s1:down`:

1. Use plain Markdown tables or short prose for in-turn scratch only.
2. Set `s6:stale` on turn row if you would have written delta.
3. On next session with serve up: run incremental delta from disk before relying on the pin map.

---

## Claim type for pipeline steps

Add to closed list in [sysml-memnet-patterns.md](sysml-memnet-patterns.md):

| Claim `type` | Use |
|--------------|-----|
| `pipe` | Pipeline step outcome (`code` = `sN:…` or `GN:…` / `MN:…`) — legacy pipe field name; keep for vocabulary |

---

## Anti-patterns

| Bad | Good |
|-----|------|
| Markdown-only scratch in chat for s1–s6 state | Step atoms on server (shared dialect preferred) |
| Re-read deploy because pipeline state was only in chat | Pin map on `TSK_turn_*` |
| One fat note for whole turn | One claim per step |
| Skip settle turn → `settled` | Settle so the pin map stays lean |
| Prefer `@TAG` pipe as agent I/O | Shared dialect; pipe = legacy/store |

---

## Quick checklist

- [ ] `serve_status` → choose shared dialect vs Markdown tier
- [ ] Opened turn task or attached to `TSK_model_*` via `childOf`
- [ ] Each completed step has a step atom (`code` = `sN:…`)
- [ ] Turn `settled` when done
- [ ] Next step starts with pin map (`query_warm` legacy alias), not chat memory
