---
name: mdtohtml
description: Convert Markdown to HTML with Mermaid diagrams, syntax highlighting, and dark theme using mdtohtml. Use when generating HTML from .md files, exporting system design reports, or rendering markdown with diagrams for web viewing.
metadata:
  pattern: tool-wrapper
  domain: publishing
  pairs_with:
    - system-design-report-generator
    - mermaid
    - project-output-article
---

# Markdown to HTML with mdtohtml

Convert Markdown files to styled HTML with integrated Mermaid diagram rendering, syntax highlighting, and dark theme using [Reperion/mdtohtml](https://github.com/Reperion/mdtohtml).

## When to Use

- **Single file export:** Convert one `.md` file to HTML
- **Merged report export:** Combine multiple `.md` sections into one HTML document
- **Batch conversion:** Export entire directories without separate setup

## Setup

### Install mdtohtml (one-time)

```bash
cd c:\Projects\SystemDesign
git clone https://github.com/Reperion/mdtohtml.git tools/mdtohtml
cd tools/mdtohtml
npm install
```

Or set environment variable if installed elsewhere:
```bash
set MDTOHTML_DIR=C:\path\to\mdtohtml
```

## Quick Start

### Convert single file

```bash
python tools/md_to_html.py <input.md> [output.html]
```

**Examples:**
```bash
# Auto-name output as input.html
python tools/md_to_html.py sysml-v2-models/projects/leo-cubesat-laser-comm/outputs/system-design-report/02-architecture.md

# Explicit output path
python tools/md_to_html.py 02-architecture.md ./output/02-architecture.html
```

### Merge sections and convert

For multi-file system design reports, use the Python merge script:

**1. Set up (one-time)**
```bash
# Copy merge_markdown.py to your tools directory
cp skills/mdtohtml/references/merge_markdown.py tools/merge_markdown.py
```

**2. Merge all sections**
```bash
cd system-design-report
python ../../tools/merge_markdown.py leo-laser-comm-PAT-system-design-merged.md \
  01-abstract.md 02-architecture.md 03-software.md ...
```

**Why Python over PowerShell?**
- **UTF-8 enforcement:** Python's explicit UTF-8 encoding preserves Unicode (–, →, ↔, etc.)
- **No corruption:** PowerShell's mixed encoding causes Unicode replacement issues
- **Simpler:** Python: Read UTF-8 → Merge → Write UTF-8. Done.
- **Cross-platform:** Works identically on Windows, macOS, Linux

**Full example** (leo-cubesat-laser-comm):
```bash
cd sysml-v2-models/projects/leo-cubesat-laser-comm/outputs/system-design-report
python ../../../tools/merge_markdown.py leo-laser-comm-PAT-system-design-merged.md \
  01-abstract-introduction.md 02-architecture.md 02b-interconnection.md \
  02b1-mcu-pinmap.md 02b2-inter-hat-bridges.md 02b3-software-allocation.md \
  02b4-connector-inventory.md 03-software-allocation.md 04-state-machine.md \
  05-tracking.md 06-calibration.md 07-storage.md 08-faults.md \
  09-device-thread-states.md 10-optics.md 11-power.md 12-references.md
```

**3. Convert merged markdown to HTML**
```bash
cd c:\Projects\SystemDesign
python tools/md_to_html.py sysml-v2-models/projects/leo-cubesat-laser-comm/outputs/system-design-report/leo-laser-comm-PAT-system-design-merged.md
```

### Batch convert multiple files

```bash
python tools/md_to_html.py --batch "sysml-v2-models/projects/*/outputs/*.md"
```

Creates `.html` file in same directory as each `.md`.

## Features

- ✅ **Mermaid diagrams** render inline (no separate rendering step needed)
- ✅ **Syntax highlighting** for code blocks
- ✅ **Dark theme** by default
- ✅ **Responsive** layout for mobile/desktop
- ✅ **UTF-8 aware** (preserves special characters: →, –, ·, §)
- ✅ **Table of contents** auto-generated (for large files)
- ✅ **No external dependencies** for rendering (everything included in HTML)

## Output Format

- **Input:** `merged.md` or individual `02-architecture.md`
- **Output:** `merged.html` or `02-architecture.html` (same directory)
- **Location:** Matches input directory (relative paths respected)

## Workflow for System Design Reports

### Single-file export (full report)
```bash
# Merge all sections into one .md
# (use PowerShell script above or write a shell script)

# Convert to HTML
python tools/md_to_html.py leo-laser-comm-PAT-system-design-merged.md
```

### Per-section export
```bash
# Export each section individually
python tools/md_to_html.py 02-architecture.md
python tools/md_to_html.py 02b-interconnection.md
python tools/md_to_html.py 03-software-allocation.md
```

### Batch export
```bash
# Convert entire report directory
python tools/md_to_html.py --batch "sysml-v2-models/projects/leo-cubesat-laser-comm/outputs/system-design-report/*.md"
```

## Validation Checklist

After conversion, verify the HTML:

- [ ] **Mermaid diagrams render** (check Figure 1, Figure 2, flowcharts)
- [ ] **Special characters display correctly** (→, –, ·, §, not as `â†'`, `â€"`, etc.)
- [ ] **Code blocks have syntax highlighting** (not just plain monospace)
- [ ] **Links work** (relative `[text](file.md)` becomes `[text](file.html)`)
- [ ] **Dark theme applied** (dark background, light text)
- [ ] **Table of contents** present (for large files)
- [ ] **Page loads quickly** (CSS/JS inlined, no external requests needed)

## Troubleshooting

### mdtohtml not found
```
Error: mdtohtml not found at tools/mdtohtml
```
**Fix:** Clone and install (see Setup section above)

### Files not converted in batch
- Check glob pattern is quoted properly
- Verify `.md` files exist in the directory
- Non-markdown files are silently skipped (expected)

### HTML looks plain (no styling)
- Ensure mdtohtml npm dependencies installed (`npm install` in tools/mdtohtml/)
- Check browser console for any JavaScript errors
- Open the HTML file in a modern browser (Chrome, Firefox, Edge)

### Special characters show as `â†'` or `Â·`
- **Solution:** This is a Pandoc encoding issue, not mdtohtml
- mdtohtml handles UTF-8 correctly by default
- If using Pandoc instead, ensure: `pandoc -f utf-8 -t html5 input.md -o output.html`

### Mermaid parse errors in diagrams

- **Common cause:** Reserved Mermaid keywords in diagram labels
- **Example error:** `Lexical error on line 18. Unrecognized text. ...`
- **Fix:** Use ASCII-safe labels in Mermaid edge annotations or escape special syntax
- **Prevention:** Use the Python merge script which preserves all Unicode correctly

## Script Reference

**File:** `tools/md_to_html.py`

```bash
# Usage
python tools/md_to_html.py <input.md> [output.html]
python tools/md_to_html.py --batch "pattern/*.md"

# Help
python tools/md_to_html.py --help
```

**Parameters:**
- `<input.md>` — Markdown file to convert (relative or absolute path)
- `[output.html]` — Optional output path (defaults to `input.html`)
- `--batch "pattern"` — Glob pattern for batch conversion (all .md files matching)

**Returns:**
- Success: prints "Successfully converted to ..."
- Error: prints error to stderr, exits with code 1 or 2

## Best Practices

1. **Use Python for merging** — `tools/merge_markdown.py` eliminates encoding corruption (see `references/merge_markdown.py`)
2. **Merge before exporting** — For system design reports, merge sections into one `.md`, then convert
3. **Validate Mermaid before export** — Run `mmdc` on merged `.md` to catch parse errors before HTML conversion: `mmdc -i leo-laser-comm-PAT-system-design-merged.md`
4. **Don't store HTML in git** — HTML is derived; keep only `.md` files in git
5. **Validate before sharing** — Check diagrams render and special characters display correctly
6. **Archive exports** — Save HTML snapshots when publishing stable versions
7. **One merged file per report** — Use one `leo-laser-comm-PAT-system-design-merged.md` → `leo-laser-comm-PAT-system-design-merged.html`
8. **UTF-8 everywhere** — Python's explicit UTF-8 handling is the key to preserving Unicode through the pipeline
