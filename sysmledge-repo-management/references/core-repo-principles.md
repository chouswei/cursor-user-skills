# SysMLEdgePrj open-gate principles

## Classify

- The subject is the git repo root. Match the directory name to `SysMLEdgePrj-*`.
- A parent folder that also starts with `SysMLEdgePrj-` is not a second repo. Use the root that contains `project.toml`.
- `project.toml` key `repo` must equal that directory name. If it differs, report the mismatch and do not rename anything.
- `modelbasedPrj-*` repos are out of scope. Stop and follow that repo's `AGENTS.md`.

## Submodules

- Run `git submodule update --init --recursive` only when `.gitmodules` exists at the repo root.
- Read `.gitmodules` for paths and URLs. Do not assume every tree pins `sysml-models/libs`.
- A non-zero exit code is a gap in the open report. Do not delete or re-point a submodule to force success.

## Identity

- `projectId` is `[project].name` in `project.toml`. Copy that string into `rev_status`. Do not invent or reuse another tree's id.
- Operator `README.md` must state the SSOT kind: **repo-based** or **SysMLEdge-based**. If the line is missing, record the gap. Do not guess the kind from the folder prefix alone.
- `AGENT-CONTEXT.md`, when present, holds the tip MemNet catalog session and the campaign cue. Tip MemNet is not the product face and not the model SSOT.

## Face

- Product MCP is `sysmledge` / `user-sysmledge`.
- `rev_status` is allowed without a human gate. `openProject` and `closeProject` stay human-gated. This skill does not call them.
- When `rev_status` shows `working_ssot=graph` for this `projectId`, the desk is the working model. `sysml-models/` is the backup after a human Save.
- When the face is unbound, or `rev_status` errors, files under `sysml-models/` are the only editable model until a human `openProject` sticks. Do not pretend graph reads succeeded.
- Do not use Foam. Do not use `sysmledgraph`.

## Hand-off

- After the open report, modelling changes follow `sysmledge-workflow`.
- Proposals, when an agent may write, go under `sysml-models/proposals/<id>/` only. They are not the SSOT.
- Part folders and allocate rules stay in the open repo's `AGENTS.md` and `.cursor/rules/`. `deploy.sysml` wins over `[parts].roots` in `project.toml`.

## Retrieval seeds

SysMLEdgePrj, open repo, submodule, project.toml, projectId, README SSOT, rev_status, SysMLEdge face, modelbasedPrj stop
