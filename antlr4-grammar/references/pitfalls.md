# ANTLR4 pitfalls and LLM-friendly tips

**Retrieval seeds:** mutual left recursion, implicit token, token conflict, unterminated string, ambiguous grammar, LLM grammar style

## Common pitfalls

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Token never matches / wrong token | Keyword or literal **after** `ID` | Put specific lexer rules above general ones |
| `implicit definition of token` warnings | String literal only in parser | Add explicit `SEMI : ';' ;` (etc.) |
| Mutual left recursion error | `a : b ... ; b : a ...` | Break cycle with a clear hierarchy or intermediate rule |
| Parse succeeds but tree useless | Missing `EOF` on start rule | Append `EOF` to whole-input entry rule |
| Empty match loops | `rule : rule? other` style mistakes | Re-read optionals; add tests for empty input |
| Greedy string eats rest of file | `.*` / unterminated patterns | Use negation sets `~[...]` and clear terminators |
| Listener hard to return values | Using listener for expression eval | Switch to **visitor** |
| Edited `*Parser.py` lost | Hand-edit of generated code | Put logic in visitor/subclass only |
| Runtime / tool mismatch | Mixed ANTLR versions | Align tool + runtime; regenerate |

## Ambiguity

ANTLR4 parsers are adaptive LL(*). Remaining ambiguities often show as wrong alternative chosen, not always a hard error. Add:

- Clearer rule boundaries
- Labelled alternatives
- Sample-driven tests for each alt
- Predicates only as last resort ([recipes.md](recipes.md))

## LLM-friendly authoring

**Do:**

- Stable, pronounceable rule names shared by docs, tests, and visitors
- Labelled alts for semantically different shapes
- Short comments on non-obvious lexer ordering
- Fixture snippets next to the grammar (`examples/ok_*.txt`, `examples/bad_*.txt`)
- One grammar concern per file until split is justified

**Avoid:**

- One-letter rules (`e`, `s`, `t`) except in throwaway sketches
- Deep nested optionals that encode a whole language in one rule
- Copy-pasting large unrelated grammars "for reference" into the project
- Inventing domain `.g4` (e.g. MemNet) without the published dialect rules
- Unicode punctuation in rule names or paths (ASCII filenames)

## Debug checklist

1. Dump tokens: walk the lexer on the failing input; confirm token sequence.
2. Confirm start rule and `EOF`.
3. Bisect: comment out recent rules; re-generate; retest.
4. Compare expected tree (labelled alts) vs visitor methods actually invoked.

## Testing habit

Every grammar change ships with at least:

- One **accept** fixture
- One **reject** fixture (illegal token or structure)
- Regenerated sources matching the project's target language
