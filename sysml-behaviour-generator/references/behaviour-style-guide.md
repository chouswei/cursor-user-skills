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
- Named **`action def`** sequences are appropriate for **ordered commissioning** and **power-cycle recovery** when the project already uses that style.

## Plant / multi-edge patterns (generic)

When the user asks for plant bring-up or recovery, model (do not invent site IPs in stubs):

| Pattern | Intent |
|---------|--------|
| Ordered commissioning | Sticky DHCP → MQTT/transport → switch status visible → device-table commit |
| Sticky MAC reservation | Reserved hosts keep IPv4 across reconnect; guest pool for unknowns only |
| Power-down / up | Link → DHCP renew → MQTT reconnect (backoff); inventory persists |
| Multi-edge join | Many edge actors; per-site address bands / role offsets on one plant LAN |

Pair with **refine** / **derive** requirement children under the parent theme; sync **`outputs/diagrams/`** via **sysml-view-doc-sync**.

## Software data flow in deploy

- Threads and **`SoftwareDataFlow`** / **`StateCommandFlow`** stay in **`deploy-*.sysml`** unless the project splits them; this skill focuses on **`behaviour-*.sysml`** lifecycle/state modelling.

## Anti-patterns

- Behaviour-only narrative in Markdown with no `behaviour-*.sysml` update.
- `root-*` not importing the new package → validate failures or invisible types.
- Using **visualizeFile** or **visualize.py** without user request.
- Hard-coding lab/office IPs into shared behaviour stubs.