# Endleaf kinds

Live session 2026-10-01 (`listPlaybooks`, `getPlaybook`, `guide` `getting-started`). Listing label for all fifteen: `renders now; performance bar not yet measured` (可正常產生；效能基準尚未量測). That is not a sold performance bar.

Call `getPlaybook` with `kind` equal to `templateId` before rendering. Copy the playbook minimal body. MUST NOT invent macros. MUST NOT invent a sixteenth kind.

| `templateId` | Body | Formats | Notes |
|--------------|------|---------|-------|
| `document-shell` | Markdown | pdf, html, docx | Only native three-format kind. Fenced figures use `{.tikz caption= alt=}`. Max 5 fences. |
| `pidcircuit` | LaTeX picture | pdf; html/docx wrap | PIDcircuitTikZ (`circuit pid ISO14617`). Author in [pid-circuit-tikz](../../pid-circuit-tikz/SKILL.md). |
| `circuits` | LaTeX picture | pdf; html/docx wrap | circuitikz with siunitx quantities (`\qty`). |
| `plots` | LaTeX picture | pdf; html/docx wrap | pgfplots 2D and 3D (3D: max 25 samples/axis, one surf/mesh). Data inline only. |
| `chemistry` | LaTeX picture | pdf; html/docx wrap | chemfig structures and mhchem formulae (`\ce`). |
| `gantt` | LaTeX picture | pdf; html/docx wrap | pgfgantt (`\begin{ganttchart}`). No `\\` on final row. |
| `floorplan` | LaTeX picture | pdf; html/docx wrap | Coordinate-form floorplan with endleaf-floorplan.sty and tikz-dimline. |
| `sysml` | LaTeX picture | pdf; html/docx wrap | sysml-tikz. One `sysmlfigure` / `sysmlcanvas` (mm, y down). Size boxes with POSITION/LENGTH before place. Port square 3.2 mm. Line ends 1.6 mm outside port centre. Sheet B MUST draw internal `\sysmlport`. Inner IBD of a part definition: outer frame `\sysmlguillemets{part def}`, nested `\sysmlguillemets{part}` usages. MUST render each canvas on this kind before any `fulldoc` embed. |
| `fulldoc` | LaTeX document body | **pdf only** | Worker owns class (`article`, a4paper) and preamble. Mix sections, lists, tables, sysml-tikz, TikZ, circuitikz. Max 16 pages. Not labelled supported. MUST NOT be the first layout debug loop for SysML canvases. |
| `tikzcd` | LaTeX picture | pdf; html/docx wrap | One `tikzcd` environment. tikz-cd. `\feynmandiagram` and un-starred `\diagram` refused. |
| `forest` | LaTeX picture | pdf; html/docx wrap | One `forest` environment. Nested trees and syntax trees. |
| `automata` | LaTeX picture | pdf; html/docx wrap | One `tikzpicture` using preloaded TikZ automata. MUST NOT `\usetikzlibrary{automata}` again. |
| `mindmap` | LaTeX picture | pdf; html/docx wrap | One `tikzpicture` using preloaded TikZ mindmap. MUST NOT `\usetikzlibrary{mindmap}` again. |
| `tikztiming` | LaTeX picture | pdf; html/docx wrap | One `tikztimingtable`. Digital timing diagrams. |
| `bytefield` | LaTeX picture | pdf; html/docx wrap | One `bytefield` environment. Field widths MUST sum to the declared word width. |

HTML and DOCX for a picture `templateId` wrap as a `document-shell` tikz fence. Named playbooks and `document-shell` both remain valid for `tikzcd`, `forest`, `automata`, `mindmap`, `tikztiming` and `bytefield`.

Cursor `renderDocument.templateId` enum on this session still listed nine ids (`document-shell` through `fulldoc`). If the tool rejects a named playbook among the last six, use `document-shell`.

## Principles (MUST)

Lead with geometry. Steal reviews of foreign TikZ or Endleaf sources MUST extract transferable principles. MUST NOT stop at relatedness to this stack. MUST NOT invent new sizing math. Macro tables below stay sysml-tikz.

- **Size from the token, do not hope auto-fit:** widest line, 0.62 em/char at >=8 pt Heros, nLines includes stereotype + name + type, pad, 7 pt floor.
- **Position is a reserved rectangle:** labels MUST NOT share space with parts, ports, or connectors; port pitch from labelWidth + 4 mm; route around gutters.
- **One intent per sheet:** owner-lock Sheet A vs B. Sheet A system context MAY show usages and peers as `\sysmlguillemets{part}`. Inner IBD of a part definition: outer frame MUST be `\sysmlguillemets{part def}` (def name only); nested boxes MUST be `\sysmlguillemets{part}` usages; ports on borders; connectors on port edges (SysON interconnection). MUST NOT draw part-in-part as a type IBD.
- **Check the figure alone:** `templateId` `sysml` before `fulldoc`. Compile success is not ship.
- **Foreign recipes donate principles only:** block diagrams, TikZJax, book listings, smartdiagram MAY donate a principle (named nodes, `positioning`, no unpositioned edge labels). MUST NOT replace sysml-tikz or smuggle preamble, Mermaid, D2, or shrink-to-fit.

## Composition Law (first-class across all kinds)

Geometry MUST is Principles. This section is the scan and type stack. Composition law outranks macros. Sufficiency is an arm's-length human scan of the figure, not a TeX compile. Soft-pass "TeX compiled = ship" is forbidden. Compile success with crushed or colliding text is FAIL. Fail = re-layout; do not kern tighter.

- **Landscape (prefer over shrink):** Prefer a landscape page over shrink-to-fit or overlapping labels when supported.
- **Typography (first-class):** Worker owns preamble. Body/prose: TeX Gyre Pagella (`tgpagella`, 10 pt on `fulldoc` and `document-shell`). Headings: Pagella scale. Sans/diagram labels: TeX Gyre Heros (`tgheros`). Mono/tokens: TeX Gyre Cursor (`tgcursor`). zh-TW/CJK: xeCJK with Noto Sans CJK TC.

## Not playbooks and refused kinds

| Item | Fact from `guide` `getting-started` / playbooks |
|------|-------------------------------------------------|
| Mermaid | Refused (use `tikz` fence; draw flowcharts with TikZ positioning) |
| D2 | Refused |
| `tikz-feynman` | Refused (`\feynmandiagram` and un-starred `\diagram` refused; `\vertex` and `\diagram*` allowed) |
| `tikz-3dplot` | Installed; no named playbook |
| `tikz` | Guide topic only; no `tikz` templateId |

## Guide topics that are not kinds

| `topic` | When |
|---------|------|
| `getting-started` | Every task, before the first render |
| `tikz` | TikZ picture inside `document-shell` (there is no `tikz` templateId) |
| `pidcircuit` | Piping & instrumentation guidance |
| `circuits` | Circuit schematics guidance |
| `xecjk` | Traditional Chinese in the body |
| `quotas` | Limits and error codes |
| `teaching` | zh-TW lesson or worksheet; still `document-shell` |

## sysml (condensed)

Worker loads sysml-tikz. MUST NOT send a preamble.

- **Owner lock:** One layer per diagram. Sheet A = boundary ports + black-box child usages (name only) + external peers, all `\sysmlguillemets{part}`. Sheet B = one child's internals WITH `\sysmlport` on every connected nested part. If Sheet B is the definition of that child (example: `EiTungstenWirePowerDriver`), the outer frame MUST be `\sysmlguillemets{part def}` and nested boxes MUST be `\sysmlguillemets{part}` usages. MUST NOT draw part-in-part as a type IBD (that is a usage/configuration view). Never A and B together. MUST NOT omit Sheet B ports because Sheet A already showed the parent boundary.
- **Intent split:** Separate sheets for external IBD, digital/isolation, and power/islands.
- **POSITION/LENGTH (MUST, before place):** Size every part box from canvas lines, not from a mean Latin width. TeX Gyre Heros at >=8 pt (absolute floor 7 pt). One em = pt * 0.351 mm/pt. MUST NOT rely on mean Latin 0.50-0.55 em; proportional Heros undersizes W/m/G and long type names.
  - **Width:** from the widest canvas line (usage name or type), 0.62 em per character, plus ~4 mm pad.
  - **Height:** nLines * 1.35 em + ~3 mm pad. SysON interconnection-view parts count stereotype + usage name + type as separate lines. MUST NOT size as a single-line box.
  - Long qnames go in a table, not on the canvas. MUST NOT rely on `sysmlcanvas` auto-shrink. MUST NOT draw a tiny box then hope the token fits. If the widest line does not fit at 8 pt, shorten that token. MUST NOT pack manufacturer part numbers (MPNs) or the canvas words `CANDIDATE`, `MAY`, `TBD`, `SHOULD`.
- **Port labels and pitch (MUST):** Port pitch MUST be >= labelWidth + 4 mm, not a fixed 10 mm. Each port label occupies a reserved rectangle that MUST NOT intersect parts, port squares, or connectors. Route connectors around those rectangles.
- **Packing budget:** At most 8 parts on a canvas; at least 6 mm clear between boxes. MUST NOT let a port-label reserved rectangle intersect box, port square, connector, or another label.
- **Barrier:** One dashed line + at most a 6-word title. Detail prose goes under the figure (caption or note), never on geometry.
- **Header:** Human sheets show title (optional revision id). Hide worker diagnostics (`view`, `rev`, `overrides`, `depth`, `body size`).
- **Port geometry:** 3.2 mm square centred on `(cx,cy)`. Port direction arrow (`in`, `out`, `inout`) drawn inside square. `[conjugated]` or leading `~` flips arrow and shows `~`.
- **Figure check before fulldoc (MUST):** For every SysML canvas, call `renderDocument` with `templateId` `sysml` and that picture body only. Scan that PDF for Composition Law, POSITION/LENGTH boxes, port reserved rectangles, and ports on connectors. MUST NOT use `fulldoc` as the first layout debug loop. After the sheet passes, embed the same picture body in `fulldoc`. A failed, timed-out, busy, or refused render does NOT spend a job; a successful `sysml` or `fulldoc` render spends one job each.
- **Internal interconnect (Sheet B):** MUST place `\sysmlport` (3.2 mm squares) on every connected nested part. Connectors terminate on the port outer edge (1.6 mm outside centre), not on box centres. Visual target is the SysON Interconnection view: nested parts inside a parent frame, ports on part borders, connectors between those ports -- not a token cartoon (labelled boxes with centre-to-centre lines and no border ports). MUST draw the inner-IBD outer frame as the owning part DEFINITION (`\sysmlguillemets{part def}` + def name only; no usage name). Nested boxes stay `\sysmlguillemets{part}` usages. MUST NOT draw that outer frame as part-in-part (`\sysmlguillemets{part}` + usage name + type). Sheet A context IBD MAY keep `\sysmlguillemets{part}` usages + peers. SysON: https://doc.mbse-syson.org/syson/main/user-manual/features/sysmlv2-overview.html (section Interconnection view) and https://doc.mbse-syson.org/syson/main/user-manual/features/interconnection-view.html (encapsulated structure of *Usage* elements: parts, properties, connectors, ports, interfaces).
- **Connectors:** Lines stop on port outer edge, 1.6 mm outside port centre. MUST NOT draw line or arrowhead into the square. MUST NOT terminate a connector on a part-box centre.
  - `\sysmlconnection`: Solid connector, NO arrowhead unless `directed` (or `directed=true`) is set. Port direction does not choose line arrowhead.
  - `\sysmlflow`: Solid line with filled triangle pointing from `from` to `to`. `at=mid` places triangle at arc-length midpoint; item text centred on middle of `from` half.
  - `\sysmlbinding`: Solid line with upright `=` at arc-length midpoint, no arrowhead, not dashed.
  - `\sysmlinterface`: Solid line with optional `\sysmlguillemets{interface}`, no arrowhead.
  - `\sysmlsuccessionflow`: Dashed with filled triangle.
  - `\sysmlmessage`: Solid with hollow closed triangle.
  - `\sysmlallocation`: Solid with open stick head and `\sysmlguillemets{allocate}`.
- **Auto-fit:** The worker may auto-fit a canvas uniformly down to 7 pt. MUST NOT treat that as a layout method. Size every part box with POSITION/LENGTH first; text never below 7 pt. Model SSOT stays SysMLEdge / `.sysml`.

## fulldoc (condensed)

- LaTeX document body, NO preamble (`\documentclass`, `\usepackage`, `\RequirePackage`, or `\begin{document}`).
- Starts with `\title` / `\author` / `\maketitle` / `\section` / figures.
- `outputFormat` is **pdf only**. HTML and DOCX are refused before the worker and do not spend a quota job.
- Page cap: Max 16 pages (`maxPages=16`). Worker refuses a document exceeding 16 pages.
- Preamble hash: `73d55216488d240edccd26168576fcb402ce10794e04a3ef5ee8aec2bb166b98`.
- Figures: `figure` environment with `\caption`, `\label`, `\ref`. Placement `[htbp]`. Float pages top-aligned with fixed 12 pt gap. Worker sets `\belowcaptionskip` to 4 pt.
- SysML pictures use `sysmlfigure` and `sysmlcanvas`. Worker may auto-fit down to 7 pt; MUST still size boxes with POSITION/LENGTH before place. Sheet B MUST draw internal `\sysmlport`. MUST embed only canvases that already passed a `templateId` `sysml` render. MUST NOT debug SysML layout on `fulldoc` first.
- Plain TikZ and circuitikz are NOT auto-fitted (keep within 12 cm; wider pictures logged as `ENDLEAF_WIDE_PICTURE`).
- Cross-references resolve via worker second pass.
- Listing label: `renders now; performance bar not yet measured` (not labelled supported).

## Engine (from playbooks and `guide`)

XeLaTeX, xeCJK, Noto CJK TC, TikZ (`shapes`, `arrows.meta`, `positioning`, `calc`, `automata`, `mindmap`, `circuits.pid.ISO14617`), PIDcircuitTikZ, circuitikz, pgfplots, chemfig, mhchem, pgfgantt, tikz-dimline, tikzscale, siunitx, sysml-tikz, tikz-cd, forest, tikz-timing, bytefield, tikz-3dplot (no named playbook). No shell-escape. No network fetch. Other pgf libraries MAY load in the body with `\usetikzlibrary` except `external`.

Retrieval seeds: document-shell, pidcircuit, circuits, plots, chemistry, gantt, floorplan, sysml, fulldoc, tikzcd, forest, automata, mindmap, tikztiming, bytefield, tikz, xecjk, quotas, teaching, PIDcircuitTikZ, circuitikz, pgfplots, chemfig, sysml-tikz, tikz-cd, forest, tikz-timing, bytefield, maxPages, POSITION/LENGTH, 0.62 em, nLines, port pitch, reserved rectangle, sysmlport, Sheet B, part def frame, part usage, sysml before fulldoc, SysON interconnection view, Principles, steal review, foreign TikZ, TikZJax, smartdiagram
