---
name: sysml-common-library-naming
description: >-
  Naming and style rules for shared SysML common libraries: package names, file names, ports, parts,
  connections, attributes, doc statements, and IMD/IPN conventions. Triggers: naming rules, common lib
  style, file/package naming, port naming, part naming, connection naming.
metadata:
  pattern: tool-wrapper
  domain: sysml-v2
  pairs_with: [sysml-common-lib-contribution, sysml-common-file-scale, sysml-hardware-part-generator, sysml-physical-port-generator, sysml-item-generator, sysml-software-part-generator, sysml-software-port-generator, sysml-requirements-generator]
---

# SysML common library naming

**Pattern:** Conventions live in this skill and `references/` — apply when naming or reviewing shared lib symbols (tool-wrapper: no separate executable; not code generation).

Use this skill for shared `sysml-v2-models/libs/common` naming and style decisions.

## Rules

- Packages: PascalCase, one top-level package per file, avoid shadowing OMG / Kernel names.
- Files: snake_case, with the file name reflecting the package.
- Ports: PascalCase with `Port` suffix; nested ports use camelCase member names.
- Parts: PascalCase. OTS parts use product names; custom / IMD parts use descriptive names plus optional ID.
- Connections: PascalCase, often ending in `Link`.
- Attributes and members: camelCase.
- Doc blocks: use `doc /* ... */` without a trailing semicolon.
- Qualified types: if the tool cannot resolve imports well, use qualified names like `HardwarePorts::SpiPort`.

## IMD / IPN

- InvenTree IPN format is `MfrPart#@MfrAbbr`.
- For custom PCBAs, use the ClickUp task ID as `partNumber`.
- IMD IPN format is `partNumber@IMD`.
- Keep the part name aligned across SysML, ClickUp, and InvenTree.

## When to apply

- New or updated shared parts, ports, connections, or FlowItems.
- Naming review for `libs/common`.
- Port / part / connection style questions before editing shared files.

## See also

- [common-library-naming-detailed](references/common-library-naming-detailed.md) — full sectioned rules (packages, files, ports, IPN, doc blocks).
- [sysml-common-lib-contribution](../sysml-common-lib-contribution/SKILL.md)
- [sysml-common-file-scale](../sysml-common-file-scale/SKILL.md)
- [sysml-v2-models/libs/common/README.md](../../../sysml-v2-models/libs/common/README.md)
