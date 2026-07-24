---
name: file-operations
description: >-
  Teach efficient file move/copy/batch operations; avoid Read→Write→Delete antipattern.
  Triggers: batch file operations, organizing outputs, preserving file content exactly,
  file cleanup, avoiding regeneration waste.
metadata:
  pattern: pipeline
  severity-levels: info
  version: 1.0
  domain: workflow
---

# File Operations Skill — Copy / Move / Batch Operations

**Efficiency focus:** Minimize read cycles, use native shell commands, batch operations.

---

## When to Use This Skill

**Triggers:**
- ✅ Moving/copying files between directories
- ✅ Batch file operations (multiple files)
- ✅ Organizing generated output (models → outputs)
- ✅ File cleanup or deduplication
- ✅ Need to preserve file content exactly (no regeneration)

**Anti-patterns to avoid:**
- ❌ Read → Write → Delete (use Move instead)
- ❌ Individual tool calls per file (batch commands)
- ❌ Shell pipes that lose metadata (timestamps, permissions)

---

## Output Contract

**This skill is advisory and reference-based.** Agents read this skill to:
1. Diagnose operation type (Move vs Copy vs Regenerate)
2. Choose the appropriate command from the reference tables
3. Call `Shell` tool with the selected PowerShell command

Example agent flow:
- **Input:** User asks "move these 4 docs from models/ to outputs/"
- **Agent reads:** Decision tree + "Real-World Example" section
- **Agent decides:** Move operation (content unchanged)
- **Agent executes:** Calls `Shell` with 4 parallel `Move-Item` commands
- **Result:** Files moved efficiently in 4 I/O operations

---

## Decision Tree

```
Do you need to move/copy files?
├─ YES: Continue below
└─ NO: Skip this skill

Is file content UNCHANGED?
├─ YES: Use MOVE (faster, preserves metadata)
├─ NO: Use COPY if original needed, else REGENERATE
└─ BOTH: Use COPY (preserves original)

Single file or batch?
├─ Single: Direct Shell command
├─ Batch (2-10): Shell loop or parallel calls
└─ Batch (10+): Script file or Task shell subagent
```

---

## Operations Reference

### MOVE (Preferred — Fastest)

**Use when:** File content is final, no need for original location

```powershell
# Single file
Move-Item "source/file.md" "dest/"

# Batch (parallel Shell calls)
Move-Item "source/CUBEMX-PIN-VERIFICATION-v7.md" "outputs/"
Move-Item "source/SIGNALS-86ewy6qck-README.md" "outputs/"
Move-Item "source/POLARFIRE-HAT-CONNECTORS.md" "outputs/"
```

**Advantages:**
- ✅ Fast (no read/write cycle)
- ✅ Preserves timestamps, metadata
- ✅ Single atomic operation per file
- ✅ No disk space bloat

**Shell example (PowerShell):**
```powershell
Move-Item -Path "models/*.md" -Destination "outputs/" -Force
```

---

### COPY (When Original Needed)

**Use when:** Keep original in source, duplicate to destination

```powershell
Copy-Item -Path "source/file.md" -Destination "outputs/file.md"
Copy-Item -Path "source/" -Destination "outputs/" -Recurse
```

**Advantages:**
- ✅ Preserves source
- ✅ Parallel-safe (no conflicts)

**Disadvantages:**
- ❌ Doubles disk space
- ❌ Slower than move

---

### REGENERATE (When Content Changes)

**Use when:** Content needs editing before moving

**❌ BAD (inefficient):**
```
1. Read file
2. Write to new location  ← Regenerated copy
3. Delete original        ← Wasted cycles
```

**✅ GOOD (efficient):**
```
1. Read file
2. Edit in place (StrReplace)
3. Move to outputs         ← Single operation
```

---

## Batch Operation Template

### Multiple Files, Sequential Moves

```powershell
# Move 4 documentation files from models/ to outputs/
Move-Item "models/CUBEMX-PIN-VERIFICATION-v7.md" "outputs/"
Move-Item "models/SIGNALS-86ewy6qck-README.md" "outputs/"
Move-Item "models/POLARFIRE-HAT-CONNECTORS.md" "outputs/"
Move-Item "models/INTER-HAT-INTERCONNECTION-MAP.md" "outputs/"
```

**Execution:**
- Use multiple Shell calls in parallel (same message)
- Each command is independent (safe to parallelize)
- No dependencies between operations

### Batch Copy with Glob

```powershell
# Copy all markdown files from src/ to dest/
Copy-Item -Path "src/*.md" -Destination "dest/" -Recurse
```

### Batch Move with Loop (if needed)

```powershell
# Move all .md files from models/ to outputs/
Get-ChildItem "models/*.md" | ForEach-Object {
  Move-Item $_.FullName "outputs/"
}
```

---

## Gotchas & Edge Cases

### ⚠️ Path Spaces
Always quote paths with spaces:
```powershell
# ✅ CORRECT
Move-Item "C:\My Documents\file.md" "outputs/"

# ❌ WRONG
Move-Item C:\My Documents\file.md outputs/
```

### ⚠️ Overwrite Behavior
By default, Move-Item fails if destination exists:
```powershell
# Overwrite without prompting
Move-Item -Path "source/file.md" -Destination "outputs/" -Force
```

### ⚠️ Directory vs File
Moving a directory moves it WITH contents:
```powershell
Move-Item "models/" "outputs/"  # Moves entire directory
Move-Item "models/*" "outputs/" # Moves files inside only
```

### ⚠️ Cross-Drive Moves
On Windows, moving across drives may copy instead:
```powershell
# May copy instead of move if drives differ
Move-Item "D:\file.md" "C:\outputs\file.md"
```

---

## Agent Checklist

Before moving/copying files:

- [ ] **Identify operation type:** Move vs Copy vs Regenerate?
- [ ] **Batch or single?** 1 file = Shell; 2–10 = parallel Shell; 10+ = script/subagent
- [ ] **Paths quoted?** Any spaces? Quote with `""`
- [ ] **Destination exists?** Create if needed: `mkdir outputs` first
- [ ] **Preserve metadata?** Use Move, not Read→Write→Delete
- [ ] **Verify afterward:** List destination with `ls` to confirm

---

## Real-World Example

**WRONG (inefficient, what I did):**
```
Read CUBEMX-PIN-VERIFICATION-v7.md
Write to outputs/
Delete from models/
Read SIGNALS-86ewy6qck-README.md
Write to outputs/
Delete from models/
[... repeat 2 more times ...]
Total: 8 I/O operations
```

**RIGHT (efficient):**
```
Move-Item models/CUBEMX-PIN-VERIFICATION-v7.md outputs/
Move-Item models/SIGNALS-86ewy6qck-README.md outputs/
Move-Item models/POLARFIRE-HAT-CONNECTORS.md outputs/
Move-Item models/INTER-HAT-INTERCONNECTION-MAP.md outputs/
Total: 4 I/O operations (2x faster)
```

---

## When to Escalate to Task/Shell Subagent

Use **Task shell subagent** for:
- 20+ files
- Complex glob patterns
- Conditional moves (move if X exists, etc.)
- Parallel file operations on large trees

```powershell
# Example: 50 markdown files from 10 subdirectories
Get-ChildItem -Path "models" -Filter "*.md" -Recurse | 
  ForEach-Object {
    Move-Item $_.FullName "outputs/" -Force
  }
```

---

## Platform Notes

**Windows (PowerShell):** Commands above use `Move-Item` / `Copy-Item` (native PowerShell).

**Unix / macOS (Bash/Zsh):** Replace PowerShell commands with:
- `Move-Item src dest` → `mv src dest`
- `Copy-Item src dest` → `cp src dest` or `cp -r` for recursive
- `Get-ChildItem *.md | ForEach-Object` → `for file in *.md; do`

Decision tree and logic remain identical; only CLI commands differ.

---

## Summary

| Operation | When | Command | Speed |
|-----------|------|---------|-------|
| **Move** | Content final, no original needed | `Move-Item src dest` | ⚡⚡⚡ Fastest |
| **Copy** | Keep original | `Copy-Item src dest` | ⚡⚡ Good |
| **Regenerate** | Content needs editing | Read → Edit → Move | ⚡ Slowest |

**Rule of thumb:** Move > Copy > Read→Write→Delete. **Never** do the latter.
