# Local patches (user pack)

## Windows ESM loader (`pathToFileURL`)

Upstream `loadBeautifulMermaid()` used `import(pkgPath)` with a Windows absolute path (`C:\...`), which Node ESM rejects.

**Patched files:** `scripts/render.mjs`, `scripts/batch.mjs`, `scripts/themes.mjs` — use `import(pathToFileURL(pkgPath).href)`.

Re-apply after upstream pull if the bug persists in [imxv/Pretty-mermaid-skills](https://github.com/imxv/Pretty-mermaid-skills).
