# SysMLEdge day loop -- STALE and propose (L3)

Normative names: [P0-contracts.md](https://github.com/chouswei/SysMLEdge/blob/main/docs/P0-contracts.md). Acceptance: [P1-acceptance.md](https://github.com/chouswei/SysMLEdge/blob/main/docs/P1-acceptance.md). Agent rules: [SysMLEdge AGENTS.md](https://github.com/chouswei/SysMLEdge/blob/main/AGENTS.md).

Load this file when STALE handling, proposal files, or the reject list need the exact shapes. Keep [../SKILL.md](../SKILL.md) as the loop.

## Revision identity

Every read that returns structure MUST include:

```text
rev.sha:    <40-char git SHA>
rev.stale:  true | false
```

APIs MUST return the full SHA. UI/MCP MAY show 7-12 hex chars. If the projection cannot name a SHA, the read MUST fail closed.

## STALE error (normative shape)

```text
code: STALE
rev.sha: <bound>
current.sha: <current or unknown>
hint: reproject from current SysML, or read with staleOk=true (read-only)
```

| Actor | MUST |
|------|------|
| Any surface | Show STALE. |
| Live-SSOT pretence | Refuse. |
| Writes to current SSOT | Refuse while STALE (import/save/reproject first, or target the bound rev as historical). |
| `staleOk` | Optional on **read-only** GQL. |
| `staleOk` + `propose` | Refuse. |

## Proposal files

`propose` creates or updates:

```text
sysml-models/proposals/<id>/
  PATCH.md
  delta.sysml
```

| Field | Rule |
|-------|------|
| `<id>` | Opaque (UUID or `prop-<short>-<n>`). |
| `PATCH.md` | MUST include `base.sha` (current SHA when proposed). If current moves, the proposal is invalid until regenerated or a human rebases. |
| `delta.sysml` | SysML text only. MUST NOT be GQL, Cypher, or a MemNet snapshot. |
| SSOT | Files outside `proposals/` change only on **human save** (whole-tree overwrite). |

Human apply: merge `delta.sysml` into `sysml-models/`, then Save (commit + reproject).

## Whole-tree SSOT

| Op | Rule |
|-----|------|
| Import | Zip or `sysml-models/` directory overwrites current; git commit; bind MemNet; previous graph nodes gone. Fail closed on invalid input. |
| Human save | Whole-tree overwrite of current from the working tree the human accepted. Git keeps history. |
| Download @ rev | SysML zip of `sysml-models/` at that rev only. |

`proposals/` MAY be omitted from a source zip of a published rev; if included, label it proposal material, not SSOT.

## v1 mapping (projection only)

Project only: `part`, `port`, `connection`, `partNumber`, ClickUp id, Inventree id -- when present in SysML at `rev.sha`. Locators: `qname=`, `path=` (file under `sysml-models/`). Unknown PLM ids: omit. Do not invent placeholders.

Identity of structure is SysML qname + file path + `rev.sha`. MUST NOT mint client `NEW` ids as SSOT identity.

## Reject list

1. Graph write-back as SSOT.
2. Kuzu as runtime, `graph.kuzu`, Cypher, or a long-lived Kuzu worker.
3. Full-tree dump as the only merge story for agents.
4. Serving the graph as downloadable source.
5. GQL that invents parts, ports, connections, or ids not in SysML at `rev.sha`.
6. Claiming P2 SaaS or P3 tenancy as shipped in the SysMLEdge seed.

## Historical MCP names (do not call)

Old codebase-sysmledgraph roles map to P0 names in [../SKILL.md](../SKILL.md). Do not call `indexDbGraph`, `cypher`, `query`, `context`, `impact`, `rename` (as a graph edit), or `worker` against Kuzu.

Retrieval seeds: STALE, staleOk, propose, base.sha, rev.sha, gql_read, rev_status, reproject, sysml-models/proposals, Kuzu refuse
