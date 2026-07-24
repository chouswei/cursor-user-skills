# Narrow-viewport templates (control PCBA / deploy hardware)

Copy-paste starters; replace IDs and labels from `deploy-*.sysml`.

## Power (TB)

```mermaid
%%{init: {'themeVariables': {'fontSize': '13px'}, 'flowchart': {'nodeSpacing': 18, 'rankSpacing': 28}}}%%
%% Figure — Power from host
flowchart TB
  HOST["payloadHost\n5V 12V enable"]
  PDU["patPdu"]
  IN["mainPowerIn"]
  DIST["on-board distro"]

  HOST -->|5V 12V| PDU
  HOST -->|enable| PDU
  PDU --> IN --> DIST
```

## Compute on-board (TB)

```mermaid
%%{init: {'themeVariables': {'fontSize': '13px'}, 'flowchart': {'nodeSpacing': 16, 'rankSpacing': 26}}}%%
%% Figure — CM5 and STM32
flowchart TB
  subgraph cm5["cm5"]
    direction TB
    SW["application SW"]
    U0["uart0"]
    U1["uart1"]
    U3["uart3"]
  end
  subgraph mcu["mcu"]
    direction TB
    FW["acquisition FW"]
    IO["SPI GPIO"]
  end
  U3 <-->|921600| IO
```

## Edge → field (TB, one column)

```mermaid
%%{init: {'themeVariables': {'fontSize': '13px'}, 'flowchart': {'nodeSpacing': 14, 'rankSpacing': 22}}}%%
%% Figure — Edge ports
flowchart TB
  subgraph edge["PCBA edge"]
    direction TB
    P1["port A"]
    P2["port B"]
  end
  F1["field unit 1"]
  F2["field unit 2"]
  P1 --> F1
  P2 --> F2
```

## Short data leg (avoid LR chains)

```mermaid
%%{init: {'themeVariables': {'fontSize': '13px'}, 'flowchart': {'nodeSpacing': 16, 'rankSpacing': 24}}}%%
%% Figure — Optical downlink
flowchart TB
  A["cm5 PCIe"] --> B["PHY"] --> C["8p eth"]
  C --> D["opto module"]
  D -->|Tx| E["booster"]
  E --> F["ground"]
  F -->|Rx| E --> D
```

---

**Edge labels:** use SysML **link** ids on edges (`linkPduToControlPcba5V`), not multiline or Unicode (`→`). Caption carries bind/uart detail. [edge-label-parser-safety.md](../references/edge-label-parser-safety.md).
