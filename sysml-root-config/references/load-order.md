# config.yaml `model_files` — typical chain

1. **OMG Kernel:** `Base.kerml`, `ScalarValues.kerml`
2. **Domain quantities:** `Quantities.sysml`, `MeasurementReferences.sysml`, `ISQBase.sysml`, `SIPrefixes.sysml`, `ISQ.sysml`, `SI.sysml` (paths as in existing projects under `libs/omg/...`)
3. **Common `libs/common/parts/`:** `flow_items.sysml` → `hardware_ports.sysml` → … (see [libs/common/README.md](../../../../sysml-v2-models/libs/common/README.md))
4. **connections.sysml**, then composites if used
5. **requirements-&lt;project&gt;.sysml**
6. **deploy-&lt;project&gt;.sysml**
7. **behaviour-&lt;project&gt;.sysml** (if present)
8. **root-&lt;project&gt;.sysml** — **always last**

Project-specific **`connections-*.sysml`** loads before **deploy** when deploy uses those defs.

Adjust paths relative to **`model_dir`** (usually `models`).
