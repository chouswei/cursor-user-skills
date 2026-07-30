# How to use the SysML v2 Release repo

The **[Systems-Modeling/SysML-v2-Release](https://github.com/Systems-Modeling/SysML-v2-Release)** repository is the **official OMG SysML v2 release**: specs, example models, normative libraries, and installers for pilot editors. This doc summarizes how to use it (here and in general).

**In this workspace we use Cursor as the primary environment** — see [Primary workflow: Cursor](#primary-workflow-cursor) below.

---

## Primary workflow: Cursor

You can do **most SysML work in Cursor** without installing Eclipse or Jupyter from the Release repo:

1. **Edit `.sysml` in Cursor** — Open and edit models under `sysml-v2-models/projects/<name>/models/`. Use the Release repo as **reference only**: [doc/](https://github.com/Systems-Modeling/SysML-v2-Release) for specs (PDFs), [sysml/](https://github.com/Systems-Modeling/SysML-v2-Release/tree/master/sysml) and [kerml/](https://github.com/Systems-Modeling/SysML-v2-Release/tree/master/kerml) for examples. For syntax during editing, use [sysml-v2-syntax-reference](../../sysml-v2-syntax-reference/references/sysml-v2-syntax-reference.md) or the spec PDFs in the Release doc/. Cursor has no built-in SysML language server, so you edit as text; [SYSML_V2_MCP_SETUP.md](../../../docs/mcp/SYSML_V2_MCP_SETUP.md) and [copilot-instructions](../../../.github/copilot-instructions.md) guide agents.
2. **Normative library** — Get the Release content under `sysml-v2-models/libs/omg/SysML-v2-Release/` (submodule or clone) so the **visualizer** can load Base.kerml, ScalarValues.kerml, and (if needed) ISQ/SI. You don’t run an editor from the Release; our scripts just need those files on disk.
3. **SysML v2 MCP (agents)** — **validate** after `.sysml` edits; **preview** for diagrams (do **not** use **visualizeFile**). **Do not** default to `visualize.py` unless the user asks for on-disk exports. See [AGENTS.md](../../../AGENTS.md) and [SYSML_V2_MCP_SETUP.md](../../../docs/mcp/SYSML_V2_MCP_SETUP.md).
4. **Optional terminal scripts** — Other project scripts (report, sync, etc.) and optional `visualize.py` for PNG/SVG in `projects/<name>/outputs/` when you want files on disk.

So: **Cursor = main editor and AI pair-programming; Release repo = library + spec/examples reference.** Eclipse and Jupyter (from the Release `install/`) are optional if you want a dedicated SysML IDE or notebooks.

**If you develop Python (or other code) in a different repo** that must follow these models, see [SYSML_IN_VIBE_CODING.md](../../../docs/SYSML_IN_VIBE_CODING.md) §6: use a generated export, a read-only submodule to this repo, or a contract doc so the other repo implements against the model without editing it here.

---

## What’s in the repo

| Path | Content |
|------|---------|
| **doc/** | Intro presentations (textual + graphical notation), spec PDFs: KerML 1.0, SysML v2.0 (Parts 1–2), Systems Modeling API & Services 1.0. |
| **install/** | **eclipse** — Eclipse plugins for KerML/SysML editors. **jupyter** — SysML language kernel for JupyterLab. |
| **kerml/** | Example models in KerML. |
| **sysml/** | Example models in SysML v2 (textual). |
| **sysml.library/** | **Normative model libraries** (textual): Kernel (Base.kerml, ScalarValues.kerml), Domain Libraries (Quantities, ISQ, SI, etc.). |
| **sysml.library.xmi/** | Same libraries in Eclipse XMI (`.kermlx`, `.sysmlx`). |

Releases (zip): [github.com/Systems-Modeling/SysML-v2-Release/releases](https://github.com/Systems-Modeling/SysML-v2-Release/releases).

---

## 1. Get the content

- **Clone:**  
  `git clone https://github.com/Systems-Modeling/SysML-v2-Release.git`  
  (or `git clone --depth 1 ...` for a shallow clone.)
- **Or download a release zip** from the [releases](https://github.com/Systems-Modeling/SysML-v2-Release/releases) page and unpack it.

**In this workspace:** We use the **normative library** only. Either:

- From repo root: `git submodule update --init --recursive` (if the submodule is configured), which populates `sysml-v2-models/libs/omg/SysML-v2-Release/`.
- Or manually:  
  `mkdir -p sysml-v2-models/libs/omg && cd sysml-v2-models/libs/omg && git clone --depth 1 https://github.com/Systems-Modeling/SysML-v2-Release.git`  
  Or unpack a release zip into `sysml-v2-models/libs/omg/SysML-v2-Release/`.

See [sysml-v2-models/README.md](../../../sysml-v2-models/README.md) (“What is libs/omg/SysML-v2-Release?”).

---

## 2. Use the normative library (this repo’s visualizer)

Our projects load **Kernel** and (when needed) **Domain** libraries from the release:

- **Kernel:** `sysml.library/Kernel Libraries/Kernel Semantic Library/Base.kerml`, `Kernel Data Type Library/ScalarValues.kerml`.
- **Quantities/units (ISQ, SI):**  
  `sysml.library/Domain Libraries/Quantities and Units/` (Quantities.sysml, MeasurementReferences.sysml, ISQBase.sysml, SIPrefixes.sysml, ISQ.sysml, SI.sysml).

Project `config.yaml` files list these paths under `libs/omg/SysML-v2-Release/` first in `model_files`. Once that directory exists (submodule or manual clone), the visualizer and scripts use the standard types and units. No extra “use” step — just have the tree in place.

---

## 3. Use the specs and examples

- **Specs:** Open the PDFs in **doc/** for KerML, SysML v2, and the Systems Modeling API. Use them as the authority for syntax and semantics.
- **Examples:** Browse **sysml/** and **kerml/** for reference models and patterns. Copy or adapt patterns into your own `.sysml` under `sysml-v2-models/projects/`.
- **Naming / style:** Our conventions are in [sysml-common-lib-contribution](../../sysml-common-lib-contribution/SKILL.md) ([detailed reference](../../sysml-common-lib-contribution/references/common-library-naming-detailed.md)); the Release repo is the primary reference for **language** rules.

---

## 4. Optional: other editors (Eclipse, Jupyter)

If you want a dedicated SysML IDE or notebooks, the Release repo’s **install/** directory provides:

- **Eclipse:** Installer under `install/eclipse` for KerML and SysML v2 editors. Point the workspace library path at your clone (or `sysml.library`).
- **Jupyter:** Installer under `install/jupyter` for the SysML language kernel and JupyterLab. See the [SysML v2 Release Google Group](https://groups.google.com/g/sysml-v2-release) for e.g. `%publish` to a repository.

**Not required for the Cursor-first workflow** above.

---

## 5. Optional: API and visualization

- **Live API (OpenAPI):** [http://sysml2.intercax.com:9000/docs/](http://sysml2.intercax.com:9000/docs/) — prototype repository API; run locally via [SysML-v2-API-Services](https://github.com/Systems-Modeling/SysML-v2-API-Services) (not a submodule in this repo). See [SYSML_V2_MCP_SETUP.md](../../../docs/mcp/SYSML_V2_MCP_SETUP.md).
- **Tom Sawyer SysML 2.0 demo:** [demonstrations/sysml.2.0.demo](https://www.tomsawyer.com/demonstrations/sysml.2.0.demo) — visualization of models from the prototype repository (account required).

---

## 6. Feedback and references

- **Questions / feedback:** [SysML v2 Release Google Group](https://groups.google.com/g/sysml-v2-release) (apply for membership, then post).
- **Pilot Implementation (Eclipse/Jupyter source):** [Systems-Modeling/SysML-v2-Pilot-Implementation](https://github.com/Systems-Modeling/SysML-v2-Pilot-Implementation) — proof-of-concept Xtext-based editors and Jupyter kernel for SysML v2 textual notation and visualization.
- **Release notes:** [SysML-v2-Pilot-Implementation/releases](https://github.com/Systems-Modeling/SysML-v2-Pilot-Implementation/releases), [SysML-v2-API-Services/releases](https://github.com/Systems-Modeling/SysML-v2-API-Services/releases), [SysML-v2-API-Cookbook/releases](https://github.com/Systems-Modeling/SysML-v2-API-Cookbook/releases).

**In short:** Use **Cursor** as your main editor: edit `.sysml` here, use **SysML v2 MCP** for validation and diagrams (agents: do not default to `visualize.py`), use the Release repo for the **normative library** (under `sysml-v2-models/libs/omg/SysML-v2-Release`) and as **spec/examples reference** (doc/, sysml/, kerml/). Eclipse and Jupyter from the Release are optional. For API and MCP, see [SYSML_V2_MCP_SETUP.md](../../../docs/mcp/SYSML_V2_MCP_SETUP.md).
