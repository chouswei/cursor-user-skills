---
name: mcp-inventree
description: >-
  InvenTree MCP (user-inventree): part, stock, purchase/sales/return orders, company,
  BOM, attachments, barcodes. Use for inventory lookups, creating/updating parts, stock
  moves, and PO/SO workflows. For IMD self-dev IPN `{ClickUpId}@IMD` follow repo
  `imd-clickup-inventree-part-number` (do not invent IPNs). Triggers: inventree,
  inventree mcp, stock location, IPN, purchase order inventree, inventree part.
metadata:
  pattern: tool-wrapper
  specialization: mcp-integration
  domain: hardware
  mcp_key: inventree
  version: "1.2"
token_guardrails: |
  - GetMcpTools(server=user-inventree) before CallMcpTool; most tools use an `operation` string.
  - Never put Inventree API tokens in SysML, README, ClickUp, or skills.
  - Destructive ops (delete, stock adjust) only when the user clearly asked.
  - IMD self-dev: load repo imd-clickup-inventree-part-number before create (IPN = {ClickUpId}@IMD).
---

# MCP: InvenTree (`user-inventree`)

## When to use

- Look up or create **parts**, categories, parameters, BOM, suppliers
- Stock levels / locations / transfers
- Purchase, sales, return, or build orders
- Attachments and barcodes

## Tool discovery and auth

1. `GetMcpTools(server="user-inventree")` — read each tool’s `operation` list from the schema.
2. On `needsAuth` or **401**: `mcp_auth` (empty args) once → re-inspect server → retry.
3. If token revoked mid-session: finish non-Inventree work; leave Inventree as an explicit follow-up.

## Essential tools

| Tool | Domain |
|------|--------|
| `part` | Part CRUD, BOM, parameters, suppliers, manufacturers |
| `stock` | Stock items, locations, transfers, adjustments |
| `purchase_order` / `sales_order` / `return_order` / `build_order` | Order workflows |
| `company` | Suppliers / manufacturers / customers |
| `attachment` | Upload/list/download files on parts or orders |
| `barcode` | Scan / assign |
| `label` / `report` | Labels and reports |
| `system` | Instance / health style ops |

Pass **`operation`** as required by the schema (e.g. `list`, `get`, `create`). Prefer `list`/`get` before write ops.

## Typical workflows

### Find a part
1. `part` with `operation=list` (or search fields per schema) → note `pk` / IPN.
2. `part` `operation=get` (+ `get_stock` / `get_bom` as needed).

### Create or update a part
1. Confirm category and naming with the user.
2. `part` create/update with IPN and manufacturer fields.
3. Optional: `attachment` upload datasheet; `stock` if receiving units.

### Stock check
1. `part` `get_stock` or `stock` list filtered by part/location.
2. Summarise quantity and location; do not invent stock counts.

## IMD / ClickUp numbering (project-specific)

This skill is **generic** Inventree MCP usage. When the open repo uses IMD self-dev part numbers:

| Field | Value |
|-------|--------|
| ClickUp task ID | SysML `partNumber` |
| Inventree Mfr PN | same ClickUp ID |
| Inventree IPN | `{ClickUpId}@IMD` |

Load that repo’s **`imd-clickup-inventree-part-number`** before create/update. Do not invent ClickUp IDs for COTS; COTS keep vendor MPN / DigiKey.

## Pitfalls

- Wrong `operation` or missing `pk` → schema errors; re-read GetMcpTools.
- Duplicate IPNs — search before create.
- 401 after auth: check Inventree URL, API token validity, and user permissions on the instance.
---
