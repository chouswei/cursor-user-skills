# ANTLR4 common recipes

**Retrieval seeds:** operator precedence, left recursion, keyword vs identifier, separated list, channel HIDDEN, lexer mode

## Precedence (expression layers)

ANTLR4 accepts **direct left recursion**. Put higher-precedence operators in earlier alternatives (they bind tighter when rewritten):

```antlr
expr
    : expr ('*'|'/') expr      # Mul
    | expr ('+'|'-') expr      # Add
    | atom                     # AtomAlt
    ;

atom : INT | ID | '(' expr ')' ;
```

Associativity: left-recursive alts are left-associative by default. For right-assoc (e.g. `**`), use right recursion or an explicit `assoc=right` option on the alt where supported:

```antlr
expr
    : <assoc=right> expr '^' expr
    | INT
    ;
```

**Avoid** encoding precedence only with tangled `*` / `+` factor/term layers unless matching an existing textbook style the project already uses -- left-recursive form is usually clearer for LLMs.

## Keywords versus identifiers

Declare keyword tokens **above** the general identifier rule:

```antlr
IF   : 'if' ;
ELSE : 'else' ;
FOR  : 'for' ;
ID   : [a-zA-Z_] [a-zA-Z0-9_]* ;
```

Parser uses `IF` / `ID`, not string literals mixed ad hoc.

**Case-insensitive keywords** (ASCII):

```antlr
IF : [Ii] [Ff] ;
```

Or use a lexer action / predicate only when the language truly needs Unicode fold -- keep it documented.

**Keyword-as-identifier** (soft keywords): prefer a parser rule that accepts either, or a lexer `isystem`/predicate pattern; do not silently let `ID` eat keywords by reordering rules wrongly.

## Separated lists

```antlr
// One or more, comma-separated
argList : expr (',' expr)* ;

// Zero or more
optArgs : (expr (',' expr)*)? ;

// Trailing comma allowed
argListTrail : expr (',' expr)* ','? ;
```

Prefer this over recursion for flat lists -- simpler trees for visitors.

## Optional and repeated

| Meaning | Syntax |
|---------|--------|
| Optional | `rule?` or `( ... )?` |
| Zero or more | `rule*` |
| One or more | `rule+` |

## Channels (comments / whitespace kept)

```antlr
WS      : [ \t\r\n]+ -> channel(HIDDEN) ;
COMMENT : '/*' .*? '*/' -> channel(HIDDEN) ;
```

Parser ignores HIDDEN by default; tools can still read the channel for formatters.

Use `-> skip` when the token must never appear (typical for `WS` in simple grammars).

## String / escape sketch

```antlr
STRING
    : '"' ( ESC | ~["\\\r\n] )* '"'
    ;
fragment ESC : '\\' [btnfr"'\\] ;
```

Keep escapes in a **fragment**; avoid overly permissive `.*?` across quote styles without tests.

## Line-oriented dialects (optional application)

For line-based agent dialects (e.g. MemNet-style `id ; key=value` lines), a thin grammar often looks like:

```antlr
line : nodeLine | edgeLine | EOF ;
// ... field tokens, then a catch-all safe string rule
```

Treat that as an **illustration** only -- author the real dialect grammar from the project's published rules when asked; do not invent MemNet `.g4` here.

## Semantic predicates (sparingly)

```antlr
stat : {isType(getCurrentToken())}? ID ID '=' expr ';'  // declaration
     | ID '=' expr ';'                                  // assignment
     ;
```

Predicates reduce ambiguity but hurt portability and LLM readability -- prefer grammar structure first.
