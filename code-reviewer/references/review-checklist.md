# Code review checklist

## Review dimensions (every pass)

1. **Correctness** — Does the code do what it is supposed to?
2. **Edge cases** — Are error conditions handled (invalid input, failures, boundaries)?
3. **Style** — Does it follow **project** conventions (formatting, naming, patterns)?
4. **Performance** — Are there obvious inefficiencies (loops, I/O, allocation, N+1)?
5. **Token efficiency** — Is context load proportionate? Prefer high-signal, concise code and comments; avoid redundant duplication, noisy logging, and giant inline blobs. For prompts, agent instructions, or skill-like strings: no unnecessary repetition; factor shared text; keep only what execution needs at the call site.

## Security

- No SQL injection, XSS, or command injection risks
- Secrets are not hardcoded
- Proper authentication/authorization checks
- Dependencies are up to date (no known vulnerabilities)

## Readability and maintainability

- Functions are appropriately sized and focused
- Variable and function names are clear
- Comments explain "why", not "what"

## Testing

- Tests cover the changes
- Edge cases are tested
- Tests are readable and maintainable

## How to provide feedback

- Be **specific** about what needs to change (file, symbol, line or region when useful).
- Explain **why**, not just **what**.
- Suggest **alternatives** when possible.
