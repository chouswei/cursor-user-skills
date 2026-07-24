---
name: sysml-signal-processing-pipeline
description: Model multi-stage DSP pipelines with nested parts, inter-stage ports, thread states. Best practices for stage decomposition, synchronization, and latency verification.
triggers:
  - multi-stage processing architecture
  - thread state machine modeling
  - nested part hierarchy
  - inter-stage data flow
  - latency budget verification
  - signal processing pipeline
  - phase accumulator
  - lock-in demodulation
metadata:
  pattern: pipeline
  version: 1.0
  domain: sysml
  keywords:
    - SysML v2
    - firmware architecture
    - DSP
    - multi-stage processing
related_skills:
  - sysml-nested-structure-modeling
  - sysml-behaviour-generator
  - sysml-connections
duration_minutes: 25
token_guardrails:
  max_context_for_references: 8000
---

system_instruction: |
  Prefer plain Markdown tables or domain wire; do not use TOON/TRON. JSON only at tool boundaries.


# SysML Signal Processing Pipeline Modeling

## When to Use This Skill

Use this skill to model **multi-stage signal processing architectures** in SysML v2 where:

- **Parallel acquisition threads** read hardware (ADC, sensors, SPI interfaces)
- **Processing stages** (filtering, demodulation, decimation, calculation) transform data
- **Synchronization points** exist (e.g., position calc waits for all 4 demod channels)
- **Latency budget** matters (end-to-end timing from input to output)
- **Thread lifecycle** includes states (idle, armed, sampling, paused, error)
- **Behavior flows** document per-sample vs. per-cycle processing

**Real-world example:** QPD lock-in demodulation (Leo CubeSat Laser Comm project):
- 4 parallel SPI acquisition threads @ 52.6 kSa/s
- Phase accumulator + 3 demodulation algorithms per sample (sin/cos, digital ±0.5, DC offset)
- 16-sample decimation to 3.2875 kHz output
- Position calculation waits for all 4 channels, outputs >10 kHz

## Quick Pattern: 7 Steps

1. **Define thread state machine** (idle → armed → processing → paused → error)
2. **Create typed inter-stage ports** (RawSamplePort, ProcessedDataPort, OutputPort)
3. **Define nested part defs** (acquisition, processing, calculation, aggregation stages)
4. **Nest instances + connect** (stage1 → stage2 → stage3 data flows)
5. **Document synchronization** (e.g., "position calc waits for all 4 channels")
6. **Verify latency budget** (sum per-stage latencies <target)
7. **Add behavior flow doc** (per-sample processing activity pseudocode)

## Architecture Pattern

```
Container (top-level)
├── SpiAcquisitionStage (4× parallel Q1–Q4 threads)
│   └── Output: RawSamplePort (16-bit ADC per channel)
├── DemodulationStage (phase accumulator + 3 algorithms)
│   └── Output: DemodulatedDataPort (amplitude, phase, DC per channel)
├── PositionCalculationStage (waits all 4 channels)
│   └── Output: PositionDataPort (x, y, confidence, timestamp)
└── DataAggregationStage (package for inter-HAT response)
    └── Output: SoftwareDataOutPort (response packet)
```

## Step 1: Define Thread State Machine

Model individual processing thread lifecycle: `idle` → `armed` → `processing` → `paused`/`error` → recovery.

**State def template** (see REFERENCES for full code):
- States: idle, armed, processing, paused, error
- Transitions: init_request, start_signal, pause_request, resume_request, error_recovery
- Rationale: Formalizes thread lifecycle; enables state transition analysis

## Step 2: Define Typed Inter-Stage Ports

Create port defs for data flowing between stages (avoid generic `SoftwareDataPort` for cross-stage).

**Port template** (see REFERENCES):
- `RawSamplePort`: 16-bit ADC value (or equivalent)
- `DemodulatedDataPort`: amplitude (algorithm1/2), phase (1/2), dc_offset
- `PositionDataPort`: x, y, confidence, timestamp

**Rationale:** Typed ports enable traceability ("Who consumes demod data?") and type-safe connections.

## Step 3: Define Processing Stage Part Defs

For each stage, create a part def with:
- **doc**: role, hardware resources, execution model (sync/async, rates, latency)
- **attributes**: stage-specific parameters (rates, decimation, filter cutoffs)
- **ports**: input/output using typed port defs

**Part template** (see REFERENCES):
```sysml
part def AcquisitionStage {
  // doc: Stage role, hardware, execution model
  attribute sampleRateHz : FrequencyValue;
  attribute parallelThreads : Integer;
  port ch1_out : RawSamplePort;
  // ... ch2_out, ch3_out, ch4_out
}
```

**Rationale:** Each stage as formal part enables modular analysis and resource tracing.

## Step 4: Create Top-Level Container with Nested Stages

Nest all stages and connect with explicit data flows.

```sysml
part def Pipeline {
  part stage1 : AcquisitionStage;
  part stage2 : DemodulationStage;
  part stage3 : CalculationStage;
  
  connection link12 : SoftwareDataFlow {
    end port source ::> stage1.output;
    end port sink ::> stage2.input;
  }
  // ... repeat for other connections
}
```

**Rationale:** Explicit nesting + connections enable end-to-end traceability and latency verification.

## Step 5: Document Synchronization Points

Add stage attributes for synchronization (e.g., "wait_all_channels"), max wait time, blocking conditions.

**Example:**
```sysml
attribute synchronizationMode : String = "wait_all_channels";
attribute maxWaitTimeUs : Integer = 50;
```

**Rationale:** Explicit sync docs enable race condition and deadlock verification.

## Step 6: Verify Latency Budget

Sum per-stage latencies and verify `totalLatencyUs < systemLatencyTargetUs`.

**Template:**
```sysml
attribute acqLatencyUs : Integer = 19;      // Per sample
attribute procLatencyUs : Integer = 3;      // Per sample
attribute calcLatencyUs : Integer = 50;     // Waits all 4
attribute totalLatencyUs : Integer = 87;    // Verified <500 µs
```

## Step 7: Add Behavior Flow Documentation

Document per-sample processing activity in interconnection markdown (not in SysML).

**Pseudocode (for doc markdown):**
```
Per-sample (52.6 kSa/s):
  1. SPI ISR → read 16-bit sample
  2. Phase acc += Δφ (2π/16)
  3. sin/cos demod: I/Q mixing (parallel)
  4. Digital ±0.5 demod: quantized mixing (parallel)
  5. DC accum: rolling sum (parallel)
  6. Every 16 samples: decimation, position calc, aggregation
```

**Rationale:** Behavior flow (separate from structure) clarifies parallelism and synchronization.

## Validation Checklist

- [ ] Thread state machine defined with all transitions
- [ ] Typed ports created (not generic `SoftwareDataPort`)
- [ ] Each stage part def has role, attributes, input/output ports
- [ ] Container nests all stages with explicit connections
- [ ] Synchronization and latency documented per stage
- [ ] SysML MCP validation: 0 errors
- [ ] Traceability test: "Who consumes stage N output?" → returns consumers

## References

See **references/sysml-signal-processing-template.md** for:
- Full state machine code (all states and transitions)
- Complete port def templates (RawSamplePort, DemodulatedDataPort, PositionDataPort)
- Acquisition and processing stage part defs with attributes and ports
- Top-level container with all nested instances and inter-stage connections
- Synchronization point examples
- Latency budget template
- Real-world QPD lock-in demodulation example from Leo CubeSat Laser Comm project

**Next steps:**
1. Use **[sysml-nested-structure-modeling](../sysml-nested-structure-modeling/SKILL.md)** for detailed decomposition if starting from monolithic
2. Use **[sysml-behaviour-generator](../sysml-behaviour-generator/SKILL.md)** for activity diagrams
3. Use **[sysml-connections](../sysml-connections/SKILL.md)** to verify inter-stage data flows
