# SysML item definitions — style guide (repo)

## Naming

- **`item def`** names: **PascalCase** (e.g. `Power12V`, `DevelopmentPlan`, `TelemetryFrame`).
- **Attributes** on items: **camelCase** with ISQ/SI value types when physical (see `FlowItems`).

## Where to define

| Scope | File / package | When |
|-------|----------------|------|
| Shared across projects | `libs/common/parts/flow_items.sysml`, package `FlowItems` | Nominal power rails, reusable physical/logical flow types used by HardwarePorts or many projects |
| Single project | `deploy-<project>.sysml` or `behaviour-<project>.sysml` | Domain-specific documents, messages, plans (e.g. modelbase `DevelopmentPlan`) |

Do **not** add to `FlowItems` without confirming impact on **hardware_ports** load order and all consumers.

## Physical items

- Import **ISQ** and **SI**; use quantity-valued attributes (e.g. `nominalVoltage : ElectricPotentialDifferenceValue = 3.3 [SI::V]`).
- Follow patterns in **`flow_items.sysml`**.

## Logical / document items

- Empty body with **`doc /* purpose, producer, consumer */`** is acceptable (see **`DevelopmentPlan`** in modelbase deploy).

## Composite items

- **`item def`** with **nested `item`** members (e.g. `PoE` with `poePow` and `ethernetPayload`).

## Port and action binding

- **Ports:** `in item name : ItemType;` / `out item name : ItemType;` on port definitions that convey flow.
- **Actions:** `in item x : SomeItem;` / `out item y : SomeItem;` in action definitions (see **`behaviour-modelbase-development.sysml`**).

## Imports

- Project packages: **`private import FlowItems::*`** when referencing `Power3V3`, etc.
- Items defined in same package need no import for local references.

## Anti-patterns

- Duplicating an existing **`FlowItems`** type in a project package under a different name.
- **`item def`** without **`doc`** when the semantic is non-obvious.
- Skipping validate after changing common lib files.
