# SysML behaviour — style guide (repo)

## File and package

| Item | Rule |
|------|------|
| File | `behaviour-<projectfolder>.sysml` (lowercase, hyphens) |
| Package | Project-specific PascalCase, e.g. `SysmledgraphBehaviour`, `LeoLaserCommBehaviour` |
| Load order | After `deploy-<project>.sysml`; before **`root-<project>.sysml`** in `config.yaml` |
| Root | `Project<Project>` imports behaviour package explicitly |

## Imports

- `private import` deploy package and requirements package when transitions or docs reference parts or reqs.
- Add ScalarValues / ISQ / SI only if attributes use quantities.

## Events

- Model triggers as **`attribute def EventName { doc /* ... */ }`** (see sysmledgraph behaviour example).
- One event per user-visible or protocol signal; name with PascalCase verb-noun (e.g. `StartIndex`, `IndexComplete`).

## State machine

- Top-level **`state def Name { ... }`** with:
  - **`doc /* ... */`** on the state def.
  - **`entry; then <initialState>;`**
  - **`state stateId { doc /* ... */ }`**
  - **`transition name first source accept Event then target;`**
- Use clear transition names (`idle_to_running`).
- Document error/retry states when applicable.

## Activities and actions

- Prefer **state machines** in this repo’s examples; **actions/activities** follow project need and OMG textual syntax—validate with MCP after adding.

## Software data flow in deploy

- Threads and **`SoftwareDataFlow`** / **`StateCommandFlow`** stay in **`deploy-*.sysml`** unless the project splits them; this skill focuses on **`behaviour-*.sysml`** lifecycle/state modelling.

## Anti-patterns

- Behaviour-only narrative in Markdown with no `behaviour-*.sysml` update.
- `root-*` not importing the new package → validate failures or invisible types.
- Using **visualizeFile** or **visualize.py** without user request.
