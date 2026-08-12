# ANTLR4 grammar structure

**Retrieval seeds:** antlr4 grammar, lexer rule, parser rule, combined grammar, tokenVocab, fragment, mode, channel, labelled alternative

## File kinds

| Kind | Header | Use |
|------|--------|-----|
| Combined | `grammar Name;` | Default: lexer + parser in one `.g4` |
| Lexer only | `lexer grammar Name;` | Shared tokens; modes; reuse |
| Parser only | `parser grammar Name;` | Needs `options { tokenVocab=Name; }` |

File name should match the grammar name (`Expr.g4` → `grammar Expr;`).

## Naming

| Element | Convention | Example |
|---------|------------|---------|
| Parser rule | lowercase start | `expr`, `statement` |
| Lexer rule | UPPERCASE | `INT`, `ID`, `SEMI` |
| Fragment | UPPERCASE, not a token alone | `fragment DIGIT : [0-9] ;` |
| Alternative label | `# Name` after alt | `expr : ... # Add` |

Generated visitor methods follow these names (`visitExpr`, `visitAdd`).

## Typical sections (combined)

1. `grammar` header and optional `options` / `@header` / `@members`
2. Parser entry rule ending in `EOF` for whole-input parses
3. Other parser rules
4. Lexer rules (keywords and punctuation **before** general `ID` / `STRING`)
5. `WS` / comments → `skip` or `-> channel(HIDDEN)`

## Lexer essentials

```antlr
fragment DIGIT : [0-9] ;
INT   : DIGIT+ ;
ID    : [a-zA-Z_] [a-zA-Z0-9_]* ;
STRING: '"' (~["\r\n])* '"' ;
LINE_COMMENT : '//' ~[\r\n]* -> skip ;
WS    : [ \t\r\n]+ -> skip ;
```

- **Fragments** compose tokens; they do not appear in the token stream.
- **Modes** (`mode INSIDE;`) for nested contexts (e.g. string interpolation) -- keep rare; document the push/pop.
- Literal `'if'` in a parser rule creates an implicit token; prefer an explicit `IF : 'if' ;` when visitors care.

## Parser essentials

```antlr
prog : statement+ EOF ;

statement
    : assignment SEMI
    | expr SEMI
    ;

assignment : ID EQ expr ;
```

- One **start rule** used by the application (`parser.prog()`).
- Use `EOF` on whole-file / whole-line entry rules so trailing junk fails loudly.
- Prefer left-recursion for binary operators (ANTLR4 rewrites direct left recursion).

## Labelled alternatives

```antlr
expr
    : expr op=('*'|'/') expr   # MulDiv
    | expr op=('+'|'-') expr   # AddSub
    | INT                      # Int
    | ID                       # Id
    | '(' expr ')'             # Parens
    ;
```

Gives distinct `visitMulDiv` / `visitAddSub` methods -- clearer for agents than one giant `visitExpr`.

## Split grammar sketch

```antlr
// ExprLexer.g4
lexer grammar ExprLexer;
INT : [0-9]+ ;
// ...

// ExprParser.g4
parser grammar ExprParser;
options { tokenVocab=ExprLexer; }
prog : expr EOF ;
expr : ... ;
```

Generate lexer then parser; keep `tokenVocab` in sync after token renames.

## Error strategy (application side)

Default Bail/DefaultErrorStrategy is enough for smoke tests. For IDE-like recovery, customise in host code -- not in the `.g4` unless using `catch` / local recovery rules deliberately.
