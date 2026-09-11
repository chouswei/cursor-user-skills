# New project checklist (reference)

Use with [../SKILL.md](../SKILL.md). Replace `<slug>`, `<Prefix>`, `<PREFIX>` placeholders.

**House default root:** `sysml-models/`. **Legacy opt-in:** `sysml-v2-models/projects/<slug>/` when the repo already uses that pack layout.

## Naming example

| user_name | slug | package_prefix | req_ids |
|-----------|------|----------------|---------|
| Delta-DataCentreHeatExchangeUnit-TestBench | delta-datacentre-heat-exchange-unit-test-bench | DeltaDCHXU | DDCHXU-R1... |
| Temperature and I-V Curve | temperature-iv-curve | TempIVCurve | none in early scaffold |
## config.yaml `model_files` (minimal + ISQ)

Copy the OMG/ISQ block from an existing tree, then fix relatives for the chosen root.

```yaml
model_dir: models
model_files:
  # OMG Kernel + ISQ/SI -- copy from an existing config.yaml; do not invent paths
  - connections-<slug>.sysml
  - requirements-<slug>.sysml
  - deploy-<slug>.sysml
  - behaviour-<slug>.sysml
  - root-<slug>.sysml
```

## root-<slug>.sysml template

```sysml
package <Prefix>Root {
  private import <Prefix>Connections::*;
  private import <Prefix>Requirements::*;
  private import <Prefix>::*;
  private import <Prefix>Behaviour::*;
}
```

Omit imports for packages you did not create.

## Index row template

House (`sysml-models/README.md` or repo README):

```markdown
| **<slug>** | <one-line purpose>; **<PREFIX>-R*** reqs. | [README](sysml-models/README.md) |
```

Legacy (`sysml-v2-models/projects/README.md`):

```markdown
| **<slug>** | <one-line purpose>; **<PREFIX>-R*** reqs. | [README](<slug>/README.md) |
```

## Post-scaffold commands

House: SysML v2 MCP **validate** on `sysml-models/models/*.sysml`. On a SysMLEdge repo, after human Save, `rev_status` must bind.

Legacy pack:

```powershell
cd sysml-v2-models
python scripts/visualize.py --project <slug> --diagram bdd --format svg
```

Expected (legacy): `projects/<slug>/outputs/bdd.svg` (or load error to fix before commit).
