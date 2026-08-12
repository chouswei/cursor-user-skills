---
name: antlr4-grammar
description: >-
  Author, validate, and work with ANTLR4 grammars (.g4): lexer/parser rules,
  visitor/listener patterns, common pitfalls, and toolchain (antlr4 tool,
  antlr4-python3-runtime, JavaScript, Java targets). Keeps grammars LLM-friendly.
  Triggers: ANTLR, ANTLR4, .g4, lexer rule, parser rule, grammar file, visitor,
  listener, TokenStream, ParseTree, antlr4-python3-runtime, generate parser,
  left recursion, keyword vs identifier. Not for: hand-rolled recursive-descent
  without .g4, or MemNet dialect authoring alone (use memnet-format).
metadata:
  pattern: pipeline
  domain: languages
  version: "1.2"
  notes: Generic ANTLR4; MemNet GQL wire is not authored via .g4 -- use memnet-format.
---

# ANTLR4 grammar

Author and validate **ANTLR4** `.g4` grammars. Generic -- not MemNet-only. Optional application: parsing a line-oriented product dialect is fine; do **not** invent project-specific `.g4` unless the user asks or a trivial illustration is enough.

British English in new prose for this pack.

## When to open

| Signal | Action |
|--------|--------|
| New or edit `.g4`, lexer/parser rules, visitor/listener | This skill |
| Generate / install runtime (Python, JS, Java) | This skill + [references/toolchain.md](references/toolchain.md) |
| Precedence, keywords vs ids, left-recursion fixes | [references/recipes.md](references/recipes.md) |
| Ambiguity, mutual left recursion, token traps | [references/pitfalls.md](references/pitfalls.md) |
| MemNet agent wire (GQL / shaped pin_map) | [memnet-format](../memnet-format/SKILL.md) -- not an ANTLR task |

## Pipeline

Copy and track:

```text
Task progress:
- [ ] 1. Clarify language / target / combined vs split grammar
- [ ] 2. Sketch tokens then rules (or load references/grammar-structure.md)
- [ ] 3. Write .g4 (ASCII path; kebab or PascalCase file names per project)
- [ ] 4. Generate and compile / import for the chosen target
- [ ] 5. Smoke-parse sample inputs; fix; re-generate
- [ ] 6. Wire visitor or listener only if the user needs a tree walk
```

### 1. Clarify

- **Input language** and sample strings (happy path + 2-3 edge cases).
- **Target**: Python3 (default for this pack), JavaScript, or Java.
- **Combined** grammar (`grammar X;`) vs **split** (`lexer grammar` / `parser grammar` + `tokenVocab`).
- Prefer **one combined grammar** until lexer reuse across parsers is required.

### 2. Structure (load on need)

Essential shape -- detail in [references/grammar-structure.md](references/grammar-structure.md):

```antlr
grammar Expr;                 // or lexer grammar / parser grammar

@header { /* target-specific imports if needed */ }

// Parser rules: lowercase start
prog  : expr EOF ;
expr  : expr ('*'|'/') expr
      | expr ('+'|'-') expr
      | INT
      | '(' expr ')'
      ;

// Lexer rules: UPPERCASE start
INT   : [0-9]+ ;
WS    : [ \t\r\n]+ -> skip ;
```

### 3. Author rules

- Lexer first for punctuation and literals; then parser.
- Prefer **explicit left-recursive** expression layers (ANTLR4 supports direct left recursion) over tangled precedence hacks -- see [references/recipes.md](references/recipes.md).
- Keywords: dedicated lexer tokens **before** a catch-all `ID` rule.
- Keep rule names stable and descriptive (`statement`, not `s`); LLMs and visitors share those names.

### 4. Generate and validate

Default **Python3** (load [references/toolchain.md](references/toolchain.md) for JS/Java):

```bash
# Install tool once (pip or the antlr4-tools wrapper)
pip install antlr4-tools antlr4-python3-runtime

# Generate (from the directory that contains the .g4)
antlr4 -Dlanguage=Python3 -visitor -no-listener MyGrammar.g4

# Smoke: import generated *Lexer/*Parser and parse a string; EOF must match
```

**MUST** re-run generation after every `.g4` change before testing callers.

### 5. Walk the tree

| Style | When |
|-------|------|
| **Visitor** (`-visitor`) | Explicit control; return values; preferred for interpreters |
| **Listener** (default) | Event-driven enter/exit; fine for side effects, weaker for returns |

Subclass `MyGrammarVisitor` (or listener) in the target language; do not edit generated `*Parser.py` / `*.js` by hand.

### 6. LLM-friendly grammar habits

- Small rules, one concern each; comments for non-obvious intent.
- Sample inputs in a sibling `examples/` or doc comment -- agents re-use them as tests.
- Avoid cryptic one-letter rules and deep optional nests that hide ambiguity.
- Prefer labelled alternatives (`# Add` / `# Mul`) when visitors need distinct methods.
- See [references/pitfalls.md](references/pitfalls.md).

## Quick recipes (pointers)

| Need | Where |
|------|--------|
| Operator precedence / associativity | [references/recipes.md](references/recipes.md) § Precedence |
| Keywords vs identifiers | [references/recipes.md](references/recipes.md) § Keywords |
| Separated lists (`a, b, c`) | [references/recipes.md](references/recipes.md) § Lists |
| Channel / hidden tokens | [references/recipes.md](references/recipes.md) § Channels |

## Non-goals

- Inventing MemNet-only `.g4` without a user request.
- Replacing a project's existing parser generator without agreement.
- Pasting full ANTLR book chapters into chat -- load `references/` instead.

## Additional resources

- [references/grammar-structure.md](references/grammar-structure.md) -- file layout, naming, modes
- [references/recipes.md](references/recipes.md) -- precedence, keywords, lists, channels
- [references/toolchain.md](references/toolchain.md) -- generate/validate per target
- [references/pitfalls.md](references/pitfalls.md) -- common failures and LLM tips
- Upstream: [ANTLR4 documentation](https://github.com/antlr/antlr4/blob/master/doc/index.md)
