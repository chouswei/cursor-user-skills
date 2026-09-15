# Bind which skill graph (L3)

Load when the live path or SKG id is unclear. Keep [../SKILL.md](../SKILL.md) as the loop.

## Live paths

Pack seed (user-pack SKL only):

```text
~/.cursor/skills/reasoning-strategy-selector/references/skill-graph-seed.wire
```

Repo seed (project SKL; default if the open workspace is a git repo with `.cursor/skills/`):

```text
<repo>/.cursor/skills/skill-graph-seed.wire
```

Repo `AGENTS.md` MAY name a different seed path. If that path is missing, create from [../assets/repo-skill-graph-seed.wire](../assets/repo-skill-graph-seed.wire).

## SKG ids

| Id | Meaning |
|----|---------|
| `SKG_global` | Pack graph. Historical id; pack-scoped, not a universe graph. |
| `SKG_repo` | Default repo graph id. A repo MAY use `SKG_<slug>` if the seed names it. |

MemNet: cue the SKG id of the **bound** graph. Do not pin pack `SKG_global` and pretend it lists repo skills.

## Relatives

A **relative** is a typed edge (`COMPLEMENTS`, `PRECEDES`, `DEFAULT_STACK`, `SPECIALIZES`, `REQUIRES`) or a **pointer SKL** row:

```cypher
CREATE (:SKL {id: 'oosem-workflow', pack: 'user', pattern: 'P', dir: 'P', domain: 'sysml', path: '~/.cursor/skills/oosem-workflow', recycle: 'persistent'})
```

The pointer names a pack skill. The body stays in the user pack. Repo skills COMPLEMENTS or PRECEDES that id.

MUST NOT copy pack skill folders into `<repo>/.cursor/skills/` to express a relative.

## Scan / write

Pack:

```text
python tools/scan_skills_to_wire.py --write
```

from `reasoning-strategy-selector/` -- pack folders only.

Repo:

```text
python tools/scan_skills_to_wire.py --repo-skills <repo>/.cursor/skills --repo-seed <repo>/.cursor/skills/skill-graph-seed.wire --write
```

MUST NOT pass `--repo-skills` with `--write` and no `--repo-seed` (that used to merge into the pack seed).
