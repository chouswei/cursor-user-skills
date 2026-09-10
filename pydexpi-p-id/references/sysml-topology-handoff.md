# SysML topology handoff (shared)

Topology from the P&ID / flowsheet stack (pyDEXPI, SFILES2, GGILES) is **evidence** for the product SysML model. Structural SSOT stays **SysML v2 `.sysml`**.

| Graph / string element | Lands in SysML as | If missing in model |
|------------------------|-------------------|---------------------|
| Equipment / instrument node | existing `part` (+ ports) | **gap** -- do not invent equipment |
| Piping / process edge | `port` + `item`/`flow` + `connection`/`bind` | gap / ISSUE |
| Signal / control edge | ports + connections per locks | gap |
| SFILES / GGILES token only | same after decode to graph | never invent from string alone |

**Locks win** (user/PDF-named topology and assay locks). Conflict with locks -> **contradict** if `.sysml` does the opposite, else gap.

SysML topology landing is owned by the SysML specialist (out-of-pack bridge skill `sfiles-pydexpi-sysml-bridge` when present locally). Diagram owns load/encode/draw; SysML owner edits `.sysml`.

Prefer conceptual/process graph over complete DEXPI for SoI wiring. No invented mL/lambda/size. MemNet delta only **after** `.sysml` validate -- do not treat NetworkX as MemNet SSOT.
