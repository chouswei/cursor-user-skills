# GitHub Wiki principles

A GitHub Wiki is **many pages** at the wiki git **root**, plus `_Sidebar.md`. GitHub serves `Page-Name.md` as `/wiki/Page-Name`.

## What counts as a wiki

| Counts | Does not count |
|--------|----------------|
| One URL per topic; Home links out | All topics concatenated into Home |
| `_Sidebar` lists every page with `[[WikiLinks]]` | Pages that exist but never appear in the sidebar |
| Encyclopedic body a field reader can use | "See `deploy.sysml`" with no explanation |
| Optional Sources footer with repo paths | Secrets, pasted design-report chapters, PCB netlists |

**Single-page wiki is not a wiki.**

## Home

Home **MUST** be a hub: title, one-paragraph purpose, table of `[[Page-Name]]` links, short See also. Home **MUSTNOT** be the commissioning runbook, LAN map, MQTT map, and UI map in one file.

## WikiLinks

| Form | Use |
|------|-----|
| `[[Page-Name]]` | Default |
| `[[Page-Name\|label]]` | Piped display text |
| `[label](Page-Name)` | Markdown on the same wiki |

**MUSTNOT** treat `#anchors` on Home as if they were pages. **MUSTNOT** tell operators to open `docs/wiki/Foo.md` as the live handbook -- that path is the **versioned mirror**; the live site is `/wiki/Foo`.

## Three homes for text

| Home | Belongs | Does not |
|------|---------|----------|
| **GitHub Wiki** | Stand-alone how-tos, tables, See also | Secrets; architecture essays that replace the model |
| **Project git** (`docs/`, `docs/wiki/`) | Version file, wiki plan, **mirror** of wiki markdown | Per-part firmware trees copied wholesale |
| **System model** (if the repo has one) | Structure, ports, allocate, behaviour | Hand-edited wiki copies treated as SSOT |

If a system model exists: on conflict **the model remains the authority**. Correct the model first, then the wiki. The wiki **MUST** still **explain** so a reader can act without opening SysML.

**MUSTNOT** invent plant topology, DHCP owners, camera hosts, or switch port maps from memory. Verify each concrete number against that repo's SSOT. Example (not law): an edge switch **uplink port** is a modelled fact -- copy it only after checking the model, not because another plant used port 8.

## Versioned mirror vs publish

| Store | Role |
|-------|------|
| `docs/wiki/*.md` in the **project** git | Reviewable source; history with the product |
| `owner/repo.wiki.git` | What GitHub Wiki renders |

Author in the mirror (or directly in a wiki clone). **Publish** is a **copy** to the wiki root, then commit + push. Keep filenames ASCII; GitHub page slugs match file stems (`Commissioning.md` -> `Commissioning`).

## Language and secrets

British English unless the host wiki already uses another locale. **MUSTNOT** put passwords, tokens, or vendor logins in wiki pages.

## Retrieval seeds

github wiki, write wiki, publish wiki, _Sidebar, WikiLinks, wiki.git, Home hub, multi-page wiki, encyclopedic operator docs
