# Hybrid type playbook

## Basement goal

Shared root + one slice per type + short inter-slice contract.

## Procedure

1. List types in order (device → edge → cloud → UI is a good default).
2. Apply [basement-layout.md](../basement-layout.md) hybrid tree.
3. Run each type playbook **inside its slice** (`firmware/`, `server/`, `web/`, …).
4. Root README section **Contract**:
   - Who initiates (MCU publish / UI poll / server push)
   - Protocol (MQTT topic prefix, HTTP paths, serial baud)
   - Config ownership (which slice owns broker URL / Wi-Fi / pins)

## Example

`hybrid: mcu + online-server + html-ui`

```text
firmware/   # device agent
server/     # broker or API
web/        # dashboard
README.md   # contract
```

## Anti-patterns

- Single build that cross-compiles everything
- UI talking directly to MCU with undocumented ports
- Duplicating README content in every slice — root owns the contract
