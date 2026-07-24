# SysML v2 MCP — agent notes

- **validate** on `.sysml` changes; **preview** for diagram checks in Cursor.
- Pass **`code`** (file contents or merged snippet) to **validate** / **parse** / **getSymbols** when not using a fork’s workspace/URI mode; pass **`name`** to **getDefinition** / **getReferences** / **getHierarchy** (see [tool-parameters.md](tool-parameters.md)).
- Prefer **project-aware** paths from `sysml-v2-models/projects/<name>` when validating project files; use **`exam_model.py --project`** for full config load when MCP single-doc scope is not enough.
- **loadProject** / **impact** / **rename** / **query**: use when the task is cross-file or refactor-oriented (often a **fork** build; stock **daltskin** npm may not expose all of these — check MCP tools list in Cursor).
