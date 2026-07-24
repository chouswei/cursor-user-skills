# Commit message — self-review rubric

## Must pass

- **Conventional format:** `type(scope): subject` (scope optional if unknown).
- **Type** is one of allowed types from `commit-style-guide.md`.
- **Subject:** imperative mood, ≤50 characters, no trailing period.
- **Breaking change:** if breaking, `BREAKING CHANGE:` or `!` after type per guide convention.

## Should pass

- **Body** explains what and why when change is non-obvious; references `Closes #` when applicable.

## Step-4 JSON

Emit: `pass` (bool), `violations` (string[]), `revision_note` (string). Max **1** revision.

## Retrieval seeds

conventional commit rubric imperative subject scope breaking change
