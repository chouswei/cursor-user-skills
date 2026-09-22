---
name: mcp-sysmledge
description: >-
  Prefer SysMLEdge product MCP sysmledge (WWW droplet face). Allowlist includes
  openProject/closeProject; tip≠face; no tunnel-as-primary.
metadata:
  pattern: tool-wrapper
  version: "1.1"
---
# MCP: SysMLEdge product face (`sysmledge`)

**Prefer `sysmledge` WWW face** (droplet nip.io `/mcp` + Bearer). tip≠face.

## Allowlist

`openProject` · `closeProject` · `rev_status` · `ask` · `gql` · `pin_map` · `propose`

## Rules

- Day-1 SysMLEdge product work -> **sysmledge only**
- When overlay + `rev_status` `working_ssot=graph`: this face is the working model SSOT. MUST NOT invent structure from Windows files then.
- `memnet-pi` is tip OPS-ONLY -- never a model SSOT, never product query path
- **No tunnel-as-primary** — `localhost:18776` / mcp-tunnel is legacy ops, not current day-1
- Do not put secrets/tokens in skills or prompts

## Multitask

Both MCPs visible → follow `sysmledge-cursor-multitask`.

## Pair

`sysmledge-workflow` / `sysmledge-cursor-multitask` / `memnet-multitask` / `memnet-use` / `mcp-memnet`
