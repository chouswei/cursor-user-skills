# Software port definition style guide

## Purpose

Logical interfaces between software parts (threads, state machines, services) in SysML v2 deploy/behaviour packages. Ports type connection ends; connections define which producer ports connect to which consumer ports.

## Naming

- **Port defs:** `{{InterfaceName}}OutPort` / `{{InterfaceName}}InPort` (e.g. `SoftwareDataOutPort`, `SoftwareDataInPort`, `StateCommandOutPort`, `StateCommandInPort`)
- **Connection defs:** `{{InterfaceName}}Flow` or `{{InterfaceName}}Link` (e.g. `SoftwareDataFlow`, `StateCommandFlow`)

See [common-library-naming-detailed.md](../../sysml-common-lib-contribution/references/common-library-naming-detailed.md) §3, §6.

## Structure

```
port def XxxOutPort;   // producer end
port def XxxInPort;    // consumer end
connection def XxxFlow {
  end port source : XxxOutPort;
  end port sink : XxxInPort;
}
```

Connection end roles should be descriptive: `source`/`sink`, `fromStateMachine`/`toComponent`, `producer`/`consumer`, etc.

## Optional item typing

When the port conveys a logical item (project-defined, e.g. `SpotAngle`, `ImageFrame`), add `in item` / `out item`:

```sysml
port def ImageFrameOutPort {
  out item frame : ImageFrame;
}
port def ImageFrameInPort {
  in item frame : ImageFrame;
}
```

For most software ports (data, commands, events), omit item — the connection type encodes semantics.

## Doc strings

- Use `doc /* ... */` for port and connection defs when helpful
- Document producer/consumer role and what flows (e.g. "logical data producer (spot angle, QPD angle)")

## Output location

- **Project-specific:** Port and connection defs in the project's deploy package (e.g. `packages/LeoLaserComm` in `deploy-leo-cubesat-laser-comm.sysml`)
- **Shared:** If reused across projects, consider a `SoftwarePorts` or `LogicalConnections` package

## Examples (reference)

- **SoftwareDataFlow** — logical data (spot angle, QPD angle, MEMS angle) producer → consumer
- **StateCommandFlow** — state machine → component (power-down, thread coordination)
