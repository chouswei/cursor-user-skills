# Atom cards and waves

Bind-ready means a list of atom cards. Missing fields means not ready.

## Atom card (MUST)

```
id: A2
wave: 1
order: 1
role: Implement
model_family: Gemini flash high
scope:
  paths: [parts/foo/bar.py]
  qnames: [Pkg::Part]
  hosts: []
  memnet_ids: []
proof:
  cmd: python -m pytest parts/foo -q
  pass_if: exit 0
return: files_changed, proof_tail, blockers
must_not: [edit other paths, settle TSK_*]
```

`wave` is the parallel group. `order` sequences atoms that are not disjoint (later wave) or a serial successor after a named proof.

Worker `prompt` is this card plus: campaign `session=` if any; SysMLEdge `projectId@rev` if bound; write only inside `scope`; return the contract below.

## Worker return (MUST)

```
atom_id: A2
status: pass | fail | blocked
files_changed:
proof_cmd:
proof_tail:
blockers:
```

## Disjoint (same wave)

Two atoms may share a wave only if they share **none** of: a write-path, a write-qname, a live host they mutate, a MemNet node they mutate. Read-only overlap is allowed.

If any pair overlaps on a write, Bind MUST raise the later atom's `wave`. MUST NOT put overlapping writes in one wave and hope the workers serialise.

## Ready set

Ready atoms = unsettled cards whose `wave` equals the smallest unsettled `wave`, and whose pairwise scopes are disjoint (true by construction if Bind followed the rule). Spawn that whole set in one parent message.

## Anti-patterns

| Fail | Why |
|------|-----|
| One Task prompt "do A then B" | Collapses atoms; Multitask default |
| Implement before Bind-ready cards | No disjoint test, no proof |
| Parent Implements after tagging Implement | Skips the role |
| Resume worker onto a new atom | Hidden bundling |
| Proof = "looks good" | Not a command with `pass_if` |
| Deploy atom authors files | Split: Implement then Deploy |
