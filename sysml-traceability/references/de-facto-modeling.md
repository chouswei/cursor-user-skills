# De facto vs nominal in SysML v2 (this repo)

**Purpose:** MBSE models go stale when **names in the library** look like “the truth” but **what is actually wired and operated** lives only in someone’s head. In this workspace, **de facto** means: *what the team plugs in, powers, configures, and documents as the running system*—including **site-specific** port choices.

---

## Definitions

| Term | Meaning |
|------|---------|
| **Nominal** | Names or roles that are convenient for diagrams or reuse but **not** printed on the device (e.g. `toCamera`, `fromCoreRouter`). |
| **De facto** | What **actually** happens: physical jack/SFP numbers, cable IDs, **deploy** `connection` ends, CLI targets, pin maps, and **outputs/*.md** tables that operators use. |
| **Product truth** | What the **datasheet** guarantees: connector types, count of RJ45/SFP, power inlet, PoE class—belongs in **`part def`** `doc` and attributes. |
| **Site convention** | A **project choice**: “we always put the core router on `poeEthernet1`.” Not intrinsic to the SKU; must be **written** in deploy `doc`, part `doc`, or `outputs/*.md`. |

---

## Rules of thumb (binding for agents)

1. **`part def` in `libs/common`** — Prefer **physical interface inventory** for COTS boxes (numbered RJ45, SFP cages, AC inlet) when the user asks for fidelity to the product. **Role-named ports** on the same class of device (e.g. one switch family physical, another logical) is a **library inconsistency**—flag it or align with an explicit pattern in `doc`.

2. **`deploy-*`** — Connection ends are **de facto wiring intent**. If the model says `backbone.poeEthernet2` ↔ cable, that is the **authoritative** story for that project; docs must not describe a different port without a model change.

3. **Never imply site convention is datasheet** — If `doc` says “port 1 = router,” prefix with **convention** or **deploy**: readers must not think NETGEAR assigns that meaning.

4. **Traceability** — `satisfy` / `allocate` link requirements to **design elements**; for “which RJ45 is the CAM leg?” the trace chain often runs **requirement → deploy connection → port name**. Gap: requirement text that names a **role** while deploy uses **numbers** → fix wording or add a short **allocation / doc** note.

5. **Outputs** — `outputs/*.md` are **operator-facing de facto**: tables and paragraphs should use the **same port names** as deploy. If the model is source of truth, **sync** after `.sysml` edits ([sysml-view-doc-sync](../../sysml-view-doc-sync/SKILL.md)).

6. **Validate** — Grammar validation does **not** check de facto alignment. Use **grep** across deploy + outputs + common part for renamed ports; run **`exam_model.py`** per project when deploy changes.

---

## Anti-patterns

- **Role ports on COTS** with no deploy instance: suggests a jack that does not exist as a separate physical interface.
- **Renaming library ports** without **sysmledgraph** / **getReferences** and **outputs** pass: breaks de facto traceability.
- **Mermaid or narrative** that invents wiring not present in `connection` usages (model-first workflow).

---

## Related skills

| Skill | Role |
|-------|------|
| **sysml-traceability** | satisfy/allocate + gap analysis; include de facto port/wiring consistency. |
| **sysml-view-doc-sync** | Align `outputs/*.md` with deploy port names and conventions. |
| **sysml-connections** | Edits to `connection` ends are de facto changes—sync docs. |
| **sysml-hardware-part-generator** / **sysml-part-reviewer** | Physical vs role port strategy; maturity gate for baselined parts. |
| **sysml-common-lib-contribution** | Shared `network.sysml` / ports: one clear pattern per product class when possible. |
