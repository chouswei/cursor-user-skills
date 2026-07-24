# SysML + MemNet atomisation patterns (user pack)

Use with [atomisation.md](../../mcp-memnet/references/atomisation.md), [sysml-memnet-snap.md](sysml-memnet-snap.md), and [sysml-memnet-cookbook-bridge.md](sysml-memnet-cookbook-bridge.md).

**Core discipline:** one row = one fact/link/status. Short pipe fields. Explicit `@EDG`. Stable ids from `query_warm`. **MUST NOT** create new rows tagged `@PARTD`, `@PORTD`, `@BEHD`, or `@TASK` (legacy aliases — re-snap to unified tags on warm miss).

## Canonical `session_open` map (copy verbatim)

```text
@ART: id|title|source|kind|status|recycle
@SEC: id|art|heading|order|status|recycle
@CLM: id|sec|type|code|status|recycle
@ENT: id|name|kind|code|recycle
@PKG: id|qname|kind|status|recycle
@PRT: id|name|kind|role|status|recycle
@POR: id|name|kind|dir|typeRef|status|recycle
@CON: id|name|kind|ends|status|recycle
@BEH: id|name|kind|owner|status|recycle
@ITM: id|name|kind|status|recycle
@REQ: id|requirementId|text|status|recycle
@MOD: id|path|pkg|role|status|recycle
@SYM: id|name|kind|path|line|owner|status|recycle
@CONV: id|topic|rule|status|recycle
@DEC: id|task|question|options|chosen|recycle
@ISSUE: id|task|code|status|recycle
@TSK: id|goal|phase|status|recycle
@USR: id|topic|value|status|recycle
@EDG: id|from|rel|to|note|recycle
```

Field notes:

- `@PRT.role` — short domain tag (`power`, `compute`, `deploy`); empty if N/A.
- `@POR.dir` — `in|out|inout` for port usages; empty for port defs.
- `@POR.typeRef` — typed port/protocol name (for `typedBy` EDG).
- `@CON.ends` — `endA|endB` usage path.
- `@BEH.owner` — owning `@PRT` usage id or package qname.
- `@DEC.task` — parent `@TSK` id; `options` pipe-separated; `chosen` when decided.
- `@ISSUE.code` — ≤15 words backlog item.

## Stable id rules

| Tag | Id pattern | Example |
|-----|------------|---------|
| `@TSK` | `TSK_model_<short>` | `TSK_diagram_<figureId>` (placement graph per Mermaid figure) | `TSK_model_vfdl2` |
| `@PKG` | `PKG_<packageSuffix>` | `PKG_FoamLiteVer2Deploy` |
| `@MOD` | `MOD_<file_slug>` | `MOD_deploy_vfdl2` |
| `@PRT` | `PRT_<name>` | `PRT_edgePc` |
| `@POR` | `POR_<name>` | `POR_pwr_in_28v` |
| `@CON` | `CON_<linkName>` | `CON_linkRelayToCoil` |
| `@BEH` | `BEH_<name>` | `BEH_RunFoamCoverageDetection` |
| `@ITM` | `ITM_<name>` | `ITM_Power5V` |
| `@REQ` | `REQ_<requirementId>` | `REQ_VFDL2-MQTT-RELAY` |
| `@SYM` | `SYM_<name>` | `SYM_edgePc` |
| `@CONV` | `CONV_<topic>` | `CONV_port_naming` |
| `@DEC` | `DEC_<nn>` | `DEC_01` |
| `@ISSUE` | `ISS_<nn>` | `ISS_03` |

## `kind` enums (closed lists)

| Tag | Allowed `kind` |
|-----|----------------|
| `@PRT` | `partDef`, `partUsage` |
| `@POR` | `portDef`, `portUsage` |
| `@CON` | `connectionDef`, `connectionUsage`, `linkUsage` |
| `@BEH` | `stateMachine`, `action`, `calculation` |
| `@ITM` | `itemDef`, `flowItem` |
| `@SYM` | `partDef`, `partUsage`, `portDef`, `portUsage`, `requirement`, `connection`, `behaviour`, `satisfy`, `allocate`, `package` |
| `@PKG` | `deploy`, `requirements`, `connections`, `behaviour`, `root`, `library`, `common` |
| `@ART` | `report`, `interconnection`, `behaviour`, `requirements`, `traceability` |
| `@CLM.type` | `fact`, `decision`, `assumption`, `convention`, `conclusion`, `stat`, `pipe` |
| `@TSK.phase` | `model`, `sync`, `audit`, `refactor`, `report`, `verify`, `pipe`, `route` |

## Recycle policy

| recycle | Tags |
|---------|------|
| `persistent` | `@PRT`, `@POR`, `@CON`, `@BEH`, `@ITM`, `@REQ`, `@PKG`, `@MOD`, `@SYM`, `@CONV`, `@ART`, `@SEC`, `@CLM`, `@USR`, campaign `@TSK` |
| `delete_on_settle` | `@DEC`, `@ISSUE`, sync/refactor sub-`@TSK` |

## SysML construct → MemNet

| SysML v2 in `.sysml` | MemNet row(s) | Same-batch `@EDG` (required) |
|---------------------|---------------|------------------------------|
| `part def` | `@PRT` kind=`partDef` + `@SYM` kind=`partDef` | `declaredIn`→`@PKG`; `inFile`→`@MOD` |
| part usage | `@PRT` kind=`partUsage` + `@SYM` kind=`partUsage` | `declaredIn`→`@PKG`; `inFile`→`@MOD` |
| `port def` | `@POR` kind=`portDef` + `@SYM` kind=`portDef` | `declaredIn`→`@PKG`; `inFile`→`@MOD` |
| port usage | `@POR` kind=`portUsage` + `@SYM` kind=`portUsage` | `declaredIn`; parent `@PRT` `hasPort`→`@POR`; `typedBy` if typed |
| connection / `link*` | `@CON` + `@SYM` | `declaredIn`; `connects` or `ends` field; **`typedBy`→`CONDEF_<DefName>`** (connection def from SysML `connection linkFoo : Bar`) |
| `requirement def` | `@REQ` + `@SYM` kind=`requirement` | `declaredIn`→requirements `@PKG` |
| `assert satisfy` / `satisfy` | **`@EDG` only** rel=`satisfies` | `@PRT`/`@BEH` → `@REQ`; `@SYM` kind=`satisfy` **only** for line locator |
| `allocate` | **`@EDG` only** rel=`allocates` | `@BEH`/`@PRT` → target `@PRT` |
| `state def` / behaviour | `@BEH` kind=`stateMachine` + `@SYM` kind=`behaviour` | `declaredIn`; `allocates` if allocated |
| `action def` | `@BEH` kind=`action` + `@SYM` | `declaredIn` |
| `item def` / `flow of` | `@ITM` + optional `@EDG` rel=`flowOf` | `declaredIn` |
| site convention | `@CONV` | `@TSK` `constrained_by`→`@CONV` |
| open design fork | `@DEC` | `@TSK` `owns`→`@DEC` |
| backlog (not in SysML) | `@ISSUE` or `@CLM` type=`assumption` | `@TSK`/`@SEC` `contains` |

**Batch rule:** every new `@PRT` / `@POR` / `@CON` **MUST** include `declaredIn` + `inFile` (`@SYM`→`@MOD`) in the **same** `add`/`update`. Cross-package types **MUST** include `typedBy`.

## EDG relations (SysML closed list)

`satisfies`, `allocates`, `declaredIn`, `hasPort`, `typedBy`, `connects`, `realizes`, `owns`, `inFile`, `contains`, `mentions`, `constrained_by`, `dependsOn`, `audits`, `flowOf`, `declaredAs`

**Diagram placement** (`TSK_diagram_*` — see [sysml-memnet-pipeline.md](sysml-memnet-pipeline.md) § Diagram placement):

| Rel | From → To | Purpose |
|-----|-----------|---------|
| `figure_includes` | `TSK_diagram_*` → `@PRT` | Node in figure scope |
| `figure_uses` | `TSK_diagram_*` → `@CON` | Edge in figure scope |
| `anchor_of` | `@PRT` → `TSK_diagram_*` | Hub / max-degree anchor |
| `adjacent_to` | `@PRT` → `@PRT` | Mate pair (same rank, consecutive declare#) |
| `documents` | `TSK_diagram_*` → `@SEC` | Report section owning the figure |

`typedBy` on `@CON`: `@EDG` from `CON_<linkName>` → `CONDEF_<ConnectionDefName>` (grep `connection link<Name> : <Def>` in deploy).

## Example: PDU-style mini-seed (unified tags)

```text
@TSK: TSK_model_pdu|Model 6U CubeSat PDU|model|in_progress|persistent
@PKG: PKG_PDU|project/pdu-controller|deploy|active|persistent
@PKG: PKG_LIB|library/power-ports|library|active|persistent
@MOD: MOD_pdu|models/deploy-pdu.sysml|PKG_PDU|deploy|active|persistent
@CONV: CONV_port_naming|ports|power ports end in _pwr|active|persistent
@REQ: REQ-01|REQ-01|Total output 15 W avg 20 W peak|active|persistent
@PRT: PRT_PDUController|PDUController|partUsage|power|active|persistent
@POR: POR_pwr_in_28v|pwr_in_28v|portUsage|in|Power28V|active|persistent
@CON: CON_pwr_in|linkPwrIn|linkUsage|Battery.pwrOut|PDU.pwr_in_28v|active|persistent
@SYM: SYM_PDUController|PDUController|partUsage|models/deploy-pdu.sysml|42|PRT_PDUController|active|persistent
@EDG: E01|TSK_model_pdu|owns|MOD_pdu|scope|persistent
@EDG: E02|MOD_pdu|ownsPackage|PKG_PDU|scope|persistent
@EDG: E03|PRT_PDUController|declaredIn|PKG_PDU||persistent
@EDG: E04|SYM_PDUController|inFile|MOD_pdu|loc|persistent
@EDG: E05|PRT_PDUController|hasPort|POR_pwr_in_28v||persistent
@EDG: E06|PRT_PDUController|satisfies|REQ-01||persistent
@EDG: E07|TSK_model_pdu|constrained_by|CONV_port_naming|convention|persistent
```

## Example: lightweight project skeleton (outputs + model)

```text
@TSK: TSK_model_underwater|Model underwater acoustic link|model|in_progress|persistent
@ART: ART_underwater-design|Underwater link design|outputs/system-design-report/index.md|report|active|persistent
@SEC: S01|ART_underwater-design|Overview|1|active|persistent
@CLM: C01|S01|fact|bidirectional acoustic command telemetry link|active|persistent
@REQ: REQ_UWL05|UWL-05|SHALL provide bidirectional link|active|persistent
@PRT: PRT_Modem|AcousticModem|partUsage||active|persistent
@EDG: E01|TSK_model_underwater|owns|ART_underwater-design|scope|persistent
@EDG: E02|PRT_Modem|satisfies|REQ_UWL05|design|persistent
```

## Example: after sysml-view-doc-sync

```text
@TSK: TSK_sync_power|Sync after power rail|sync|in_progress|delete_on_settle
@CLM: C10|S03|fact|24V rail feeds modems via fuse F3|active|persistent
@CON: CON_pwr_modem_tx|linkPowerToModemTX|linkUsage|Rail.out|ModemTX.powerIn|active|persistent
@EDG: E20|CON_pwr_modem_tx|declaredIn|PKG_deploy|origin|persistent
@EDG: E21|C10|mentions|CON_pwr_modem_tx|subject|persistent
```

## Example: open decision (transient)

```text
@DEC: DEC_01|TSK_model_pdu|Command channel UART vs GPIO|UART|Simple GPIO||delete_on_settle
@EDG: E30|TSK_model_pdu|owns|DEC_01|fork|delete_on_settle
```

When user chooses: `update` `@DEC.chosen`; settle `@DEC`.

## Linking doc claims to model elements

1. Use `mcp-sysmledgraph` or `mcp-sysml-v2` `getDefinition`/`getSymbols` for exact names.
2. Create/update `@PRT`/`@POR`/`@CON`/`@REQ` with unified `kind`.
3. Add `@EDG` from `@CLM`/`@SEC` — `mentions`, `satisfies`, `documents`.
4. On rename: refactor skill + `update` MemNet ids; refresh `@SYM.line`.

**Locators:** `name` + `path` authoritative; `@SYM.line` ephemeral — refresh after every validated edit ([sysml-memnet-snap.md](sysml-memnet-snap.md)).

## Anchor strategy

- Campaign → `TSK_model_<short>`
- Mermaid figure placement → `TSK_diagram_<figureId>` ([mermaid-placement-by-degree.md](../../mermaid/references/mermaid-placement-by-degree.md))
- Part/port under edit → `PRT_<name>` / `POR_<name>` / `SYM_<name>`
- Requirement audit → `REQ_<requirementId>`
- Pending choice → `DEC_<nn>`
- Convention → `CONV_<topic>`
- Outputs section → `@SEC` id

Warm depth 2 default; increase only when needed.

## Quick tag reference

| Tag | Id example | Purpose |
|-----|------------|---------|
| @PKG | PKG_FoamLiteVer2Deploy | Logical package / file group |
| @MOD | MOD_deploy_vfdl2 | One `models/*.sysml` file |
| @PRT | PRT_edgePc | Part def or usage (`kind` discriminates) |
| @POR | POR_ethernet | Port def or usage |
| @CON | CON_linkRelayToCoil | Connection or link |
| @BEH | BEH_FoamDetection | State machine or action |
| @ITM | ITM_Power5V | Item / flow item |
| @REQ | REQ_VFDL2-MQTT-RELAY | Requirement |
| @SYM | SYM_edgePc | Edit locator (path + line) |
| @CONV | CONV_port_naming | Site convention |
| @DEC | DEC_01 | Open design fork |
| @ISSUE | ISS_03 | Backlog not yet in model |
| @ART/@SEC/@CLM | ART_vfdl2, S02, C10 | Outputs / claims |
| @TSK | TSK_model_vfdl2 | Campaign anchor |
| @EDG | E42 | Typed relation |
