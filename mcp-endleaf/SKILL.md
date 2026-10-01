---
name: mcp-endleaf
description: >-
  Renders templated documents through Endleaf by InkMirage
  (MCP namespace user-endleaf, Cursor mcp.json key endleaf).
  Use when the user asks for an Endleaf PDF, HTML, or DOCX from a
  Markdown shell, a named LaTeX picture playbook, sysml-tikz, or fulldoc.
  SysML canvases MUST be checked with templateId sysml before fulldoc.
  SysML part boxes MUST use POSITION/LENGTH (widest line 0.62 em, nLines
  height); MUST NOT use mean Latin 0.50-0.55 em.
  Steal reviews of foreign TikZ or Endleaf sources MUST extract geometry
  principles; MUST NOT stop at relatedness to this stack.
  MUST NOT compile a repo documentclass pack here -- that is Overleaf
  (overleaf-free-cloud-olcli-mcp) or local latex.
  Triggers: Endleaf, InkMirage Endleaf, endleaf MCP, document-shell,
  fulldoc, sysml-tikz Endleaf, SysML POSITION/LENGTH, Sheet B
  internal ports, sysml before fulldoc, SysON interconnection view,
  steal TikZ principles, foreign Endleaf review, circuitikz Endleaf
  fence, tikzcd, forest, automata, mindmap, tikztiming, bytefield.
metadata:
  pattern: tool-wrapper
  domain: doc
  version: "1.8"
  secondary: "guide getting-started first, then getPlaybook; SysML figures: one sysml job each before fulldoc; steal reviews extract Principles; Endleaf != Overleaf"
---

# Endleaf MCP

Endleaf by InkMirage. Namespace `user-endleaf`. URL `https://endleaf.inkmirage.xyz/mcp`. Cursor `mcp.json` key `endleaf`. Auth header uses env `ENDLEAF_API_KEY`. MUST NOT paste that secret into this skill or a prompt.

Fifteen playbooks from live `listPlaybooks` (2026-10-01). Listing label for each is `renders now; performance bar not yet measured` (可正常產生；效能基準尚未量測). That is not a sold bar. `fulldoc` is not labelled supported. Mermaid and D2 are refused. `tikz-feynman` stays refused. `tikz-3dplot` stays installed with no named playbook.

Named playbooks: `document-shell`, `pidcircuit`, `circuits`, `plots`, `chemistry`, `gantt`, `floorplan`, `sysml`, `fulldoc`, `tikzcd`, `forest`, `automata`, `mindmap`, `tikztiming`, `bytefield`. MUST NOT invent extra `templateId` values. MUST call `listPlaybooks` when the list may have changed.

Endleaf is a templated render. MUST NOT send a repo `\documentclass` pack with its own preamble. That stays [overleaf-free-cloud-olcli-mcp](../overleaf-free-cloud-olcli-mcp/SKILL.md) (`user-overleaf`) or local latex. `fulldoc` is the Endleaf path for one article-shaped PDF whose class and preamble the worker owns.

`guide` `getting-started` (2026-10-01): named playbooks and `document-shell` both remain valid for `tikzcd`, `forest`, `automata`, `mindmap`, `tikztiming` and `bytefield`. A `document-shell` TikZ picture may use those worker packages with no extra worker package.

Cursor `renderDocument.templateId` enum on the same session still listed the original nine (`document-shell` through `fulldoc`). If `CallDynamicTool` rejects `tikzcd`, `forest`, `automata`, `mindmap`, `tikztiming` or `bytefield`, send a `document-shell` TikZ picture body instead. MUST NOT invent a host or a sixteenth kind.

## Order

1. Call `guide` first with `topic` `getting-started`. Load Principles before any kind. Other topics: `tikz`, `pidcircuit`, `circuits`, `xecjk`, `quotas`, `teaching`.
2. Call `getPlaybook` with `kind` equal to the `templateId`. Call `listPlaybooks` when the kind is unclear. Reads do not spend a render.
3. Load [references/render-contract.md](references/render-contract.md) and [references/kinds.md](references/kinds.md).
4. SysML canvases (including those later embedded in `fulldoc`): MUST apply Principles before place. MUST call `renderDocument` once per figure with `templateId` `sysml` and that picture body only. Scan each PDF against Principles (size, reserved rectangles, one intent, ports on connectors). MUST NOT use `fulldoc` as the first layout debug loop. After every sheet passes, embed the same picture body in `fulldoc` and then call `renderDocument` for `fulldoc`. Other kinds: one `renderDocument`.
5. The result is inline bytes, not stored. If the user asked for a file, write those bytes to the requested local path.
6. On tool `isError`, read `errorText` / `errorLine` / `failedFenceIndex` / `playbookKind`. Fix the body from those fields. Resend once per change. MUST NOT resend the identical failing body. MUST NOT loop. A failed, timed-out, busy, or refused render does NOT spend a job.

## Principles (MUST)

Lead with these geometry principles when authoring SysML canvases and when reviewing foreign TikZ or Endleaf sources. Steal reviews MUST extract transferable principles. MUST NOT stop at scoring how related a source is to this stack. MUST NOT invent new sizing math.

- **Size from the token, do not hope auto-fit:** Box width from the widest canvas line at 0.62 em per character at TeX Gyre Heros >=8 pt; nLines counts stereotype + usage name + type; add pad; 7 pt absolute floor. MUST NOT rely on `sysmlcanvas` auto-shrink or a mean Latin 0.50-0.55 em.
- **Position is a reserved rectangle:** Labels MUST NOT share space with parts, port squares, or connectors. Port pitch MUST be >= labelWidth + 4 mm. Route connectors around those gutters.
- **One intent per sheet:** Owner-lock Sheet A versus Sheet B. Inner IBD MUST be parent frame + nested parts + ports on borders + connectors on port edges (SysON interconnection view). MUST NOT mix A and B on one canvas.
- **Check the figure alone:** Render each canvas with `templateId` `sysml` before `fulldoc`. Compile success is not ship. Sufficiency is an arm's-length scan of that PDF.
- **Foreign recipes donate principles only:** Block diagrams, TikZJax, book listings, and smartdiagram MAY donate a principle (named nodes, `positioning`, no unpositioned edge labels). MUST NOT replace sysml-tikz. MUST NOT smuggle a foreign preamble, Mermaid, D2, or shrink-to-fit.

Detail and macro tables stay in [references/kinds.md](references/kinds.md) and [references/render-contract.md](references/render-contract.md).

## `renderDocument`

Required keys only (`additionalProperties` false): `lane`, `outputFormat`, `templateId`, `body`. MUST pass only those keys in `CallDynamicTool` arguments. MUST set `mcpDetails.description`.

| Argument | Values |
|----------|--------|
| `lane` | `InstruMeasure` \| `Weft` \| `Investor` |
| `outputFormat` | `pdf` \| `html` \| `docx` (`fulldoc` is `pdf` only) |
| `templateId` | live playbook id from `listPlaybooks` (see kinds table) |
| `body` | string; at most `maxInputKiB` from `guide` `quotas` |

MUST NOT send `\documentclass`, `\usepackage`, `\RequirePackage`, or `\begin{document}`. The worker owns the template.

Quota from `guide` `quotas` (2026-10-01): `jobsPerDay` 200, `perMinute` 5, `maxInputKiB` 2048. Playbook reads: `playbookReadsPerMinute` 30. `rejectBusy` waits `retryAfterSec` 60. A successful `renderDocument` spends one job. `uploadSource` does not spend a render. Reading `guide` or playbooks does not spend a render. A failed, timed-out, busy, or refused render does NOT spend a job. Playbook `Limits` tails may still print legacy 50 / 256 KiB; MUST prefer `guide` `quotas`. `maxFences=5` is from playbook `Limits`. `fulldoc` has `maxPages=16`.

Default `outputFormat` is `pdf` when the user does not name a format. `guide` `getting-started` says use `pdf`.

## Composition Law (first-class)

Geometry MUST is Principles. This section is the scan and type stack. Composition law overrides macro tips across every Endleaf kind. Sufficiency is an arm's-length human scan of the figure, not a TeX compile. Soft-pass "TeX compiled = ship" is forbidden. Compile success with crushed or colliding text is FAIL. Fail = re-layout; do not kern tighter.

- **Landscape:** Prefer landscape over shrink-to-fit or overlapping labels when supported.
- **Typography:** Worker preamble owns the single type stack. Body and prose: TeX Gyre Pagella (`tgpagella`, 10 pt on `fulldoc` and `document-shell`). Headings: Pagella scale. Sans and diagram labels: TeX Gyre Heros (`tgheros`). Mono/tokens: TeX Gyre Cursor (`tgcursor`). zh-TW/CJK: xeCJK with Noto Sans CJK TC.

## Core kinds summary

- `document-shell`: Markdown body; native `pdf`, `html`, `docx`. Up to 5 `tikz` fences (`{.tikz caption="..." alt="..."}`). Fences support `circuitikz`, `ganttchart`, `tikzcd`, `forest`, `automata`, `mindmap`, `tikztimingtable`, `bytefield`. Mermaid and D2 fences are refused.
- `sysml`: LaTeX picture body, `sysmlfigure` + `sysmlcanvas` (mm, y down). MUST size each part box with POSITION/LENGTH in kinds.md before place. MUST NOT rely on `sysmlcanvas` auto-shrink or draw a tiny box then hope the token fits. MUST NOT pack MPNs or the canvas words `CANDIDATE`, `MAY`, `TBD`, `SHOULD`. Owner lock: one layer per diagram (Sheet A = boundary ports + black-box children + peers; Sheet B = one child's internals WITH `\sysmlport` on every connected nested part). MUST NOT omit Sheet B ports because Sheet A already showed the parent boundary. Sheet B inner interconnect MUST look like a SysML/SysON interconnection view (nested parts in a parent frame, ports on borders, connectors between ports), not a token cartoon. At most 8 parts per canvas; >=6 mm clear between boxes. Port square 3.2 mm; connectors stop on the port outer edge (1.6 mm outside centre), not box centres; MUST NOT draw line or arrowhead into the square. Port direction (`in`, `out`, `inout`) stays inside square. `\sysmlconnection` has no arrowhead unless `directed`. MUST render each of these canvases with `templateId` `sysml` before embedding them in `fulldoc`.
- `fulldoc`: LaTeX document body, NO preamble (`\documentclass`, `\usepackage`, `\RequirePackage`, or `\begin{document}`). `pdf` only! HTML and DOCX refused before worker without spending a job. Max 16 pages (`maxPages=16`). Preamble hash `73d55216488d240edccd26168576fcb402ce10794e04a3ef5ee8aec2bb166b98`. Float pages top-aligned with 12 pt gap; `\belowcaptionskip` 4 pt. Worker may auto-fit SysML canvases down to 7 pt; MUST still size boxes with POSITION/LENGTH before place. MUST embed only SysML picture bodies that already passed a `templateId` `sysml` render. Plain TikZ and circuitikz are NOT auto-fitted (keep within 12 cm).

## Pair

| Need | Skill |
|------|--------|
| Endleaf Markdown / picture / sysml / fulldoc | this skill (`user-endleaf`) |
| Overleaf Free Cloud repo TeX | [overleaf-free-cloud-olcli-mcp](../overleaf-free-cloud-olcli-mcp/SKILL.md) |
| Local `.tex` | [mcp-latex](../mcp-latex/SKILL.md) |
| Picture authoring | [tikz](../tikz/SKILL.md); P&ID from [pid-circuit-tikz](../pid-circuit-tikz/SKILL.md) |
| SysML model SSOT | SysMLEdge / repo `.sysml`, not this render |
| Mermaid / D2 diagrams | mermaid skills locally; MUST NOT send those fences to Endleaf |
