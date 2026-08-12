# Fusion MCP + ElectronFileOutput

## Server

- Cursor key: `fusionMCP` → URL `http://127.0.0.1:27182/mcp`
- Discovered server id: typically `user-fusionMCP`
- Prefer built-in Fusion MCP over third-party bridges

## `fusion_mcp_read`

| queryType | Notes |
|-----------|--------|
| `document` + `operation=search` | Requires `name`; optional `project` |
| `document` + `operation=open` | Lists open documents (no fileId) |
| `document` + `operation=recent` | Recent files |
| `screenshot` | Needs active graphics canvas; electronics may return "No active graphics canvas" |
| `projects` | Hub project list |

Search is fuzzy and case-insensitive; unrelated hits are common — filter by `parentFolder` / exact product name.

## `fusion_mcp_execute`

| featureType | Notes |
|-------------|--------|
| `document` + `open` | `object.fileId` = lineage URN from search |
| `document` + `close` | If dirty: require `userConfirmedSaveAndClose` or `userConfirmedCloseWithoutSave` (ask user) |
| `document` + `save` | **Only if user explicitly asks** |
| `script` | Must define `def run(_context: str):`; prints become tool output; do not swallow exceptions |

### Script tip — list / activate

```python
import adsk.core

def run(_context: str):
    app = adsk.core.Application.get()
    for i in range(app.documents.count):
        d = app.documents.item(i)
        print(i, d.name, "active", d.isActive)
        if d.name == "Schematic-PA107":
            d.activate()
```

## `fusion_mcp_electronics_read`

Pass `entity_type` (examples):

- `electronics.Schematic`, `electronics.Sheet`, `electronics.Part`, `electronics.Net`
- `electronics.Board`, `electronics.Element`, `electronics.Signal`, `electronics.Layer`
- `electronics.DeviceSet`

Optional `object.fields`, `object.pagination.limit`.

### Pitfalls

1. **Sticky product context** — activating a different Fusion document does not always switch electronics_read; Schematic path may stay on the first product.
2. **Empty Board/Element** — layer table may appear with `used:0` while a real `.brd` exists in ElectronFileOutput; trust the cache file.
3. **Duplicate names** — same display name can have multiple lineage IDs (sch vs brd vs revisions); record all useful IDs in `fusion.toml`.
4. **Open failures** — `Failed to open document for fileId` → try alternate lineage from search; document may already be open (`alreadyOpen: true`).

## ElectronFileOutput layout

```
%LOCALAPPDATA%/Temp/Neutron/ElectronFileOutput/<sessionId>/
  sch-<uuid>/<Design>.sch
  brd-<uuid>/<Design>.brd
  .../small.png
```

`<sessionId>` is often a numeric PID-like folder (e.g. `38436`). Prefer the newest session that contains the opened design names.

PowerShell list (Windows):

```powershell
$dir = "$env:LOCALAPPDATA\Temp\Neutron\ElectronFileOutput"
Get-ChildItem $dir -Directory | Sort-Object LastWriteTime -Descending | Select-Object -First 3
```

Then list children of the newest session for `*.sch` / `*.brd`.

## Repo landing conventions

| Field | Example |
|-------|---------|
| Folder | `parts/rf-power-amplifier/hardware/fusion-pa107/` |
| `fusion_hardware` | `hardware/fusion-pa107` |
| Lineage | `urn:adsk.wipprod:dm.lineage:...` |

Shared designs (e.g. Aux reusing PA107): set `fusion_hardware_candidate` to a relative path; do not duplicate binary files without a reason.

## Retrieval seeds

fusionMCP, ElectronFileOutput, electronics.Part, lineage URN, parts/*/hardware/fusion-, .sch .brd fetch
