# Layout check

Check these paths. Record present or missing. Do not create missing paths in this skill.

| Path | Expect |
|------|--------|
| `README.md` | States SSOT kind: repo-based or SysMLEdge-based |
| `project.toml` | `[project].name` and `[project].repo` |
| `AGENTS.md` | LLM-facing routes for this tree |
| `AGENT-CONTEXT.md` | Tip catalog session and campaign cue, when the tree uses MemNet |
| `.gitmodules` | Present only when the tree has submodules |
| `sysml-models/config.yaml` | Load order |
| `sysml-models/models/` | Model files. Working model only when unbound or repo-based |
| `sysml-models/proposals/` | Agent proposals. Not SSOT |
| `sysml-models/outputs/` | Derived. Not the model SSOT |
| `parts/` | Implementation. Align after the working model |
| `.cursor/skills/` | Optional tree overlay |

`[parts].roots` in `project.toml` is informational. The deploy model in the working SSOT wins.

A missing overlay is not a fault. A missing `README.md` SSOT line is a fault.
