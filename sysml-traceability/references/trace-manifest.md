# Trace manifest

**Purpose:** Provide a canonical, project-agnostic input contract for projecting SysML v2 model elements to external tracking systems or documentation boards.

## Manifest structure

The manifest MUST be a flat Markdown table or domain-specific ASCII wire. It MUST NOT include implementation-specific details for the target board (e.g. ClickUp IDs or list names).

### Required fields

| Field | Description | Constraint |
|---|---|---|
| **kind** | The SysML v2 element type (e.g. `requirement`, `part`, `port`, `interface`, `allocation`). | MUST use lowercase kebab-case. |
| **qname** | The fully qualified name of the element in the SysML model. | MUST use double-colon separator (e.g. `Model::Package::Element`). |
| **target** | The target of an `allocate` or `satisfy` relationship, if applicable. | MUST be the qname of the destination element; `null` if not a relationship. |

## Usage constraints

- **Source of Truth:** The SysML v2 model is the SSOT. The manifest is a derived projection input.
- **Independence:** The manifest MUST NOT contain logic or triggers for a specific external service.
- **Integrity:** Every `qname` in the manifest MUST exist in the model and be validated via `user-sysml-v2` MCP before inclusion.
- **Relativity:** Use the manifest to bridge the gap between model structure and external status tracking without polluting the model with foreign IDs.

## Projection contract

The manifest serves as the **boundary** between modelling and tracking:
1.  **Extract:** A worker reads the model and produces the manifest.
2.  **Project:** A separate worker (e.g. `clickup-project-management`) consumes the manifest and synchronises the external board.
3.  **Sync:** The manifest MUST NOT be committed to the repository if it contains transient data; it is a session-local artifact.

---
[trace manifest | kind | qname | allocate]
