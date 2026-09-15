# SysML v2 MCP — agent notes

- **validate** on `.sysml` changes; **preview** for diagram checks in Cursor.
- Pass **`code`** (file contents or merged snippet) to **validate** / **parse** / **getSymbols** when not using a workspace/URI mode; pass **`name`** to **getDefinition** / **getReferences** / **getHierarchy** (see [tool-parameters.md](tool-parameters.md)).
- In `modelbasedPrj-*` system repos, SysML model SSOT lives under `sysml-models/`. Pass file contents via `code` or file paths to MCP tools.
- Stock **daltskin** npm exposes `validate`, `parse`, `getDiagnostics`, `getSymbols`, `getDefinition`, `getReferences`, `getHierarchy`, `getModelSummary`, `preview`, `getComplexity` (Cursor namespace `user-sysml-v2`).
