---
name: fusion-electronics-fetch
description: >-
  Fetch Autodesk Fusion 360 Electronics schematics (.sch) and boards (.brd) via
  Fusion MCP into modelbasedPrj parts/*/hardware/. Use when the user asks to
  pull, fetch, export, or sync Fusion electronics, PCB, schematic, Eagle cache,
  or ElectronFileOutput for a part. Triggers: fusion360 electronics fetch,
  fusion MCP schematic, .sch .brd, PA107/PCBA from Fusion, fusion-pa107.
metadata:
  pattern: tool-wrapper
  specialization: mcp-integration
  pack: user
  domain: pcba
  mcp_key: fusionMCP
  version: "1.0"
token_guardrails: |
  - GetMcpTools(server=user-fusionMCP) before CallMcpTool shapes.
  - Never fusion_mcp_execute document save unless the user explicitly asks.
  - Prefer Neutron ElectronFileOutput .sch/.brd copy over inventing netlists.
  - Landing path: parts/<part>/hardware/fusion-<slug>/ (ASCII only).
---

# Fusion Electronics fetch (`user-fusionMCP`)

## When to use

- Pull live Fusion Electronics schematic/PCB into a system repo part tree
- Record Fusion lineage URNs next to local `.sch` / `.brd` snapshots
- BOM/net extract from fetched Eagle XML schematics

## Prerequisites

1. Fusion 360 running; **Preferences → General → API → Fusion MCP Server** on (default **27182**).
2. Cursor MCP: `"fusionMCP": { "url": "http://127.0.0.1:27182/mcp" }` (server id often `user-fusionMCP`).
3. Target part folder exists (`parts/<part>/part.toml`) in a `modelbasedPrj-*` layout.

If connection refused → Fusion up + MCP checkbox + port match. Layout SSOT: `c:/Projects/SYSTEM-REPO-LAYOUT.md` (Fusion MCP section).

## Tool map

| Tool | Role |
|------|------|
| `fusion_mcp_read` | `document` search/open/recent; optional `screenshot` |
| `fusion_mcp_execute` | `document` open/close; `script` for activate/list |
| `fusion_mcp_electronics_read` | Parts/Nets/Schematic/Board/Element (active electronics product) |

Detail and pitfalls: [references/mcp-and-cache.md](references/mcp-and-cache.md).

## Workflow

```
Fetch progress:
- [ ] 1. Discover tools / confirm MCP healthy
- [ ] 2. Search + open Fusion electronics docs
- [ ] 3. Optional: electronics_read BOM/nets sanity
- [ ] 4. Locate ElectronFileOutput sch/brd
- [ ] 5. Copy into parts/<part>/hardware/fusion-<slug>/
- [ ] 6. Write fusion.toml + bom-extract + README; patch part.toml
```

### 1. Discover

`GetMcpTools(server="user-fusionMCP")`. Prefer ready status before open/read.

### 2. Search and open

- Read: `queryType=document`, `operation=search`, `name=<substring>`, optional `project`.
- Execute: `featureType=document`, `object.operation=open`, `object.fileId=<urn:adsk.wipprod:dm.lineage:...>`.
- Fuzzy search often returns sch + brd + libraries; open **product** schematics/boards, skip Packet libraries unless requested.
- Open may fail for some lineage IDs while another ID of the same name works — try siblings from search.
- List open docs: `queryType=document`, `operation=open` (no fileId).

Activate a doc via short `featureType=script` (`documents.item(i).activate()`).

### 3. Electronics read (optional sanity)

`fusion_mcp_electronics_read` with `entity_type` e.g. `electronics.Part`, `electronics.Net`, `electronics.Schematic`.

**Pitfall:** read often stays bound to one open electronics product even after activating another Fusion document. Treat MCP BOM as secondary; **always** copy cache files for ground truth.

### 4. Cache files (authoritative export)

After open, Fusion writes under:

`%LOCALAPPDATA%/Temp/Neutron/ElectronFileOutput/<session>/`

- `sch-<uuid>/<Name>.sch`
- `brd-<uuid>/<Name>.brd`
- optional `small.png`

List that session’s dirs; match names to the designs just opened.

### 5. Land in repo

```
parts/<part>/hardware/fusion-<slug>/
  <Name>.sch
  <Name>.brd
  board-preview.png          # optional
  fusion.toml
  bom-extract.json
  README.md
```

- ASCII path segments only (`fusion-pa107`, not spaces).
- Rename spaces in filenames to hyphens when copying (e.g. `RF-power-amplifier-PA107.brd`).
- Do **not** `document save` in Fusion unless the user asks.

### 6. Metadata

- `fusion.toml` — project, folder, schematic/board `lineage_id`, local `file` names ([assets/fusion.toml.template](assets/fusion.toml.template)).
- `bom-extract.json` — `python scripts/extract_bom.py <path-to.sch>` (writes beside the `.sch`).
- Short `README.md` — Fusion names + IC highlights + caveats (e.g. single vs paralleled topology).
- Patch `parts/<part>/part.toml`: `fusion_hardware`, `fusion_schematic_lineage`, `fusion_board_lineage`.
- Touch `AGENT-CONTEXT.md` only if the repo already keeps a Fusion one-liner there.

## Pairing

- Layout SSOT: `SYSTEM-REPO-LAYOUT.md` (`parts/*/hardware/`, Fusion MCP).
- SysML stays architecture SSOT; this skill only snapshots CAD electronics.
- After fetch: compare ClickUp / `deploy.sysml` topology vs schematic (IC count, rails).

## Non-goals

- Editing Fusion geometry or committing `.sch`/`.brd` unless the user asks
- Inventing netlists when cache files are missing
- Mech-only Fusion designs (separate Fusion MCP scripts; still land under part `hardware/` if needed)
