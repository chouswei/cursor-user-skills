---
name: mcp-digikey
description: >-
  DigiKey MCP (user-digikey): keyword search, product details, pricing, substitutions,
  media, categories. Use when sourcing parts, checking stock/price, or resolving DigiKey
  / manufacturer part numbers. Triggers: digikey, digi-key, digikey mcp, MPN search,
  digikey pricing, product substitutions.
metadata:
  pattern: tool-wrapper
  specialization: mcp-integration
  domain: hardware
  mcp_key: digikey
  version: "1.1"
token_guardrails: |
  - Discover schema with GetMcpTools(server=user-digikey) before CallMcpTool.
  - Never store DigiKey client secrets or tokens in skill files, SysML, or READMEs.
  - Prefer small `limit` on keyword_search; deepen with product_details / get_product_pricing.
  - OAuth OK + Product API 401 → fix DigiKey app Product Information entitlement; do not loop mcp_auth.
---

# MCP: DigiKey (`user-digikey`)

## When to use

- Search catalog by keyword or MPN
- Fetch datasheet links / media, pricing tiers, DigiReel quotes, substitutions
- Disambiguate manufacturer vs DigiKey product numbers

## Tool discovery and auth

1. `GetMcpTools(server="user-digikey")` (or `toolName` for one tool) before every new call shape.
2. If `serverStatus` is `needsAuth` or a call returns **401 / unauthorized**: call `mcp_auth` with **empty arguments** once, then re-check the server and retry.
3. Do **not** spam `mcp_auth` if auth succeeded but Product API still fails (see pitfalls).

## Essential tools

| Tool | Use |
|------|-----|
| `keyword_search` | Primary search (`keywords` required; optional `limit`, filters, sort) |
| `product_details` | Full product record by DigiKey or manufacturer PN |
| `get_product_pricing` | Price breaks / quantity |
| `get_digi_reel_pricing` | DigiReel-compatible PNs only |
| `search_product_substitutions` | Alternates |
| `get_product_media` | Images / docs / videos |
| `search_categories` / `get_category_by_id` / `search_manufacturers` | Browse filters |

## Typical workflow

1. `keyword_search` with a tight keyword or MPN (`limit` 5–10).
2. Pick a DigiKey product number → `product_details`.
3. If quoting BOM → `get_product_pricing` with `requested_quantity`.
4. Optional: substitutions or media for DFM / docs.

## Pitfalls — 401 after successful `mcp_auth`

Cursor OAuth/`mcp_auth` can succeed while DigiKey **Product Information API** still rejects calls. Check:

1. **API Product access** — DigiKey developer app must have **Product Information** (search/details) enabled, not only OAuth login.
2. **Client credentials** — Client ID/secret in the DigiKey developer portal match what the MCP server uses; regenerate if rotated.
3. **Environment** — sandbox vs production keys; mismatched base URL causes opaque 401s.
4. **Scopes / subscription** — some orgs need an approved DigiKey API plan before Product endpoints work.

If auth UI completed and tools still 401, tell the user to verify the DigiKey app’s **Product Information API** entitlement and credentials — do not loop `mcp_auth`. Keyword search and Product Details share that Product API surface.

## Pairing

- BOM / PCBA sourcing: project `hardware-custom-pcba-workflow` or atopile creating-packages when in a system repo
- Inventory after pick: `mcp-inventree` (user pack); IMD self-dev IPNs → repo `imd-clickup-inventree-part-number`
---
