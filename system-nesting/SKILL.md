---
name: system-nesting
description: Recursively clarifies architecture by treating every part and relevant nested usage as a system. Use when detailing a system, digging into an architecture, reviewing system-of-systems structure, or when nested parts, ownership, interfaces, behaviour, or requirements are unclear.
metadata:
  version: "1.0"
---

# System nesting

## Doctrine

> all parts are systems; if it is not clear enough, dig into this system

Apply this doctrine whenever a system is being explained, reviewed, designed, or
decomposed.

## MUST

- Treat every part as a system boundary, including a relevant nested usage.
- At each layer, identify the system's purpose, owned parts, ports or
  interfaces, behaviours, and requirements.
- Recurse into child parts when ownership, interfaces, behaviour, or
  requirements are unclear at the current layer.
- Use the same analysis at every deeper layer until the open question is clear
  or an explicit unknown is recorded.
- Keep the current layer distinct from the child system being inspected.
- Explain how each child system contributes to its parent system.
- State the evidence and boundary used to stop recursion.

## MUST NOT

- Treat a part as an opaque box when its internal structure is needed to answer
  the question.
- Flatten all nesting into one undifferentiated architecture description.
- Infer ownership, interfaces, or behaviour from names alone.
- Invent a child system, connection, or responsibility to fill a modelling gap.
- Stop at a parent boundary merely because the child is inconvenient to inspect.
- Present unresolved detail as established architecture.

## Model-based repositories

When working in a `modelbasedPrj-*` repository:

- MUST use the SysML model as the architecture source of truth.
- Inspect the relevant `.sysml` part usages, ports, behaviours, requirements,
  and connections before relying on program code or informal output.
- MUST follow the model-first rule: update the model before synchronising
  generated views or implementation.
- MUST NOT invent nesting from code alone; realign code and documentation with
  the model.

## Workflow

1. Name the target system and the question that is unclear.
2. Describe the target boundary and its direct child parts or usages.
3. Check ownership, interfaces, behaviour, and requirements at that layer.
4. Select the child system that contains the unresolved detail.
5. Recurse and repeat the same checks.
6. Report the clarified chain from parent to child, including remaining
   unknowns and the evidence for each boundary.

## Output shape

For a detail or review, structure the result as:

- **Target system** -- the boundary and the question being answered.
- **Current layer** -- purpose, owned children, interfaces, behaviour, and
  requirements.
- **Nested system dives** -- one subsection per child inspected and why it was
  necessary.
- **Resolution** -- clarified ownership and interactions.
- **Open points** -- explicit unknowns, missing model elements, or assumptions.

Pair this skill with the repository's SysML modelling workflow when the task
changes architecture, interfaces, behaviour, requirements, or allocation.
