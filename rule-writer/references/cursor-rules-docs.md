# Cursor Rules -- condensed reference

Source: https://cursor.com/docs/rules (fetch when details may have changed).

## Rule types

| Type | Storage | Scope |
|------|---------|-------|
| Project | `.cursor/rules/*.mdc` | Repo, version-controlled |
| User | Customize -> Rules | Global; Agent Chat only |
| Team | Dashboard (Team/Enterprise) | Org-wide; optional enforce + globs |
| AGENTS.md | Root / nested markdown | Simple alternative; nested combine |

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
| Settings User Rules | Customize -> Rules UI | Pack `~/.cursor/rules/*.mdc` |
| Pack user `.mdc` | `~/.cursor/rules/` (copies in pack `rules/`) | Settings User Rules blob |
| Project Rules | `<repo>/.cursor/rules/` | Either of the above |

Do not double-inject the same content via Settings User Rules and alwaysApply `.mdc`.

## Best practices (docs)

- <500 lines; split large rules
- Concrete examples / `@` file refs
- No full style guides, tool encyclopedias, or rare edge cases
- Prefer pointing at canonical code over copying it
