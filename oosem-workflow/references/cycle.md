# OOSEM cycle map (L3)

Load when binding an activity, mapping to SysML skills, or citing sources. Keep [../SKILL.md](../SKILL.md) as the loop.

**Method SSOT:** [https://oosem.opensysml.org/](https://oosem.opensysml.org/). Steward: INCOSE Object-Oriented Systems Engineering Method Working Group. Originated 1998 (Lockheed Martin engineers with the working group). Later re-expressed in SysML. Tool- and vendor-neutral: no OOSEM product; any SysML-capable modeling tool plus a requirements tool.

MUST NOT invent activities beyond the six below. MUST NOT paste textbook chapter text.

## Framing

OOSEM treats a system as interacting objects. Behaviour is allocated to structure through a repeated cycle, not one pass of functional decomposition. That framing is meant to ease later object-oriented software, hardware, and test work.

Shared character (not this skill's job): Harmony; Rational Unified Process for Systems Engineering (RUP SE). Techniques named on the primer (use when the concern appears; do not run as a fixed extra pipeline): causal analysis, logical decomposition, node distribution analysis, control strategy definition, parametrics.

## Activity map

| Activity | Entry | SysML in this pack | Exit |
|----------|-------|--------------------|------|
| Needs analysis | Problem unclear; solution language not yet allowed | `sysml-stakeholder-use-case` | Named stakeholders, goals, operational scenarios |
| Requirements analysis | Needs and scenarios exist | `sysml-requirements-generator` | Black-box requirements; no presupposed design |
| Architecture and logical decomposition | Black-box behaviour exists | Nested structure, then behaviour on those objects, then connections / software ports / items, then `sysml-allocate-generator` for software-to-hardware (one skill per turn) | Logical objects with behaviour and interactions; then physical component split |
| Trade studies and analysis | Two or more candidate architectures or parameter sets | `mcdm-decider` against measures of effectiveness | Justified choice (or documented reject) |
| Design synthesis | Logical/physical split chosen | hardware/software part generators; `sysml-physical-port-generator` when connector pinouts are the gap | Design specific enough to implement, test, integrate |
| Verification and validation | Design or implementation claims done | `sysml-traceability` or `sysml-requirements-audit` (audit after trace); `sysml-part-reviewer` for part maturity -- one skill per turn | Coverage of requirements and original needs; lessons listed for an earlier activity |

## Iteration

Each pass MAY decompose objects further, allocate more detailed behaviour, and tighten requirements. V&V MUST feed lessons into earlier activities. Closing 06 does not forbid another 01-05 pass.

Order inside architecture: logical interacting objects before physical components. `sysml-allocate-generator` is software/firmware **usages to hardware usages** in deploy -- not a substitute for behaviour on logical objects (`sysml-behaviour-generator`). Order vs design: do not synthesise implementable parts until a logical allocation exists unless the user is explicitly refining an already-allocated object.

## Tooling this pack uses

The primer is method-only. This pack practises it with textual SysML v2 (`mcp-sysml-v2` validate) and MemNet working memory (`sysml-modeling-workflow`). Open-source communities the primer names: OpenMBEE (model management); SysML v2 / KerML forum. MUST NOT switch the pack to a commercial modeling GUI unless the user explicitly asks about tool selection (`sysmltools.com` rule in sysml-modeling-workflow).

## Sources (cite, do not copy)

- Primer: https://oosem.opensysml.org/
- 2009 -- Friedenthal, Moore and Steiner, *A Practical Guide to SysML* (Morgan Kaufmann / OMG Press), Chapter 16 (SysML applied to OOSEM). Training often follows this chapter; do not reproduce it.
- 2008 -- Estefan, *Survey of Model-Based Systems Engineering (MBSE) Methodologies*, INCOSE Technical Publication (OOSEM among other methods).
- 2000 -- Lykins, Friedenthal, Sanford and Meilich, *Adapting UML for an Object-Oriented Systems Engineering Method (OOSEM)*, INCOSE International Symposium.

INCOSE home and working-group charter/marketplace material: follow links on the primer. Do not scrape INCOSE member-only PDFs into this skill.
