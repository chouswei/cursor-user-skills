---
name: rule-writer
description: >-
  Author Cursor rules correctly: Project Rules (.mdc frontmatter), User Rules
  (draft for user paste only), Team Rules, and AGENTS.md; apply modes, globs,
  precedence, dual-store pitfalls. Use when creating or editing .cursor/rules,
  User Rules, Team Rules, AGENTS.md, alwaysApply/globs frontmatter, /create-rule,
  or Import Remote Rule. Triggers: rule writer, cursor rules, create rule,
  .mdc rule, alwaysApply, project rules, user rules, team rules, AGENTS.md,
  remote rule import.
metadata:
  pattern: generator
  domain: meta
  version: "1.1"
---

# Rule writer

Teach agents to author Cursor rules from [Cursor Rules docs](https://cursor.com/docs/rules). Condensed tables: [references/cursor-rules-docs.md](references/cursor-rules-docs.md). Prose quality: [prompt-writing-discipline](../prompt-writing-discipline/SKILL.md).

Built-in `create-rule` (skills-cursor) is a thin scaffold; this skill is the accurate docs + store workflow.

## When invoked

1. **Clarify store** (ask if unclear): Project | User (Settings paste) | Pack `.mdc` | Team (dashboard) | AGENTS.md.
2. **Review existing** rules in the target location; extend or split instead of duplicating.
3. **Draft thin, actionable** content (prefer **<120 lines** for alwaysApply; docs allow <500).
4. **Set frontmatter** for Project / pack `.mdc` only (tables below).
5. **Write only to agent-writable stores**; for User Rules, draft text for the user to paste (see below).

## Four rule types

| Type | Where | Agent may write? | Notes |
|------|-------|------------------|-------|
| **Project Rules** | Workspace `.cursor/rules/*.mdc` | **Yes** | Version-controlled; frontmatter controls apply |
| **User Rules** | Customize -> Rules -> User Rules | **No** (paste only) | Global freeform; **Agent Chat only** -- not Ctrl/Cmd+K |
| **Team Rules** | Cursor dashboard | **No** (admins UI) | Team/Enterprise; freeform (+ optional globs); can be enforced |
| **AGENTS.md** | Project root and/or nested dirs | **Yes** | Plain markdown; no frontmatter; nested combine, more specific wins |

## Stores (MUST clarify)

These are **not** the same thing:

| Store | Path / UI | What it is | Agent action |
|-------|-----------|------------|--------------|
| Settings **User Rules** | Customize -> Rules -> User Rules | One global freeform blob (IDE-only / online Settings) | Draft markdown; **user copy/pastes** into the field and saves |
| Pack `~/.cursor/rules/*.mdc` | `~/.cursor/rules/` (source also in pack `rules/`) | Optional pack convention -- **not** the Settings UI | Edit pack / compose paste buffer; **do not** silent-write Settings |
| **Project Rules** | `<workspace>/.cursor/rules/*.mdc` | Repo-scoped | Agent edits `.mdc` files directly |

**MUSTNOT** put the same normative text in Settings User Rules **and** an `alwaysApply: true` pack/project `.mdc` if both load -- double injection.

## User Rules workflow (MUST / MUST NOT)

Aligned with docs: [User Rules](https://cursor.com/docs/rules) = global preferences in **Customize -> Rules**.

### MUST NOT

- Do **not** write `aicontext.personalContext`, patch `state.vscdb`, or use AppData / SQLite / other storage hacks to "set User Rules".
- Do **not** claim Settings were updated, or that the agent applied User Rules programmatically.
- Do **not** treat pack `~/.cursor/rules/*.mdc` as equivalent to Settings User Rules.

### MUST

When the user asks to create or revise **User Rules**:

1. Produce a **clean markdown block** (the full intended User Rules text).
2. Tell the user to open **Customize -> Rules -> User Rules**, **replace** the field with that text, and **save**.
3. Optionally write the same text to a helper file such as `user-rules-settings-composed.txt` (workspace or pack) **only as a copy/paste aid** -- never as "Settings updated".

### Closing instruction (example)

After drafting, end with something like:

> Copy the block below into **Customize -> Rules -> User Rules**, replace the whole field, then save.
>
> ```markdown
> ...drafted User Rules...
> ```

## Project rule mechanics

- Extension **must** be `.mdc`. Plain `.md` under `.cursor/rules` is **ignored** (no frontmatter). Prefer AGENTS.md for plain markdown.
- Frontmatter fields: `description`, `globs`, `alwaysApply`.
- Folders under `.cursor/rules/` are fine (e.g. `frontend/components.mdc`).

### Apply modes (UI type -> behaviour)

| Rule type (UI) | Effect |
|----------------|--------|
| Always Apply | Every chat session |
| Apply Intelligently | Agent pulls in when `description` matches relevance |
| Apply to Specific Files | Auto-attach when a matching file is in context |
| Apply Manually | Only when `@`-mentioned (e.g. `@my-rule`) |

### Frontmatter interaction

| `alwaysApply` | `description` | `globs` | Behaviour |
|---------------|---------------|---------|-----------|
| `true` | -- | -- | Always included; globs and description ignored |
| `false` | -- | provided | Auto-attached when a matching file is in context |
| `false` | provided | omitted | Agent uses description; includes when relevant |
| `false` | omitted | omitted | Manual `@`-mention only |

### Minimal templates

Always apply:

```markdown
---
alwaysApply: true
---

- Concrete MUST / MUSTNOT lines only
```

Globs:

```markdown
---
globs: src/**/*.tsx
alwaysApply: false
---

- File-scoped conventions
```

Intelligent:

```markdown
---
description: When this topic applies (be specific)
alwaysApply: false
---

- Topic-scoped guidance
```

Manual:

```markdown
---
alwaysApply: false
---

- Checklist used only via @-mention
```

Multiple globs: comma-separated (`docs/**/*.md, docs/**/*.mdx`). See reference for pattern examples.

## Creating rules

- **Project:** Chat `/create-rule` or Customize -> Rules -> Add Rule (writes under `.cursor/rules`). Agent may edit those `.mdc` files.
- **User Rules:** Agent drafts only; user pastes into Customize -> Rules -> User Rules (see workflow above).
- **Remote:** Customize -> Rules -> Add Rule -> **Remote Rule (Github)** -> URL; lands under `.cursor/rules/imported/...` (relative paths preserved).
- **Team:** dashboard only (admins); not a local `.mdc` file.

## Precedence

When guidance conflicts: **Team Rules -> Project Rules -> User Rules**. All applicable rules still merge; earlier source wins on conflict.

## Best practices

- Under **500** lines per rule (prefer **<120** for alwaysApply / thin-mdc).
- Split large topics into composable rules.
- Concrete examples or `@file` references; do not paste whole files that go stale.
- Avoid style-guide dumps, exhaustive CLI lists, and rare edge cases -- use linters / point at canonical code.
- Add rules when Agent repeats a mistake; check into git for Project Rules.

## AGENTS.md

- Root and nested `AGENTS.md` supported; nested apply for that directory tree; more specific overrides broader.
- Use when instructions are simple and frontmatter/apply modes are unnecessary.

## FAQ (docs)

- Intelligent mode needs a real `description`; glob mode needs patterns that match files in context.
- Rules do **not** affect Cursor Tab or other non-Agent features.
- User Rules do **not** apply to Inline Edit (Ctrl/Cmd+K).

## Checklist before finish

- [ ] Store chosen (project / settings user paste / pack `.mdc` / team / AGENTS.md)
- [ ] No duplicate of an existing rule
- [ ] Correct frontmatter for apply mode (or none for AGENTS.md / Settings User Rules)
- [ ] Thin, actionable; ASCII paths; British English unless host file differs
- [ ] Dual-store: not copying Settings User Rules into alwaysApply `.mdc`
- [ ] User Rules: draft + copy/paste instruction only; no `state.vscdb` / `aicontext` / AppData writes
- [ ] Helper compose file (if any) labelled as copy/paste aid, not Settings sync
