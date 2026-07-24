# skillfish reference (condensed)

Upstream: **skillfish** npm CLI; registry/browse: **https://skill.fish**; spec context: **https://agentskills.io**.

## Common flags

- **Location:** `--project` (./), `--global` (~/)
- **Agents:** `--agent "Cursor"` (and others per upstream)
- **Non-interactive:** `--yes`, pipe/CI; **`--json`** on any command
- **add:** `--all`, `--path`, `--force`

## Manifest (`skillfish.json`)

- `bundle` writes manifest from **externally installed** skills (local `init` skills stay in git only).
- `install` syncs to manifest: installs/updates/removes **manifest-listed** skills; manually added skills are not removed by default.
- Pin refs: `owner/repo@v1.0.0`, `owner/repo@main/skills/my-skill`.

## Exit codes (typical)

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid args |
| 3 | Network |
| 4 | Not found |

## Telemetry opt-out

`DO_NOT_TRACK=1` or `CI=true` (upstream README).

## Security

Report vulnerabilities: **security@skill.fish** (per upstream). Always review skill source before installing.
