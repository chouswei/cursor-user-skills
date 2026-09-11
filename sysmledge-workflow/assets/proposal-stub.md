# Proposal stub -- copy into sysml-models/proposals/<id>/

Replace `<id>`, `<base.sha>`, qnames, and the delta body. `delta.sysml` is SysML text only.

## PATCH.md

```markdown
# Proposal <id>

- **base.sha:** <40-char git SHA of current when proposed>
- **stale:** false
- **affected qnames:**
  - `<package>::<part>`
- **intent:** <one sentence>
- **human apply:** merge `delta.sysml` into `sysml-models/`, then whole-tree Save.

If current.sha != base.sha, this proposal is invalid until regenerated or a human rebases.
```

## delta.sysml

```sysml
// SysML delta against base.sha. Not GQL. Not Cypher. Not a MemNet snapshot.
package ProposalDelta {
  // human applies this into the author tree, then Save
}
```
