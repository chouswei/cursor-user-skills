# Cursor Rules -- condensed reference

Source: https://cursor.com/docs/rules (fetch when details may have changed).

## Rule types

| Type | Storage | Scope | Agent writable? |
|------|---------|-------|-----------------|
| Project | `.cursor/rules/*.mdc` | Repo, version-controlled | Yes |
| User | Customize -> Rules -> User Rules | Global; Agent Chat only | **No** -- draft for user paste |
| Team | Dashboard (Team/Enterprise) | Org-wide; optional enforce + globs | No (dashboard) |
| AGENTS.md | Root / nested markdown | Simple alternative; nested combine | Yes |

## User Rules (docs)

- Global preferences in **Customize -> Rules** (freeform text).
- Used by Agent (Chat); not Inline Edit (Cmd/Ctrl+K).
- **Not** a reliable filesystem target. Agents **MUST NOT** write `aicontext.personalContext`, `state.vscdb`, or AppData hacks to set them.
- **MUST** output a clean markdown block; user replaces the User Rules field and saves.
- Optional helper file (e.g. `user-rules-settings-composed.txt`) = copy/paste aid only -- not "Settings updated".

## Project: extension and frontmatter

- **Must** use `.mdc`. Plain `.md` in `.cursor/rules` is ignored.
- Fields: `description`, `globs`, `alwaysApply`.

## Apply modes

| UI type | When included |
|---------|----------------|
| Always Apply | Every session |
| Apply Intelligently | Agent judges from `description` |
| Apply to Specific Files | Matching file in context |
| Apply Manually | `@`-mention only |

## alwaysApply x description x globs

| alwaysApply | description | globs | Behaviour |
|-------------|-------------|-------|-----------|
| true | -- | -- | Always; other fields ignored |
| false | -- | set | Auto-attach on glob match |
| false | set | omitted | Intelligent attach |
| false | omitted | omitted | Manual `@` only |

## Glob examples

| Pattern | Matches |
|---------|---------|
| `*` | One path segment |
| `**` | Any depth of directories |
| `*.ts` | `.ts` in root |
| `**/*.ts` | `.ts` anywhere |
| `src/**` | Everything under `src/` |
| `src/**/*.tsx` | `.tsx` under `src/` |
| `docs/**/*.md, docs/**/*.mdx` | Comma-separated multi-pattern |
| `tailwind.config.*` | Any extension |

## Precedence

**Team -> Project -> User** on conflict (all applicable still merged).

## Import Remote Rule (GitHub)

Customize -> Rules -> Add Rule -> Remote Rule (Github) -> repo URL.

Result: `.cursor/rules/imported/<...>/` (relative paths kept).

## Dual-store (pack convention)

| Name | Location | Not to confuse with |
|------|----------|---------------------|
| Settings User Rules | Customize -> Rules UI (user pastes) | Pack `~/.cursor/rules/*.mdc` |
| Pack user `.mdc` | `~/.cursor/rules/` (copies in pack `rules/`) | Settings User Rules blob |
| Project Rules | `<repo>/.cursor/rules/` | Either of the above |

Do not double-inject the same content via Settings User Rules and alwaysApply `.mdc`.

Pack `.mdc` edits: sync to a paste buffer / composed helper for User Rules if the user wants that text in Settings -- **never** silent DB write.

## Best practices (docs)

- <500 lines; split large rules
- Concrete examples / `@` file refs
- No full style guides, tool encyclopedias, or rare edge cases
- Prefer pointing at canonical code over copying it
