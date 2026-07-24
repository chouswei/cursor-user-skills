# New project checklist (reference)

Use with [../SKILL.md](../SKILL.md). Replace `<slug>`, `<Prefix>`, `<PREFIX>` placeholders.

## Naming example

| user_name | slug | package_prefix | req_ids |
|-----------|------|----------------|---------|
| Delta-DataCentreHeatExchangeUnit-TestBench | delta-datacentre-heat-exchange-unit-test-bench | DeltaDCHXU | DDCHXU-R1… |
| Temperature and I-V Curve | temperature-iv-curve | TempIVCurve | none in early scaffold |
## config.yaml `model_files` (minimal + ISQ)

```yaml
model_dir: models
model_files:
  - ../../../libs/omg/SysML-v2-Release/sysml.library/Kernel Libraries/Kernel Semantic Library/Base.kerml
  - ../../../libs/omg/SysML-v2-Release/sysml.library/Kernel Libraries/Kernel Data Type Library/ScalarValues.kerml
  # … ISQ/SI block (copy from temperature-iv-curve/config.yaml) …
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

## Index row template (projects/README.md)

```markdown
| **<slug>** | <one-line purpose>; **<PREFIX>-R*** reqs. | [README](<slug>/README.md) |
```

## Post-scaffold commands

```powershell
cd sysml-v2-models
python scripts/visualize.py --project <slug> --diagram bdd --format svg
```

Expected: `projects/<slug>/outputs/bdd.svg` (or load error to fix before commit).
