---
name: sysml-nested-structure-modeling
description: Decompose monolithic parts into hierarchical nested structures. Model coarse-grained architecture (container) with fine-grained stages (nested parts), inter-part ports, and explicit data flows.
triggers:
  - decompose monolithic part
  - firmware architecture nested
  - hierarchical structure modeling
  - multi-stage processing decomposition
  - nested part composition
  - nested parts
  - monolithic to modular
metadata:
  pattern: pipeline
  version: 1.0
  domain: sysml
  keywords:
    - SysML v2
    - firmware architecture
    - hierarchical design
    - refactoring
related_skills:
  - sysml-modeling-workflow
  - sysml-memnet-cache
  - sysml-signal-processing-pipeline
  - sysml-connections
duration_minutes: 20
token_guardrails:
  max_context_for_references: 8000
---

system_instruction: |
  Prefer plain Markdown tables or domain wire; do not use TOON/TRON. JSON only at tool boundaries.


# SysML Nested Structure Modeling

## When to Use This Skill

Use this skill when:

- **Monolithic part too large** — Part def has >200 lines of doc, many attributes, unclear responsibilities
- **Multiple processing stages** — Acquisition → Processing → Output is natural decomposition
- **Parallel subsystems** — E.g., 4 QPD channels, each with own acquisition + demod pipeline
- **Explicit data flow matters** — You need to trace "data flows from Stage A to Stage B"
- **Reusability** — Each nested stage could be reused elsewhere (e.g., Stage1Def in another project)

**Real-world example:** Decomposing QpdAcquisitionFirmware from 60+ lines of monolithic doc into 4 nested stages with explicit inter-stage ports and connections.

## Quick Pattern

```
ContainerPart (top-level)
├── part stage1 : Stage1Def;
├── part stage2 : Stage2Def;
├── part stage3 : Stage3Def;
└── // connections between stages
    connection link12 : DataFlow { end port source ::> stage1.output; end port sink ::> stage2.input; }
```

## Step 1: Identify Logical Boundaries

Read the monolithic part's doc and attributes. Mark natural stage boundaries.

**Example from QpdAcquisitionFirmware:**

```
Stage 1: SPI Acquisition (52.6 kSa/s)
  Attributes: sampleRateHz, adcBitsPerSample, parallelThreads
  Input: FourChannelPdModule ADC board → Output: Raw 16-bit ADC samples

Stage 2: Lock-In Demodulation (52.6 kSa/s core → 3.2875 kHz)
  Attributes: referenceFrequencyHz, decimationFactor, algorithmCount
  Input: Raw samples → Output: Amplitude, phase, DC offset per channel

Stage 3: Position Calculation (>10 kHz output)
  Attributes: positionUpdateRateHz, confidenceMetric
  Input: Demodulated data (all 4 channels) → Output: x-y position, confidence

Stage 4: Data Aggregation
  Attributes: responseLatencyTargetUs
  Input: Position + demodulated data → Output: Response packet
```

## Step 2: Create Typed Port Definitions

Define ports that **only** carry data needed between stages (avoid generic `SoftwareDataPort` for cross-stage flow).

**Template:**
```sysml
port def StageXToYPort {
  doc /* Data flowing from Stage X to Stage Y */
  out result1 : Type1;
  out result2 : Type2;
}
```

**Naming rule:** `StageName + OutputPort` (e.g., `AcquisitionOutputPort`, `DemodulatedDataPort`).

## Step 3: Define Nested Part Defs

For **each** stage, create a part def with:
- **doc**: clear role, hardware resources, execution model (sync/async, rates, latency)
- **attributes**: stage-specific parameters (rates, decimation, filter cutoffs, etc.)
- **ports**: input/output using typed port defs from Step 2

**Template:**
```sysml
part def Stage2Processing {
  doc /*
    Stage 2: Process data from Stage 1, prepare for Stage 3.
    Role: Apply algorithms A, B, C to transform input.
    Execution: [Interrupt-driven / DMA-based / threaded]
    Synchronization: [Waits for all inputs / Per-sample / Per-batch]
    Latency: <X µs per input
  */
  attribute processingRateHz : FrequencyValue = 3287.5 [SI::Hz];
  attribute algorithmCount : Integer = 3;
  
  port input1_in : PortType;        // from Stage 1
  port output1_out : OutputPortType; // to Stage 3
}
```

**Rationale:** Each stage as formal part enables modular analysis and resource tracing.

## Step 4: Create Top-Level Container

Create a container part that nests all stages and documents the full pipeline.

**Template:**
```sysml
part def PipelineContainer {
  doc /*
    Top-level processing pipeline orchestrating all stages.
    Data flow: [Describe the overall flow]
    Synchronization: [Global sync mechanism, if any]
    Latency budget: <X µs end-to-end
    Stages: (1) Stage1 — Role; (2) Stage2 — Role; (3) Stage3 — Role
  */
  part stage1 : Stage1Processing;
  part stage2 : Stage2Processing;
  part stage3 : Stage3Processing;
  
  attribute systemLatencyTargetUs : Integer = 500;
  port systemOutput : TopLevelOutputPort;
  
  connection link12 : DataFlow {
    end port source ::> stage1.output;
    end port sink ::> stage2.input;
  }
  // ... repeat for other connections
}
```

**Rationale:** Explicit nesting + connections enable end-to-end traceability and latency verification.

## Step 5: Refactor Monolithic Attributes

Move stage-specific attributes from container to respective nested part defs.

**Before:**
```sysml
part def QpdAcquisitionFirmware {
  attribute sampleRateHz : FrequencyValue = 52600 [SI::Hz];
  attribute qpdModulationFrequencyHz : FrequencyValue = 3287.5 [SI::Hz];
  attribute positionUpdateRateHz : FrequencyValue = 10000 [SI::Hz];
  // ... many more attributes
}
```

**After:**
```sysml
part def SpiAcquisitionStage {
  attribute sampleRateHz : FrequencyValue = 52600 [SI::Hz];
}
part def LockInDemodulationStage {
  attribute referenceFrequencyHz : FrequencyValue = 3287.5 [SI::Hz];
}
part def PositionCalculationStage {
  attribute positionUpdateRateHz : FrequencyValue = 10000 [SI::Hz];
}
part def QpdAcquisitionFirmware {
  // Container-level only
  attribute hostUartBaud : Integer = 921600;
  attribute totalAcquisitionLatencyUs : Integer = 500;
  // ... nested stages
}
```

**Rationale:** Clearer separation of concerns; easier to reason about stage-specific vs. system-level parameters.

## Step 6: Enable Traceability Queries

Verify the nested structure supports answering key questions:

- "Who consumes demodulated data?" → Connections show: position calc + aggregation
- "What's the latency from raw sample to position output?" → Sum of per-stage latencies
- "Which stage uses SPI1?" → Acquisition stage attributes + hardware allocation
- "What happens if demod fails?" → Check error paths in thread state machine

**Test in SysML MCP:**
```
getReferences(name="DemodulatedDataPort")
// Should return: posCalcStage, aggStage (consumers)

getDefinition(name="LockInDemodulationStage")
// Should return: full part def with all attributes and ports
```

## Step 7: Validate Structure

Run SysML MCP validate:
- [ ] All nested part defs resolve
- [ ] All inter-stage connections have matching port types
- [ ] No circular dependencies
- [ ] All attributes have valid types and default values

## Validation Checklist

- [ ] Identified 3–6 logical stages from monolithic part's documentation
- [ ] Created typed port defs for inter-stage communication (not generic `SoftwareDataPort`)
- [ ] Created nested part def for each stage with role, attributes, input/output ports
- [ ] Created top-level container part that nests all stages
- [ ] Moved stage-specific attributes from container to respective nested parts
- [ ] Added explicit inter-stage connections with `SoftwareDataFlow` or equivalent
- [ ] Documented synchronization and latency budget at container level
- [ ] SysML MCP validation: 0 errors
- [ ] Tested traceability queries (getReferences, getDefinition) in MCP
- [ ] Updated interconnection doc to reference nested structure

## Example: QpdAcquisitionFirmware Decomposition

**Before:** Monolithic part with 60+ lines of doc covering 4 stages simultaneously.

**After:**
```
QpdAcquisitionFirmware (container)
├── SpiAcquisitionStage (input: FourChannelPdModule; output: RawSamplePort ×4)
├── LockInDemodulationStage (input: RawSamplePort ×4; output: DemodulatedDataPort ×4)
├── PositionCalculationStage (input: DemodulatedDataPort ×4; output: PositionDataPort)
└── DataAggregationStage (input: PositionDataPort + DemodulatedDataPort ×4; output: SPI6 packet)
```

Each stage is now **discoverable, reusable, and traceable**.

## References

See **references/nested-structure-examples.md** for:
- Full stage part def templates with all attributes
- Complete top-level container with nested instances and inter-stage connections
- Before/after refactoring example (60+ line monolithic → 4 nested stages)
- Traceability verification queries (getReferences, getDefinition in SysML MCP)
- Real-world QpdAcquisitionFirmware decomposition from Leo CubeSat Laser Comm project

**Next:** Use **[sysml-signal-processing-pipeline](../sysml-signal-processing-pipeline/SKILL.md)** for thread states and latency verification, or **[sysml-connections](../sysml-connections/SKILL.md)** to verify inter-stage data flows.
