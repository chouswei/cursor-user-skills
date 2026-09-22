---
name: mcp-sysmledge
description: >-
  Prefer SysMLEdge product MCP sysmledge (panel sysmledge, namespace
  user-sysmledge). Allowlist: rev_status, ask, gql, pin_map, propose
  (openProject human-gated); tip≠face; no tunnel-as-primary.
metadata:
  pattern: tool-wrapper
  version: "1.2"
---
# MCP: SysMLEdge product face (`sysmledge`)

**Live product MCP:** panel `sysmledge`, namespace `user-sysmledge` (URL in `mcp.json` only). MUST NOT tip-as-face. MUST NOT treat a SKILL.md URL as live.

## Allowlist

`rev_status` · `ask` · `gql` · `pin_map` · `propose` (`openProject` human-gated; `closeProject` when closing)

## Rules

- Day-1 SysMLEdge product work -> **sysmledge only**
- When overlay + `rev_status` `working_ssot=graph`: this face is the working model SSOT. MUST NOT invent structure from Windows files then. Windows `sysml-models/` is backup.
- Graph write = `propose`; agent does not finish Save.
- MUST NOT invent `projectId`.
- `memnet-pi` is tip OPS-ONLY -- never a model SSOT, never product query path. MUST NOT tip-as-face.
- **No tunnel-as-primary** — stale local tunnel hosts are legacy ops, not current day-1; URL lives in `mcp.json` only
- Do not put secrets/tokens in skills or prompts

## Multitask

Both MCPs visible → follow `sysmledge-cursor-multitask`.

## Pair

`sysmledge-workflow` / `sysmledge-cursor-multitask` / `memnet-multitask` / `memnet-use` / `mcp-memnet`
