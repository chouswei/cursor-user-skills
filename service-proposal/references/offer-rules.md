# Offer rules (L3)

Apply when drafting or recasting a **service proposal**. British English in new customer text unless the host file already uses another locale. ASCII `->` `--`.

## Artefact class

| Is | Is not |
|----|--------|
| Customer-facing commercial **offer** | Internal SOP / work instruction |
| What **we** supply and under what terms | Lab calibration procedure |
| Scope, deliverables, timeline, pricing placeholders, terms | Engineering design dump (schematic narrative, netlist walk) |

## We offer vs Customer furnishes (CFE)

1. MUST label two buckets in Executive Summary and Scope of Work: **We offer** and **Customer furnishes (CFE)**.
2. MUST NOT list CFE items as sellable SKUs, BOM sell-lines, or "products we propose the client purchase" when the client already owns or must supply them.
3. PandaDoc "products the client purchases" may appear only for items **we** actually sell or broker; CFE stays in the CFE bucket.

## Product shape

1. If the work is a **PCBA subsystem** (function on a board / island set, not a separate boxed product root): MUST say **PCBA subsystem** (or equivalent) in cover/subject and Executive Summary.
2. MUST NOT frame a subsystem as a standalone boxed instrument, crate PSU, or separate enclosure SKU unless that is the closed commercial fact.

## Sense and monitors

1. On-board sense (ADC, TIA, island readout) is **ours** when it is in scope.
2. A site DMM / handheld meter is optional **customer check-only** -- not an offer SKU.
3. MUST NOT invent a "COTS bench monitor" (or similar) product line item.

## Reference vendors and catalogue SKUs

1. MUST NOT name competitor or reference-vendor brands, or their catalogue SKUs, in the customer proposal (example class: a named COTS PSU used only as an internal engineering reference).
2. Internal hardware notes MAY keep those SKUs; the proposal MUST strip or generalise them ("constant-current source module", "isolated DC-DC", etc.).

## Ratings and model SSOT

1. If the host repo is model-based (`sysml-models/models/*.sysml` present, or `AGENTS.md` states SysML as SSOT) and the change touches design SHALLs / ratings / ports: MUST edit the model first, then align the proposal.
2. Else MUST write only from stated closed facts; mark unknowns as `[bracket placeholders]`.
3. MUST NOT invent electrical ratings, isolation figures, or schedule dates.

## Pricing

1. MUST use **TBD** (or empty TBD table cells) for currency amounts until the user supplies figures.
2. MUST NOT invent unit prices, totals, tax, or discount math.

## Hazards

1. MUST state hazards as **offer constraints**, **exclusions**, or **customer responsibilities**.
2. MUST NOT paste lock-out procedures, cal steps, or lab method bodies into the proposal.

## Recast (plan -> proposal)

1. Keep closed commercial facts; drop internal implementation narrative.
2. Re-bucket every bullet into We offer / CFE / Not offered.
3. Re-run the SKU / vendor / monitor / subsystem checks before emit.

## Self-check before emit

- [ ] PandaDoc heading order intact
- [ ] We offer vs CFE split present
- [ ] No CFE sold as our SKU
- [ ] Subsystem named if applicable; no false boxed-instrument cover
- [ ] No competitor / reference catalogue SKUs
- [ ] No invented COTS bench-monitor SKU
- [ ] Pricing is TBD unless user-supplied
- [ ] Hazards are constraints/exclusions only
- [ ] Model edited first when model-based and SHALLs changed
