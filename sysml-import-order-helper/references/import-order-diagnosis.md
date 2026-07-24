# Import / load order diagnosis

## 1. `config.yaml` `model_files` sanity

- **`root-<project>.sysml` must be last** in the list.
- **OMG Kernel + ISQ/SI** block should match a **known-good** project (see [sysml-root-config/references/load-order.md](../sysml-root-config/references/load-order.md)).
- **Typical relative order** (adjust names to your project):
  - Common **parts**: `flow_items` → `hardware_ports` → other `parts/` → **connections** (`connections.sysml`) → **composites** if referenced by deploy.
  - Project **`connections-*.sysml`** before **`deploy-*`** when deploy uses those `connection def`s.
  - **`requirements-*`** before **`deploy-*`** when deploy has **`satisfy`** / requirement usages.
  - **`deploy-*`** before **`behaviour-*`** when behaviour imports deploy package.
- Paths are relative to **`model_dir`** (usually `models`).

## 2. Unresolved type / “not defined” in one file

- The **defining package** must appear **earlier** in **`model_files`** than the file that uses the type, **or** the using file must **`private import`** a package that re-exports it (per SysML v2 scoping rules).
- **Common mistakes:** `SharedConnections` or **`Network`** before **`HardwarePorts`**; **deploy** before **requirements**; **behaviour** before **deploy**.

## 3. Circular dependency suspicion

- If two packages import each other, **break the cycle** by moving shared types upstream (e.g. into **common**), or by narrowing imports — not by random reorder.
- **sysmledgraph** can help list **who imports whom** after indexing.

## 4. When to switch to **sysml-root-config**

- Missing **`root-*.sysml`**, new project skeleton, or wholesale rewrite of **`model_files`** template → use **sysml-root-config** for scaffold + **new-project-index-updates**.
