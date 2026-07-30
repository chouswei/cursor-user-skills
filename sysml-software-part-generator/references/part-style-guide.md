# Software part definition style guide

## Purpose

Software part definitions (threads, state machines, services, composites) in SysML v2 deploy/behaviour packages. Use **sysml-software-port-generator** first to define port and connection types; this skill produces the part defs that use them.

## Naming

- **Part defs:** PascalCase, no suffix (e.g. `CameraThread`, `QpdThread`, `PatApplicationStateMachine`, `PatControlSoftware`)
- **Member parts:** camelCase (e.g. `cameraThread`, `rollingStorage`)
- **Ports:** camelCase (e.g. `spotAngleOut`, `dataIn`, `stateCommandOut`)
- **Attributes:** camelCase (e.g. `imageRateHz`, `positionUpdateRateHz`)

See [common-library-naming-detailed.md](../../sysml-common-lib-contribution/references/common-library-naming-detailed.md) §4, §5.

## Structure (simple part)

```
part def XxxThread {
  doc /* Role, rate, inputs/outputs. */
  attribute rateHz : FrequencyValue = N [SI::Hz];   // optional
  port outPort : XxxOutPort;
  port inPort : XxxInPort;
}
```

## Structure (composite part)

```
part def XxxSoftware {
  doc /* Aggregation of sub-components. */
  part subPart1 : SubPart1;
  part subPart2 : SubPart2;
  connection linkX : XxxFlow {
    end port source ::> subPart1.outPort;
    end port sink ::> subPart2.inPort;
  }
}
```

## Common attribute types

| Attribute | Type | Example |
|-----------|------|---------|
| Rate (Hz) | FrequencyValue | `30 [SI::Hz]`, `10000 [SI::Hz]` |
| Baud | Integer | `921600` |
| Imports | ScalarValues, ISQ, SI | For Integer, FrequencyValue |

## Doc strings

- Use `doc /* ... */` — describe role, update rate, data flow, state handling
- No semicolon after doc block

## Output location

- **Project-specific:** Part defs in project deploy or behaviour package (e.g. `deploy-<project>.sysml`)
- Define port and connection types in the same package (or use sysml-software-port-generator first)

## Examples (reference)

- **CameraThread** — image rate 30 Hz; spotAngleOut, spotDataOut
- **QpdThread** — position update >10 kHz; qpdAngleOut, qpdDataOut
- **MemsControlThread** — PID loop 10 kHz; cameraAngleIn, qpdAngleIn, memsAngleOut
- **PatControlSoftware** — composite: OsAndDrivers, threads, RollingStorage, connections
