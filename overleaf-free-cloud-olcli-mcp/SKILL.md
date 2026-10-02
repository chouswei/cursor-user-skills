---
name: overleaf-free-cloud-olcli-mcp
description: >-
  Use when wiring, refreshing, or operating Overleaf Free Cloud from
  Cursor via @aloth/olcli (cookie MCP) — list/pull/push/compile, not
  self-host, not Git-token MCPs.
metadata:
  pattern: tool-wrapper
---
# Overleaf Free Cloud + olcli MCP

## When this applies
- LaTeX in Cursor against **Overleaf Free Cloud**
- Need to **add**, **fix**, or **refresh** the Overleaf MCP
- Auth errors / empty project list after weeks of idle use
- Choosing among Overleaf MCP packages

## Locked product choices (do not reopen casually)
- Prefer **Overleaf Free Cloud** over self-host on Pi / shared droplet next to lab stacks (InvenTree/MemNet/etc.)
- Free tier → **cookie auth**, not Git Integration tokens (Git usually needs paid)
- Canonical server: **`@aloth/olcli`** binary **`olcli-mcp`**
- Docs sometimes say `npx @aloth/olcli-mcp` — that package **does not exist** on npm (404). Use the form below.

## Correct MCP launch (`~/.cursor/mcp.json`)
```json
{
  "mcpServers": {
    "overleaf": {
      "command": "npx",
      "args": ["-y", "-p", "@aloth/olcli", "olcli-mcp"],
      "env": {
        "OVERLEAF_SESSION": "<overleaf_session2 cookie value>"
      }
    }
  }
}
```
- Backup `mcp.json` before editing, then reload MCP / restart Cursor
- Optional self-host only: also set `OVERLEAF_BASE_URL` (cookie may be `sharelatex.sid`)

## Cookie: `overleaf_session2`
1. Log into https://www.overleaf.com (project list visible)
2. DevTools → **Application** (not Console) → Cookies → `https://www.overleaf.com`
3. Name must be **`overleaf_session2`** (underscore). Ignore `overleaf.session2` (dot = stale)
4. Value is HttpOnly — Console `document.cookie` will **not** show it
5. Value starts with `s%3A` and is long (≥ ~80 chars). Short / `s%3Ac%3A1%3A…` = logged out
6. Never paste the cookie into chat transcripts; put it only in `mcp.json` env
7. Expires on the order of weeks — when tools fail auth, refresh and update `OVERLEAF_SESSION`

## Tool playbook (typical agent loop)
1. `list_projects` → pick `project_id`
2. `get_project_info` / `get_entities` → map files
3. Edit path: `pull_project` → local edit → `push_file` (or push one file at a time)
4. `compile` or `download_pdf` to verify
5. Comments: `list_comments` / `add_comment` / `reply_to_comment` / `resolve_comment` as needed
6. Destructive renames: `plan_project_renames` is **preview only**; bulk apply stays human CLI (`olcli project rename-bulk --apply`)

## What not to use on Free Cloud
- Git-token Overleaf MCPs (`OVERLEAF_GIT_TOKEN` / `olp_…`) for edit — usually paid
- Self-host Overleaf beside lab-critical stacks without a dedicated host decision

## Smoke test after wire / refresh
Call `list_projects`. Expect the account’s project list. If connection closed / 401 / empty with known projects → refresh cookie and restart the MCP server.

## Failure cheat sheet
| Symptom | Fix |
|--------|-----|
| npm 404 `@aloth/olcli-mcp` | Use `npx -y -p @aloth/olcli olcli-mcp` |
| Auth / empty list | Refresh `overleaf_session2`, update env, restart MCP |
| Cookie row missing | Not logged in, or wrong host — use `www.overleaf.com` cookies |
| Cursor doesn’t see tools | Reload MCP / restart Cursor after `mcp.json` edit |

## Pairing
- Session expired only → skill `overleaf-session-cookie-refresh`
- Endleaf/InkMirage Markdown/tikz PDF is not this skill -- use `mcp-endleaf` (`user-endleaf`). This skill compiles repo TeX on Overleaf Free Cloud (`user-overleaf`).
