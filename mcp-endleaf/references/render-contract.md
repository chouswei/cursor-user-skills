# Endleaf render contract

Live session 2026-10-01. Fetch playbook prose with `guide` and `getPlaybook`. MUST NOT invent fence syntax.

## Transport

- Product: Endleaf by InkMirage
- Namespace: `user-endleaf`
- URL: `https://endleaf.inkmirage.xyz/mcp`
- Cursor `mcp.json` key: `endleaf`
- Auth: env `ENDLEAF_API_KEY` (MUST NOT paste the secret)
- Signup: https://endleaf.inkmirage.xyz/signup (email confirm and Turnstile). Paid plans are not available yet.
- Skill resource: `endleaf://guide/skill`

## Tools

`guide` (call first), `listPlaybooks`, `getPlaybook` (`kind`), `renderDocument`.

`guide` topics: `getting-started`, `tikz`, `pidcircuit`, `circuits`, `xecjk`, `quotas`, `teaching`.

## `renderDocument` arguments

`additionalProperties` false. MUST pass only these keys. MUST set `mcpDetails.description`.

| Argument | Values |
|----------|--------|
| `lane` | `InstruMeasure`, `Weft`, `Investor` |
| `outputFormat` | `pdf`, `html`, `docx` (`fulldoc` is `pdf` only) |
| `templateId` | one of the fifteen live playbook ids from `listPlaybooks` |
| `body` | string; at most `maxInputKiB` from `guide` `quotas` |

MUST NOT send `\documentclass`, `\usepackage`, `\RequirePackage`, or `\begin{document}`.

`document-shell` body is Markdown. `fulldoc` body is a LaTeX document body, `pdf` only. Every other `templateId` takes a LaTeX picture body.

HTML and DOCX for a picture `templateId` are wrapped as a tikz fence under `document-shell`. HTML and DOCX for `fulldoc` are refused before the worker and do not spend a job.

If Cursor rejects a named playbook `templateId` that `listPlaybooks` still lists (`tikzcd`, `forest`, `automata`, `mindmap`, `tikztiming`, `bytefield`), fall back to `document-shell` (see kinds.md).

## Quota and limits (from `guide` `quotas`)

From `guide` `quotas` (2026-10-01): `jobsPerDay` 200, `perMinute` 5, `maxInputKiB` 2048. Playbook reads: `playbookReadsPerMinute` 30 (`rejectPlaybookRate`).

- A successful `renderDocument` spends one job.
- `uploadSource` does not spend a render.
- Reading `guide` or `getPlaybook` does not spend a render.
- A failed, timed-out, busy, or refused render does NOT spend a job. Fix the source and send it again. MUST NOT loop.
- Result is inline bytes, not stored. Write bytes to a local path when the user requests a file.

Playbook `Limits` tails may still print legacy `jobsPerDay=50` and `maxInputKiB=256`. MUST prefer `guide` `quotas`.

Playbook `Limits` still enforce `maxFences=5` under `document-shell`.

`fulldoc` only: `maxPages=16` (worker refuses a document exceeding 16 pages).

## Principles (MUST)

Lead with geometry. Steal reviews MUST extract transferable principles from foreign TikZ or Endleaf sources. MUST NOT stop at relatedness. MUST NOT invent new sizing math. Size from the token (widest line, 0.62 em/char, nLines = stereotype + name + type, pad, 7 pt floor). Position is a reserved rectangle (port pitch >= labelWidth + 4 mm; route around gutters). One intent per sheet; owner-lock Sheet A vs B. Sheet A system context MAY show usages as `\sysmlguillemets{part}`. Inner IBD of a part definition: outer frame MUST be `\sysmlguillemets{part def}`; nested boxes MUST be `\sysmlguillemets{part}` usages; SysON interconnection. MUST NOT draw part-in-part as a type IBD. Check `templateId` `sysml` before `fulldoc`; compile success is not ship. Foreign recipes MAY donate a principle (named nodes, `positioning`, no unpositioned edge labels). MUST NOT replace sysml-tikz or smuggle preamble, Mermaid, D2, or shrink-to-fit.

## Composition Law (first-class)

Geometry MUST is Principles. This section is the scan and type stack. Composition law overrides macro tips across every Endleaf kind. Sufficiency is an arm's-length human scan of the figure, not a TeX compile. Soft-pass "TeX compiled = ship" is forbidden. Compile success with crushed or colliding text is FAIL. Fail = re-layout; do not kern tighter to hide a collision.

- **Landscape:** Prefer a landscape page over shrink-to-fit or overlapping labels when supported.
- **Typography:** Worker preamble owns the single type stack. Body and prose: TeX Gyre Pagella (`tgpagella`, 10 pt on `fulldoc` and `document-shell`). Headings: Pagella scale. Sans and diagram labels: TeX Gyre Heros (`tgheros`). Mono/tokens: TeX Gyre Cursor (`tgcursor`). zh-TW/CJK: xeCJK with Noto Sans CJK TC.

## Refused kinds and sandbox restrictions

- Mermaid and D2 are refused. This render path is TikZ only. Use `tikz` fences; draw flowcharts with TikZ positioning.
- `tikz-feynman` stays refused (`\feynmandiagram` and un-starred `\diagram` refused; `\vertex` and `\diagram*` stay allowed).
- `tikz-3dplot` stays installed with no named playbook.
- Forbidden: `\write18`, shell-escape, Asymptote, outside programs, network, TikZ external library, file reads by path (`\input` or `\include` of `/...` or `../...`, `\openin`, `\read`), runaway loops, cap evasion, graphdrawing, Lua.

## document-shell fences

Fence class is always `tikz`. Info string shape from the playbook: `{.tikz caption="..." alt="..."}`. Body is the environment the kind requires (`tikzpicture`, `circuitikz`, `ganttchart`, `tikzcd`, `forest`, `tikztimingtable`, `bytefield`, etc.). At most five fences.

CJK in Markdown prose uses xeCJK. CJK inside a fence needs the playbook Noto workaround unless the kind is a native PDF picture (`sysml` PDF CJK is direct).

## Errors (from `guide` `quotas`)

Tool result (`isError`):
- `rejectInvalidInput`: The request is not usable. A preamble or `\documentclass` causes this error. HTTP 400 or HTTP 200 with `isError`.
- `rejectPreflight`: The body uses a refused construct. HTTP 200 with `isError`.
- `rejectRenderError`: TeX failed. HTTP 200 with `isError`. Read `errorText`, fix the body, and resend.

JSON-RPC errors:
- `rejectBusy`: Service busy. HTTP 429. Carries `retryAfterSec` 60. Wait, then send the job again.
- `rejectBadKey`: Key is missing or not accepted. HTTP 401.
- `rejectKillSwitch`: Rendering is stopped. HTTP 403.
- `rejectStoreDown`: Keys cannot be read right now. HTTP 503.
- `rejectOverQuota`: Key has used its free tier. HTTP 429.
- `rejectPlaybookRate`: Playbook reads over the per-minute limit (30/min). HTTP 429. (Not the render quota).
- `rejectUnreachable`: Render service could not be reached. HTTP 503.
- `rejectNoResult`: No result arrived in time. HTTP 504.
- `failTimeout`: Job ran too long. HTTP 504.
- `failCapHit`: Job hit a resource cap. HTTP 502.
- `rejectSpawnFail`: Job did not start. HTTP 502.
- `rejectLinkDropped`: Job connection dropped. HTTP 502.
- `rejectUnboundConfig`: Service is not configured. HTTP 503.

MUST NOT treat an empty `errorText: unknown` on a playbook read as a packing error.

## SysML canvas layout (author, not worker auto-fit)

MUST size every part box with POSITION/LENGTH before place. TeX Gyre Heros at >=8 pt (absolute floor 7 pt). One em = pt * 0.351 mm/pt. MUST NOT rely on mean Latin 0.50-0.55 em; proportional Heros undersizes W/m/G and long type names.

- **Width:** from the widest canvas line (usage name or type), 0.62 em per character, plus ~4 mm pad.
- **Height:** nLines * 1.35 em + ~3 mm pad. SysON interconnection-view parts count stereotype + usage name + type as separate lines. MUST NOT size as a single-line box.
- **Port pitch:** MUST be >= labelWidth + 4 mm, not a fixed 10 mm.
- **Port labels:** each occupies a reserved rectangle that MUST NOT intersect parts, port squares, or connectors. Route connectors around those rectangles.

Long qnames go in a table. MUST NOT rely on `sysmlcanvas` auto-shrink. MUST NOT pack MPNs or the canvas words `CANDIDATE`, `MAY`, `TBD`, `SHOULD`. If the widest line does not fit at 8 pt, shorten that token.

Sheet A = boundary ports + black-box children + peers as `\sysmlguillemets{part}` usages. Sheet B = one child's internals WITH `\sysmlport` (3.2 mm) on every connected nested part. If Sheet B is the inner IBD of a part definition (example: `EiTungstenWirePowerDriver`), the outer frame MUST be `\sysmlguillemets{part def}` and nested boxes MUST be `\sysmlguillemets{part}` usages. MUST NOT draw part-in-part as a type IBD (that is a usage/configuration view). Connectors stop on the port outer edge (1.6 mm outside centre), not box centres. MUST NOT omit Sheet B ports because Sheet A already showed the parent boundary.

Sheet B inner interconnect MUST look like a SysML/SysON interconnection view, not a token cartoon: part-def frame, nested part usages, ports on part borders, connectors between those ports. SysON overview: https://doc.mbse-syson.org/syson/main/user-manual/features/sysmlv2-overview.html . Interconnection view: https://doc.mbse-syson.org/syson/main/user-manual/features/interconnection-view.html (encapsulated structure of *Usage* elements: parts, properties, connectors, ports, interfaces).

## SysML figure check before fulldoc

MUST call `renderDocument` once per SysML canvas with `templateId` `sysml` and that picture body only. Scan each PDF against Principles (size, reserved rectangles, one intent, ports on connectors). MUST NOT use `fulldoc` as the first layout debug loop. After every sheet passes, embed the same picture body in `fulldoc` and then render `fulldoc`. A failed, timed-out, busy, or refused render does NOT spend a job. Each successful `sysml` or `fulldoc` render spends one job.

## Not Overleaf

MUST NOT use Endleaf to compile a repo `\documentclass{article}` tree with its own preamble and figures. That stays Overleaf (`user-overleaf`) or local latex. `fulldoc` is one worker-owned article body, not a repo pack.

Retrieval seeds: Endleaf, InkMirage, renderDocument, guide, getPlaybook, templateId, document-shell, fulldoc, sysml, tikzcd, forest, automata, mindmap, tikztiming, bytefield, lane, InstruMeasure, Weft, Investor, outputFormat, pdf, html, docx, quota, 200, 2048 KiB, rejectInvalidInput, rejectRenderError, circuitikz, sysml-tikz, no preamble, not Overleaf, POSITION/LENGTH, 0.62 em, nLines, port pitch, reserved rectangle, sysmlport, Sheet B, part def frame, part usage, sysml before fulldoc, SysON interconnection view, Principles, steal review, foreign TikZ
