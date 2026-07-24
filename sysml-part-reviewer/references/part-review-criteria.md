# SysML part review — design maturity and documentation gate

Use when classifying a **part def** (hardware, software, or abstract block) before accepting edits.

---

## Three conditions (pick one per part)

| Condition | Meaning | Typical signals |
|-----------|---------|-----------------|
| **under-design** | Work in progress; structure and interfaces still evolving. | Placeholder names, TBD attributes, draft ports, no stable external identity, internal project-only block. |
| **well-design** | Design is baselined or released; changes have traceability and stakeholder impact. | Frozen or versioned interfaces, requirements satisfied, outputs/docs exist or are expected for changes, custom or semi-custom part with agreed spec. |
| **COTS** | Commercial Off-The-Shelf; identity and behaviour come from vendor data. | Manufacturer + MPN, datasheet, dev kit, standard module; model mirrors catalog, not invented internals. |

If unclear, default toward **well-design** or **COTS** (stricter gate) and ask one clarifying question.

---

## Modification rule (binding)

**Only parts in condition `under-design` may be modified without accompanying documentation.**

- **under-design:** SysML edits in the model may proceed without requiring separate docs (still follow project workflow: validate, outputs sync if the project uses them).
- **well-design:** Do not treat model-only edits as sufficient. Require or produce documentation appropriate to the change (e.g. updated `outputs/*.md`, pin map, rationale, requirements delta, BOM note, ADR) before or with the `.sysml` change.
- **COTS:** Do not change electrical/logical substance without vendor-aligned evidence (datasheet, errata, supplier drawing). Model should reference the COTS identity; prefer attributes and ports that match the datasheet. If the part is replaced by another MPN, document the substitution.

---

## Review output (for the agent)

For each part in scope:

1. **Name** (qualified name or file + part def id).
2. **Condition:** `under-design` | `well-design` | `COTS` (with one-line rationale).
3. **Modification allowed without docs?** `yes` only if `under-design`; else `no` and list required doc artifacts.
4. **Findings** (optional): severity `error` | `warning` | `info` — e.g. COTS without MPN, well-design change without outputs update.

---

## Mapping common inputs to maturity (hardware / lib)

| User / model signal | Likely condition | Notes |
|---------------------|------------------|--------|
| **OTS** + MPN + datasheet | **COTS** | Model should track vendor identity; no invented pin behaviour. |
| **Custom / IMD / PCBA** + baselined outputs | **well-design** | Changes need traceability (outputs, BOM, pin map). |
| **Custom** still in flux, no frozen interfaces | **under-design** | Model-only edits allowed without extra docs (still validate). |
| **New** `part def` (greenfield) in draft deploy | **under-design** until baselined | User may declare baseline → becomes well-design. |
| **`hardware_ports.sysml`** connector from published standard | **COTS** or **well-design** | Standard pinout = external spec; lib edits need rationale or version bump note. |

---

## De facto vs nominal ports (COTS and network gear)

When reviewing **hardware `part def`** that exposes many identical connectors (e.g. switch RJ45 banks):

- **Physical naming** (`poeEthernet1`…`n`, `sfp1`…`n`, `acInlet`) matches **product truth** and operator/CLI reality; **site-specific** meaning (“port 1 = core router”) belongs in **`doc`** as an explicit **convention**, not as if the vendor defined it.
- **Role naming** (`fromCoreRouter`, `toCamera`) is **nominal**—useful for reuse in some deploys but **misleading** if readers think each role is a distinct jack.
- **Inconsistency** across sibling `part def` in the same file (one switch physical, another role-only) is a **warning**: require an explicit **`doc`** pattern or align types.

Full guidance: [sysml-traceability/references/de-facto-modeling.md](../../sysml-traceability/references/de-facto-modeling.md).

---

## Related skills (after gate is clear)

| Skill | Use when |
|-------|----------|
| **sysml-hardware-part-generator** | New or allowed edit to hardware `part def` (boards, modules, PCBA). |
| **sysml-software-part-generator** | Software `part def` (threads, SM, services). |
| **sysml-physical-port-generator** | Connector / `port def` with `protocol { pin }` in `hardware_ports.sysml` (often before hardware part). |
| **sysml-item-generator** | `item def` for flow payloads on ports / actions. |
| **sysml-connections** | `connection def` / deploy wiring after parts and ports exist. |
| **sysml-view-doc-sync** | Project `outputs/*.md` must match model after **well-design** / **COTS** substantive changes. |
| **sysml-common-lib-contribution** | Any change under `libs/common/` — extra scrutiny; often **well-design** or **COTS**. |

---

## Contrast with generators

This skill **reviews** maturity and doc gates; it does **not** scaffold new part defs. Run **sysml-part-reviewer** first when **editing an existing** part or when maturity is unclear; use **sysml-hardware-part-generator**, **sysml-software-part-generator**, or **sysml-item-generator** after the gate allows edits.
