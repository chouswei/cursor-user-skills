---
name: overleaf-session-cookie-refresh
description: >-
  Use when Overleaf MCP auth fails or the session expired — refresh
  overleaf_session2 and update ~/.cursor/mcp.json without reinstalling.
metadata:
  pattern: pipeline
---
# Overleaf session cookie refresh

## When this applies
- Overleaf MCP tools fail with auth / empty project list / connection errors after previously working
- User says the Overleaf session expired or asks to refresh the cookie
- Smoke test `list_projects` fails and wiring is already known-good

## Do not do
- Do not paste the cookie into chat
- Do not scrape Chrome cookie DB / CDP / Playwright
- Do not reinstall Overleaf or change hosts — this skill only refreshes `OVERLEAF_SESSION`

## Steps
1. Confirm the MCP launch line is still `npx -y -p @aloth/olcli olcli-mcp` (not the nonexistent `@aloth/olcli-mcp` package).
2. Get a fresh `overleaf_session2` value from DevTools → Application → Cookies → `https://www.overleaf.com` (underscore name only).
3. Validate: value starts with `s%3A`, length ≥ ~80. Reject anonymous/short values.
4. Backup then update `~/.cursor/mcp.json` → `mcpServers.overleaf.env.OVERLEAF_SESSION`.
5. Reload MCP / restart Cursor.
6. Smoke: `list_projects` returns the account’s projects.

## Cookie checklist
| Check | Expect |
|-------|--------|
| Cookie name | `overleaf_session2` (underscore) |
| Host | `www.overleaf.com` |
| Prefix | `s%3A…` |
| Console `document.cookie` | Empty for this cookie (HttpOnly) — use Application panel |

## Done when
`list_projects` works and Cursor Overleaf MCP tools respond after reload.

## Pairing
- Full wire / Free-tier playbook → skill `overleaf-free-cloud-olcli-mcp`
