---
name: memnet-format
description: >-
  Canonical MemNet wire format (@TAG pipe rows, @EDG relations, tag vocabulary, atomisation,
  tiered handoff). LLM-only skill for authoring rules, skills, and durable graph state.
  Triggers: memnet format, memnet wire, @TAG, pipe rows, atomised rows, goldfish format,
  durable graph format, token efficient graph, memnet atoms, @EDG, @SET, @IDX, wire grammar.
metadata:
  pattern: tool-wrapper
  version: "1.3"
  domain: data-formats,memnet
---

# MemNet Wire Format (LLM-only)

**Audience:** model. Wire rows are canonical; open `references/memnet-wire-format.md` for full grammar and tag field orders.

**Role:** format authority for `@TAG:` pipe language. Pair with `mcp-memnet` (tools) and `memnet-goldfish-loop.mdc` (loop). Do not use TOON/TRON for handoffs.

---

## Core record shape

```text
@TAG: id|field2|field3|...|recycle
```

```text
@RUL: F01|MUST|one atom per line; exactly one : after tag|high
@RUL: F02|MUST|relations as separate @EDG rows (never embedded arrays)|high
@RUL: F03|MUST|escape literal | as \| inside field values|high
@RUL: F04|MUST|last field = recycle: persistent|delete_on_settle|delete_on_expire|high
@RUL: F05|MUSTNOT|prose blobs or nested JSON on the wire|high
@RUL: F06|SHOULD|query_warm(anchor, depth≤2) before inventing ids|high
```

---

## Tag selection (when to use which)

```text
@SEL: fact_or_claim|@CLM + @ENT + @EDG|atomic verifiable statement
@SEL: relationship|@EDG|from|rel|to — verbs: owns,contains,satisfies,documents,next,delegates,overrides,governs,preempts,memberOf
@SEL: flat_enumeration|@SET or @IDX|membership list; @IDX carries count field for verification
@SEL: work_unit|@TSK|goal, phase, status, recycle
@SEL: pipeline_step|@CLM type=pipe|code=s1:…s6: or G/M codes when serve up
@SEL: user_constraint|@USR|lasting scope, style, preference
@SEL: file_or_symbol|@MOD @SYM|coding memory
@SEL: sysml_element|@PRT @POR @CON @REQ @SYM|see sysml-memnet-patterns.md
@SEL: rule_or_policy|@RUL|normative directive with priority
@SEL: procedure_step|@PRC|ordered action chain
@SEL: routing|@ROU|condition → target skill or doc
@SEL: trigger_map|@TRG|phrase → skill-id
```

**@EDG vs @SET:** membership of many ids in one pack → `@SET` (one row). Directed relation between two nodes → `@EDG`. Ordered workflow chain → `@EDG` with `rel=next`.

---

## Tiered handoff

```text
@ROU: handoff_0|LLM/author-facing in-prompt|English pins + write=display (md_triple-style); NOT raw @TAG pipe dumps
@ROU: handoff_1|serve up + durable store write|MemNet MCP wire (@TSK + @CLM type=pipe + @EDG) — store only
@ROU: handoff_2|serve down + same-turn scratch|plain Markdown tables or short prose (not TOON/TRON)
@ROU: handoff_3|tool/MCP/CLI boundary|JSON envelope only
@ROU: handoff_4|human operator deliverable|prose Markdown; Markdown tables for dense grids
```

**LLM vs store:** `@TAG|pipe` is machine-durable (MCP). Author feed follows novel-cut doctrine (accurate/precise/consistent/coherent/low-noise/English).

SysML pipeline codes: [sysml-memnet-pipeline.md](../sysml-memnet-documentation/references/sysml-memnet-pipeline.md).

---

## Atomisation (before every add/update)

```text
@RUL: A01|MUST|split fat row into multiple rows + @EDG if possible|high
@RUL: A02|MUST|field values = short ids, paths, codes, numbers (no sentences)|high
@RUL: A03|MUST|stable id from prior query_warm or add response|high
@RUL: A04|MUSTNOT|@NOTE paragraphs — use @CLM facts + @EDG instead|high
```

Full discipline: [mcp-memnet/references/atomisation.md](../mcp-memnet/references/atomisation.md).

---

## Pre-write checklist

```text
@CHK: w1|query_warm on tight anchor|pass|fail
@CHK: w2|values short and structured|pass|fail
@CHK: w3|relations are @EDG rows|pass|fail
@CHK: w4|recycle matches lifetime (transient=delete_on_settle)|pass|fail
@CHK: w5|atom reachable from useful anchor via @EDG|pass|fail
```

---

## Pairing edges

```text
@EDG: E_fmt_01|memnet-format|implements|wire grammar|canonical|persistent
@EDG: E_fmt_02|memnet-format|paired_with|mcp-memnet|tools_and_loop|persistent
@EDG: E_fmt_05|memnet-format|paired_with|sysml-memnet-documentation|sysml_patterns|persistent
@EDG: E_fmt_06|memnet-format|governed_by|memnet-goldfish-loop.mdc|orchestration|persistent
@EDG: E_fmt_07|memnet-format|detail_in|references/memnet-wire-format.md|grammar|persistent
```

---

## Further reading (lazy-load)

- [references/memnet-wire-format.md](references/memnet-wire-format.md) — line grammar, tag shapes, good/bad examples
- [mcp-memnet/references/atomisation.md](../mcp-memnet/references/atomisation.md)
- [sysml-memnet-patterns.md](../sysml-memnet-documentation/references/sysml-memnet-patterns.md)
- MemNet upstream `LLM-GUIDE.md`
