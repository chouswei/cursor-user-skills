# ANTLR4 toolchain

**Retrieval seeds:** antlr4-tools, antlr4-python3-runtime, -Dlanguage=Python3, generate visitor, Java target, JavaScript target, grun

Prefer documenting **commands the agent can run**. Adjust package managers to the project.

## Python3 (default for this pack)

```bash
pip install antlr4-tools antlr4-python3-runtime

# Generate lexer, parser, visitor (no listener)
antlr4 -Dlanguage=Python3 -visitor -no-listener Path/To/MyGrammar.g4
```

Typical outputs beside the `.g4`: `MyGrammarLexer.py`, `MyGrammarParser.py`, `MyGrammarVisitor.py`, `*.tokens`, `*.interp`.

Smoke parse:

```python
from antlr4 import InputStream, CommonTokenStream
from MyGrammarLexer import MyGrammarLexer
from MyGrammarParser import MyGrammarParser

def parse(text: str):
    lexer = MyGrammarLexer(InputStream(text))
    stream = CommonTokenStream(lexer)
    parser = MyGrammarParser(stream)
    tree = parser.prog()  # start rule
    return tree
```

**Validate loop:** edit `.g4` → re-run `antlr4 ...` → run smoke tests → fix grammar (not generated files).

### Windows notes

- Use ASCII paths; quote paths with spaces.
- In PowerShell chain with `;`, not `&&`.
- If `antlr4` is not on `PATH`, use `python -m antlr4_tools.antlr4` equivalent via the installed `antlr4` console script from `antlr4-tools`.

## Java

```bash
# Requires JDK and antlr-4.x-complete.jar on CLASSPATH (version per project)
java -jar antlr-4.13.2-complete.jar -visitor MyGrammar.g4
javac MyGrammar*.java
# Optional tester
grun MyGrammar prog -gui
```

`grun` is the runtime test rig (`org.antlr.v4.gui.TestRig`).

## JavaScript / TypeScript

```bash
antlr4 -Dlanguage=JavaScript -visitor -no-listener MyGrammar.g4
# or TypeScript target when the project already uses it:
# antlr4 -Dlanguage=TypeScript -visitor MyGrammar.g4
```

Install matching runtime (`antlr4` npm package) at the version compatible with the tool. Prefer the project's existing ANTLR major version -- do not mix 4.9 runtime with 4.13 generated code.

## Useful flags

| Flag | Purpose |
|------|---------|
| `-Dlanguage=Python3` | Target language |
| `-visitor` | Emit visitor base class |
| `-no-listener` | Skip listener if unused |
| `-listener` | Emit listener (default on many installs) |
| `-o dir` | Output directory |
| `-lib dir` | Token vocab / import search path |
| `-Xexact-output-dir` | Put outputs exactly in `-o` |

## Version alignment

- Tool jar / `antlr4` CLI major.minor should match the **runtime** package.
- Pin both in the project lockfile when shipping parsers.
- After upgrading the tool, regenerate all `.g4` outputs in one pass.

## Minimal check without a full app

1. Generate for the target.
2. Parse a fixture string ending so `EOF` matches.
3. On failure, read `parser.getNumberOfSyntaxErrors()` / exception message; fix the **grammar or input**, regenerate, retry.

## CI suggestion

```text
antlr4 -Dlanguage=Python3 -visitor -no-listener grammars/*.g4
pytest tests/parser/
```

Fail the job if generation or tests fail; commit generated sources only if the project already does (many repos generate in CI instead).
