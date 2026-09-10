# P&ID / flowsheet stack (PI Research + project policy)

## Preferred order

1. **DEXPI / Proteus XML -> pyDEXPI -> NetworkX** -- skill `pydexpi-p-id`
   - AGPL-3.0 -- **flag before proprietary redistribute**
2. **Optional string views**
   - Flowsheet units -> **SFILES2** (`sfiles2`, MIT) -- graph <-> SFILES 2.0
   - Arbitrary typed graphs -> **GGILES** (`ggiles`, MIT) -- graph <-> sequence + tokenizer
3. **Demoted:** D2 ISA sketches (`d2-pid`) -- stakeholder only; no redraw spam without a clear target

## Upstream

| Package | Repo | License |
|---------|------|---------|
| pyDEXPI | https://github.com/process-intelligence-research/pyDEXPI | AGPL-3.0 |
| SFILES2 | https://github.com/process-intelligence-research/SFILES2 | MIT |
| GGILES | https://github.com/process-intelligence-research/Generalized-graph-line-entry-system | MIT |

## Related reading

- ChatP&ID (AIChE e70540) -- GraphRAG on DEXPI graphs
- Vogel et al. 2023 -- SFILES 2.0 paper
- DEXPI2graphML -- alternate GraphML path

## Install (box venv)

```bash
python3 -m venv .venv
.venv/bin/pip install pydexpi SFILES2 ggiles
```

Confirm imports before claiming installed.

## SysML landing

Graph/SFILES/GGILES -> ports/items/connections via the SysML specialist (out-of-pack bridge skill `sfiles-pydexpi-sysml-bridge` when present locally). No invent equipment; `.sysml` SSOT. Mapping table: `pydexpi-p-id/references/sysml-topology-handoff.md`.
