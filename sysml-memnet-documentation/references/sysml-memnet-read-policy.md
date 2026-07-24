# SysML MemNet read policy — when to read `.sysml` vs `query_warm`

**Problem:** Agents with MemNet still **re-read** `deploy-*.sysml`, `requirements-*.sysml`, and report sections every turn — duplicating work the graph already holds and burning context.

**Rule:** On `sysml-v2-models/projects/<slug>/`, **topology discovery = MemNet**; **syntax edit = narrow file window**; **full file read = last resort**.

Pair with [sysml-memnet-snap.md](sysml-memnet-snap.md) (6-step turn) and [sysml-memnet-pipeline.md](sysml-memnet-pipeline.md) (step wire).

---

## Three stores — who answers what

| Question | Ask first | Only if miss |
|----------|-----------|--------------|
| What parts exist? Who connects to whom? | `query_warm` → `@PRT` / `@CON` / `@EDG` | Grep `part ` in `deploy-*.sysml` |
| Where is `linkFoo` / `FoamLiteVer2RelayController`? | `query_warm` → `@SYM_<name>` → `path` + `line` | `Grep` exact symbol in `models/` |
| What does requirement `VFDL2-*` satisfy? | `query_warm` → `@REQ_*` + `satisfies` EDGs | Read `root-*.sysml` satisfy block (window) |
| What changed last session? | `pin_map(TSK_model_*)` + project `.memnet/*.snap` load if session expired | Git diff (user asked or commit prep only) |
| Exact `connection` / `bind` / import syntax to patch? | Read **±15 lines** at `@SYM.line` | Wider window or `mcp-sysml-v2 getDefinition` |
| Load order / package imports broken? | `config.yaml` + `mcp-sysml-v2 validate` errors | Read `root-*.sysml` imports only |
| Human narrative for one report section? | Hub `index.md` + **one** `llm_toc[].file` | Other sections |

**MemNet is authoritative for structure between turns.** `.sysml` is authoritative for **syntax and satisfy links** at edit time.

---

## Per-turn read budget (substantive modeling turn)

| Allowed | Typical limit |
|---------|----------------|
| `serve_status` + `query_warm` | 1–2 calls (`TSK_model_*`, optional `@PRT_*` / `@CON_*`) |
| `Read` on `.sysml` | **≤2 files**, **≤40 lines each** (locator window around `@SYM.line`) |
| `Grep` on `models/` | **≤3** queries; scoped to one file when `@MOD` known |
| `Read` hub `index.md` | 1× (~80 lines) when touching reports |
| `Read` one report section | 1× the section file for the task topic only |

| **Forbidden** (unless user asks to audit whole file, or warm miss initial snap) |
|--------------------------------------------------------------------------------|
| `Read` entire `deploy-*.sysml` (>80 lines) to “understand architecture” |
| Re-`Read` same deploy file every turn in a multi-turn thread |
| `Grep` whole project for names already in warm output |
| `Read` full `AGENT-CONTEXT.md` body for topology (header line only: session + anchor) |
| `Read` all report sections when one topic changed |
| Chat-summary / conversation memory instead of `query_warm` |

---

## Decision tree (step 3 — locate before edit)

```
serve_status.running?
  false → grep/read as needed; note stale MemNet; skip step 6
  true  → pin_map(TSK_model_<short>, depth=2)

Need symbol location?
  warm has @SYM_<name> with path+line?
    yes → Read(path, offset=line-12, limit=35)
    no  → Grep symbol in models/<file from @MOD_*>

Need connection endpoints?
  warm has @CON_<linkName>?
    yes → use ends from warm; open window on each @SYM if editing
    no  → Grep linkName in deploy + connections-*.sysml

Need new part between existing parts?
  warm @PRT_* for neighbours → grep only the insertion region

Still ambiguous after warm + one grep?
  mcp-sysmledgraph impact OR mcp-sysml-v2 getSymbols (not full file read)
```

---

## Anti-patterns (do not repeat)

| Anti-pattern | Why wrong | Do instead |
|--------------|-----------|------------|
| Read `deploy-*.sysml` at start of every user message | Graph already has `@PRT`/`@CON` | `query_warm` |
| Grep `W6300|relayChain|edge24V` across repo each turn | Redundant after delta push | Warm on `@PRT_relayController` / `@PRT_relayChainPcba` |
| Read requirements + deploy + root before one link rename | Blast radius is in MemNet + sysmledgraph | Warm `@CON_*` + grep link name |
| Sync outputs by re-reading all of deploy | Report pipeline: warm + **one** section | [memnet-report-pipeline.md](../../system-design-report-generator/references/memnet-report-pipeline.md) M1–M3 |
| Skip MemNet write after multi-file session | Next turn forces full re-read | Step 6 delta + `session_save` / wire push |

---

## Multi-turn threads (conversation handoff)

When the user continues a design thread (e.g. “add PSU”, then “de facto W6300”, then “40-pin harness”):

1. **Turn 2+:** `pin_map(TSK_model_*)` — **do not** re-ingest deploy from disk for facts already atomised.
2. If prior turn edited `.sysml` but **step 6 was skipped** → treat as **stale graph**: run **incremental delta** from git-diff symbols **before** warm, or grep changed ids only.
3. Store **settled decisions** as `@CLM` / `@DEC` (e.g. “relay PCBA mates via gpio40p pin 37”) so prose questions do not require re-read.

---

## `query_warm` prompts (copy patterns)

Use **anchor + entity**, not open-ended chat:

| Task | Warm query focus |
|------|------------------|
| Relay / valve chain | `TSK_model_vfdl2` + rows for `PRT_relayChainPcba`, `PRT_relayController`, `CON_link*Relay*` |
| Edge power | `PRT_edge24VPsu`, `CON_linkEdge24VPsu*` |
| Requirements touched | `REQ_VFDL2-*` + `satisfies` edges |
| Report section | `ART_<project>-design` + `@SEC` for section id |
| Locate edit | `@SYM_<linkOrPartName>` |

Increase `max_rows` (50→80) only when warm returns &lt;3 relevant rows **and** initial snap is known good.

---

## When full file read **is** allowed

| Case | Action |
|------|--------|
| **Initial snap** (warm miss, greenfield) | Grep-by-role per [sysml-memnet-snap.md](sysml-memnet-snap.md) §Initial snap — not blind `Read` entire file |
| **User:** “audit deploy file” / “review whole model” | Full read permitted |
| **Import-order diagnosis** | `sysml-import-order-helper` — targeted files from validate errors |
| **Refactor blast radius** | `mcp-sysmledgraph` first; full deploy only if graph unavailable |
| **Common lib edit** (`libs/common/`) | No project `@TSK` — grep/read lib file; optional `MOD_*` in MemNet if seeded |

---

## After edit (mandatory — prevents next-turn re-read)

1. `mcp-sysml-v2 validate`
2. MemNet delta: new/changed `@PRT`/`@POR`/`@CON`/`@REQ` + `@SYM` + `@EDG`
3. Re-grep touched `@MOD` → `update` all `@SYM.line` in that file
4. If ≥3 structural changes or end of session: `session_save` → `projects/<slug>/.memnet/<slug>.snap` or wire push

**Stale graph is the main cause of repeated SysML reads.** Step 6 is not optional for structural edits.

---

## Specialist skills

Any `sysml-*` generator/refactorer/audit skill **MUST**:

1. Delegate **discovery** to `query_warm` (this policy)
2. Delegate **turn order** to [sysml-modeling-workflow](../../sysml-modeling-workflow/SKILL.md)
3. Run **step 6** before ending the turn when structure changed

---

## Quick self-check (before opening another `.sysml` file)

Answer **yes** to at least one, or stop and warm:

- [ ] `serve_status` checked this turn?
- [ ] `query_warm` run for this task’s anchor?
- [ ] I have `@SYM.line` for the symbol I will edit?
- [ ] This read is ≤40 lines or validate-error-targeted?
- [ ] I am not re-fetching facts already in warm output?
