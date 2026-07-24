# SysML connections — reference

## Where connections live

| Kind | Typical files | Syntax hint |
|------|---------------|-------------|
| Deployment (hardware) | `deploy-<project>.sysml` | `connection linkName : SpiLink { end port master ::> part.port.path; end port slave ::> ... }` |
| Nested ports | Part defs, HAT models | `port computeIn : SomePort { port spi1 : SpiFourPinPort { ... } }` |
| Software logical flow | Same deploy or `behaviour-*.sysml` | Project-specific `connection def` + `SoftwareDataFlow`-style links |
| Shared link types | `libs/common/connections/connections.sysml` | Reuse `SpiLink`, `UartLink`, … before adding new defs |

## End roles

Match the `connection def` in `SharedConnections`: e.g. `SpiLink` uses `master` / `slave`; `UartLink` uses `host` / `device`; `GpioExpansionLink` uses `a` / `b`. Wrong role names break validation.

## PAT / pinmap projects

If `mappings/*_pinmap_from_sysml.yaml` lists connection names, add or adjust entries when deploy connection names or hat ports change. Run:

`python sysml-v2-models/scripts/check_pinmap_from_sysml.py --project <name>`

## Anti-patterns

- Document-only wiring without updating `deploy-*.sysml`.
- Skipping validate after `.sysml` edits.
- Using `visualizeFile` or `visualize.py` unless the user asked (see mcp-sysml-v2 `references/cursor-mcp-rules.md`).
