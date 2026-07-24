---
title: Signal Processing Pipeline - Template Code
description: Full SysML code templates for thread state machines, port definitions, stage part defs, and top-level container (moved from SKILL.md for token efficiency).
---

# Signal Processing Pipeline - Template Code

## Full Thread State Machine

```sysml
state def ProcessingThreadLifecycle {
  doc /* State machine for processing thread */
  
  state idle;          // Not started or suspended
  state armed {        // Ready; resource initialized
    doc /* Ready to start; hardware configured */
  }
  state processing {   // Actively executing (sampling / demodulating / calculating)
    doc /* Processing samples or data; main loop active */
  }
  state paused {       // Suspended (power down or wait condition)
    doc /* Thread suspended; can resume to armed state */
  }
  state error {        // Fault condition
    doc /* Error detected; logs to telemetry; requires reset */
  }
  
  // Transitions
  transition t1 (idle -> armed) {
    trigger event /* init_request */;
  }
  transition t2 (armed -> processing) {
    trigger event /* start_signal_or_interrupt */;
  }
  transition t3 (processing -> paused) {
    trigger event /* pause_or_powerdown_request */;
  }
  transition t4 (paused -> armed) {
    trigger event /* resume_request */;
  }
  transition t5 (processing -> error) {
    trigger event /* hardware_fault or timeout */;
  }
  transition t6 (error -> armed) {
    trigger event /* error_recovery */;
  }
}
```

## Full Port Definitions

```sysml
port def RawSamplePort {
  doc /* Raw ADC sample from acquisition stage */
  out sample : Integer;  // 16-bit ADC value or similar
}

port def DemodulatedDataPort {
  doc /* Demodulated output with amplitude, phase, and DC baseline */
  out amplitude_algorithm1 : Real;   // e.g., sin/cos amplitude
  out phase_algorithm1 : Real;       // e.g., sin/cos phase
  out amplitude_algorithm2 : Real;   // e.g., digital ±0.5 amplitude
  out phase_algorithm2 : Real;       // e.g., digital ±0.5 phase
  out dc_offset : Integer;           // DC baseline (16-sample sum >> 4)
}

port def PositionDataPort {
  doc /* Calculated position output */
  out x : Real;             // X-axis position estimate
  out y : Real;             // Y-axis position estimate
  out confidence : Real;    // SNR or lock status metric
  out timestamp : Long;     // Sample timestamp for sync
}
```

## Full Acquisition Stage Part Def

```sysml
part def AcquisitionStage {
  doc /*
    Stage 1: Continuous hardware data acquisition (samples, sensor reads, etc.).
    
    Role: N parallel threads read raw data from hardware interface at specified sample rate.
    Hardware: SPI/I2C/ADC peripheral, GPIO, DMA channels.
    Execution: Interrupt-driven or DMA-based; continuous, non-blocking.
    Output: Raw data samples → processing stage.
  */
  attribute sampleRateHz : FrequencyValue = 52600 [SI::Hz];
  attribute dataBitsPerSample : Integer = 16;
  attribute parallelThreads : Integer = 4;  // e.g., Q1, Q2, Q3, Q4
  
  // One port per parallel channel
  port ch1_out : RawSamplePort;
  port ch2_out : RawSamplePort;
  port ch3_out : RawSamplePort;
  port ch4_out : RawSamplePort;
}
```

## Full Processing Stage Part Def

```sysml
part def ProcessingStage {
  doc /*
    Stage N: Transform and combine data from previous stage.
    
    Role: Apply algorithms (filtering, demodulation, etc.) to input data.
    Execution: Parallel per-sample or per-batch; synchronized via shared state (phase accumulator, etc.).
    Synchronization: Waits for all input channels before output.
    Output: Processed data → next stage or final output.
  */
  attribute processingRateHz : FrequencyValue = 3287.5 [SI::Hz];  // After decimation
  attribute algorithmCount : Integer = 3;  // e.g., sin/cos, digital, DC
  attribute decimationFactor : Integer = 16;  // Input rate / output rate
  
  // Input ports (one per channel)
  port ch1_in : RawSamplePort;
  port ch2_in : RawSamplePort;
  port ch3_in : RawSamplePort;
  port ch4_in : RawSamplePort;
  
  // Output ports
  port ch1_out : DemodulatedDataPort;
  port ch2_out : DemodulatedDataPort;
  port ch3_out : DemodulatedDataPort;
  port ch4_out : DemodulatedDataPort;
}
```

## Full Top-Level Container

```sysml
part def SignalProcessingPipeline {
  doc /*
    Top-level container orchestrating all processing stages.
    
    Stages: (1) Acquisition → (2) Processing → (3) Calculation → (4) Aggregation
    
    Data flow: Raw samples flow through each stage with typed inter-stage ports.
    Synchronization: Shared phase accumulator (if applicable) synchronizes all stages.
    Latency budget: <500 µs end-to-end from acquisition input to final output.
  */
  
  // Nested stage instances
  part acquisitionStage : AcquisitionStage;
  part processingStage : ProcessingStage;
  part calculationStage : CalculationStage;
  part aggregationStage : AggregationStage;
  
  // Top-level attributes
  attribute systemLatencyTargetUs : Integer = 500;
  attribute endToEndSampleLatency : Integer = 4;  // <5 samples latency
  
  // Top-level output port
  port finalOutput : SoftwareDataOutPort;
  
  // Inter-stage connections (explicit data flow)
  connection linkAcqToProc_Ch1 : SoftwareDataFlow {
    end port source ::> acquisitionStage.ch1_out;
    end port sink ::> processingStage.ch1_in;
  }
  // ... repeat for Ch2, Ch3, Ch4
  
  connection linkProcToCalc_Ch1 : SoftwareDataFlow {
    end port source ::> processingStage.ch1_out;
    end port sink ::> calculationStage.ch1_in;
  }
  // ... repeat for Ch2, Ch3, Ch4
  
  connection linkCalcToAgg : SoftwareDataFlow {
    end port source ::> calculationStage.output;
    end port sink ::> aggregationStage.input;
  }
  
  connection linkAggToFinal : SoftwareDataFlow {
    end port source ::> aggregationStage.output;
    end port sink ::> finalOutput;
  }
}
```

## Synchronization Point Example

```sysml
part def PositionCalculationStage {
  doc /*
    ...
    Synchronization: Single thread waits for all four demodulated inputs (Ch1, Ch2, Ch3, Ch4).
    Blocking condition: Holds until all four DemodulatedDataPort outputs are ready.
    Output: Released after geometry calculation (~50 µs after last demod input arrives).
  */
  attribute synchronizationMode : String = "wait_all_channels";
  attribute maxWaitTimeUs : Integer = 50;
}
```

## Latency Budget Template

```sysml
attribute acquisitionLatencyUs : Integer = 19;      // Per sample @ 52.6 kSa/s
attribute processingLatencyUs : Integer = 3;        // Per sample, all 3 algorithms
attribute decimationLatencyUs : Integer = 10;       // 16-sample window
attribute calculationLatencyUs : Integer = 50;      // Waits for all 4 inputs
attribute aggregationLatencyUs : Integer = 5;       // Package for output
attribute totalLatencyUs : Integer = 87;            // <500 µs target; verified ✓
```

**Verification:** Ensure `totalLatencyUs < systemLatencyTargetUs`.

## Real-World Example: QPD Lock-In (Leo CubeSat Laser Comm)

The Leo CubeSat Laser Comm project models a complete signal processing pipeline:

```
QpdAcquisitionFirmware (top-level, Nucleo H753ZI MCU)
├── SpiAcquisitionStage: 4× SPI1–4 @ 52.6 kSa/s
├── LockInDemodulationStage: phase accumulator + 3 algorithms → 3.2875 kHz
├── PositionCalculationStage: waits all 4 channels → >10 kHz output
└── DataAggregationStage: SPI6 slave response packets
```

**Thread states:** Q1–Q4 acquisition threads follow `AcquisitionThreadLifecycle` (idle → armed → sampling ↔ paused → error)  
**Ports:** `RawSamplePort`, `DemodulatedDataPort`, `PositionDataPort` enable typed data flow  
**Latency:** <500 µs end-to-end verified  
**Behavior:** Per-sample phase update, 3-algorithm parallelism, 16-sample decimation documented in interconnection report  

See model: `sysml-v2-models/projects/leo-cubesat-laser-comm/models/deploy-leo-cubesat-laser-comm.sysml` (lines 190–858)
See doc: `sysml-v2-models/projects/leo-cubesat-laser-comm/outputs/system-design-report/02b-interconnection.md`
