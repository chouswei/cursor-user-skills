# Skill review — output skeleton

Use this structure when reporting findings (fill in; omit empty sections).

## Summary

- **Skill:** `<folder-name>` (`SKILL.md` path)
- **Verdict:** Ready | Ready with fixes | Blocked
- **Score:** `<1–10>` / 10 (one line: what caps the score)

## Findings

### error

| Location | Issue | Fix |
|----------|-------|-----|

_(none, or rows)_

### warning

| Location | Issue | Fix |
|----------|-------|-----|

### info

| Location | Suggestion |
|----------|------------|

## Top 3 recommendations

1. …
2. …
3. …

## Registry / portability (if user may publish)

- Install path (monorepo subpath): …
- skill.fish / **skillfish** note: …
- Version: confirm `metadata.version` was bumped for this change before GitHub push (user pack consumers via skillfish).

## Files reviewed

- [ ] `SKILL.md`
- [ ] `references/*` (list)
- [ ] `assets/*` (list)
- [ ] `tools/*` (list)
- [ ] `Folder_Structure.md` (if present)
