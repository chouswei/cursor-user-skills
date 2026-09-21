# SysMLEdgePrj naming and migrate (L3)

Load when the user names **SysMLEdgePrj-***, asks to **rename/migrate** a `modelbasedPrj-*` tree onto that prefix, or scaffolds a new SysMLEdge product-face system repo. Keep [../SKILL.md](../SKILL.md) as the day loop.

Product contracts stay in SysMLEdge: [P0-contracts.md](https://github.com/chouswei/SysMLEdge/blob/main/docs/P0-contracts.md), [SysMLEdge AGENTS.md](https://github.com/chouswei/SysMLEdge/blob/main/AGENTS.md). Dual-MCP: [sysmledge-cursor-multitask](../../sysmledge-cursor-multitask/SKILL.md).

## Prefixes

| Prefix | Product MCP `sysmledge` | Author SSOT | When |
|--------|-------------------------|-------------|------|
| **`SysMLEdgePrj-*`** | YES (human-gated `openProject`, then day loop) | `sysml-models/` | System repo that is a SysMLEdge product tree |
| **`modelbasedPrj-*`** | NO (legacy / MemNet-only) | `sysml-models/` | Existing trees without a product face; do not pretend bind |

Shape: `SysMLEdgePrj-<Org>-<Name>` ASCII, same suffix as the old `modelbasedPrj-<Org>-<Name>` when migrating. Example: `modelbasedPrj-ITRI-PeritonealDialysisMonitoring` -> `SysMLEdgePrj-ITRI-PeritonealDialysisMonitoring`.

Greenfield SysMLEdge system repos MUST use **`SysMLEdgePrj-*`**. MUST NOT mint a new `modelbasedPrj-*` when the tree will have a product face.

## Product face (MUST / MUST NOT)

| MUST | MUST NOT |
|------|----------|
| Face name is **`sysmledge`**. Bind with human-gated `openProject` (`confirmHumanOpen=true`). | Invent `projectId`, `memnetSession`, or a PD/Foam bind in this pack or in SysMLEdge product `AGENTS.md`. |
| After bind: record live `projectId` / `rev.sha` / `rev.stale` / `memnetSession` from `rev_status`. Follow the day loop. | Reuse or rename `foam-beachhead` / Foam desk as this tree's face. |
| Unbound: edit `sysml-models/` + `sysml-v2` validate. Author SSOT stays the files. | Treat tip `memnet-pi` as the product face. |
| Agents propose under `sysml-models/proposals/<id>/`. | Silent overwrite of `sysml-models/` SSOT. |

SysMLEdge product `AGENTS.md` does **not** invent a PD bind. A `SysMLEdgePrj-*` overlay MAY declare that this tree binds on `sysmledge` with a **new** `projectId` when a human opens it. Until that bind exists, the repo is unbound: files are SSOT; GQL is not live-SSOT.

## Migrate `modelbasedPrj-*` -> `SysMLEdgePrj-*`

Operator + git. Agents update overlay files; they do not rename the GitHub repository.

1. **GitHub rename (human):** Settings -> Rename repository to `SysMLEdgePrj-<Org>-<Name>`. GitHub keeps a redirect from the old name. MUST NOT create a second empty repo and copy history by hand.
2. **Identity files:** `project.toml` `repo=`, root `README.md` tree heading, `AGENTS.md` layout line, derived `outputs/` mentions of the old prefix.
3. **Overlay:** replace any `*-repo-only` SysMLEdge skill with a `SysMLEdgePrj` overlay: face `sysmledge`, human `openProject`, never Foam, never invent ids. Route SysMLEdge work to pack `sysmledge-workflow`.
4. **Proposals:** add `sysml-models/proposals/README.md` (agents propose; human Save). Stub: [../assets/proposal-stub.md](../assets/proposal-stub.md).
5. **Local / Pi path:** keep the live checkout path until the operator moves it. MUST NOT invent a new host path. After they rename the folder, update `AGENT-CONTEXT.md` and any Pi-path rule in the same turn.
6. **Tip MemNet:** catalog session + campaign cue stay in `AGENT-CONTEXT.md`. Tip is not the product face.
7. **Pack pointers:** if a pack skill still says this tree is repo-only, update that row in the same pack change.

Validate: `sysml-v2` on touched `.sysml` if any; otherwise overlay + identity files only. After a human Save and bind, `rev_status` must name `rev.sha`.
