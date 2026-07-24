---
title: Nested Structure Modeling - Reference Examples
description: Full SysML code and decomposition examples for nested structure refactoring (moved from SKILL.md for token efficiency).
---

# Nested Structure Modeling - Reference Examples

## Full Stage Part Definition Template

```sysml
part def Stage2Processing {
  doc /*
    Stage 2: Process data from Stage 1, prepare for Stage 3.
    
    Role: Apply algorithms A, B, C to transform input.
    Execution: [Interrupt-driven / DMA-based / threaded / polled]
    Synchronization: [Waits for all inputs / Per-sample / Per-batch]
    Latency: <X µs per input
  */
  
  attribute processingRateHz : FrequencyValue = 3287.5 [SI::Hz];
  attribute algorithmCount : Integer = 3;
  
  port input1_in : PortType;        // from Stage 1
  port input2_in : PortType;
  
  port output1_out : OutputPortType; // to Stage 3
  port output2_out : OutputPortType;
}
```

## Full Top-Level Container Template

```sysml
part def PipelineContainer {
  doc /*
    Top-level processing pipeline orchestrating all stages.
    
    Data flow: [Describe the overall flow]
    Synchronization: [Global sync mechanism, if any]
    Latency budget: <X µs end-to-end
    
    Stages:
    (1) Stage1 — Role
    (2) Stage2 — Role
    (3) Stage3 — Role
  */
  
  // Nested instances
  part stage1 : Stage1Processing;
  part stage2 : Stage2Processing;
  part stage3 : Stage3Processing;
  
  // Pipeline attributes
  attribute systemLatencyTargetUs : Integer = 500;
  
  // Top-level output port
  port systemOutput : TopLevelOutputPort;
  
  // Inter-stage connections
  connection link12 : DataFlow {
    end port source ::> stage1.output;
    end port sink ::> stage2.input;
  }
  connection link23 : DataFlow {
    end port source ::> stage2.output;
    end port sink ::> stage3.input;
  }
  connection link3Out : DataFlow {
    end port source ::> stage3.output;
    end port sink ::> systemOutput;
  }
}
```

## Refactoring Example: Before and After

### Before Decomposition (Monolithic)

```sysml
part def QpdAcquisitionFirmware {
  doc /*
    Firmware running on acquisition MCU (Nucleo H753ZI):
    
    Stage 1: Continuous SPI acquisition from FourChannelPdModule @ 52.6 kSa/s
    Stage 2: Lock-in demodulation with phase accumulator and 3 algorithms
    Stage 3: Position calculation from all 4 demodulated channels
    Stage 4: Data aggregation for inter-HAT SPI6 response
    
    ... 60+ lines of detailed processing description ...
  */
  
  // All attributes mixed together
  attribute sampleRateHz : FrequencyValue = 52600 [SI::Hz];
  attribute qpdModulationFrequencyHz : FrequencyValue = 3287.5 [SI::Hz];
  attribute positionUpdateRateHz : FrequencyValue = 10000 [SI::Hz];
  attribute lockInFilterCutoffHz : FrequencyValue = 1000 [SI::Hz];
  attribute adcSampleBitsPerChannel : Integer = 16;
  attribute demodulationAlgorithmCount : Integer = 3;
  attribute phaseAccumulatorDeltaPhiRadians : Real = 0.3927;
  attribute cpuCyclesPerSample : Integer = 15;
  attribute totalAcquisitionLatencyUs : Integer = 500;
  attribute decimationFactor : Integer = 16;
  attribute positionConfidenceMetric : String = "SNR";
  attribute hostUartBaud : Integer = 921600;
}
```

### After Decomposition (Modular)

**Step 1: Create nested part defs for each stage**

```sysml
part def SpiAcquisitionStage {
  doc /*
    Stage 1: Continuous hardware data acquisition.
    Role: N parallel threads read raw data from hardware interface @ specified sample rate.
    Hardware: SPI1–4 peripheral, GPIO, DMA channels.
    Execution: Interrupt-driven or DMA-based; continuous, non-blocking.
    Output: Raw data samples → demodulation stage.
  */
  attribute sampleRateHz : FrequencyValue = 52600 [SI::Hz];
  attribute adcSampleBitsPerChannel : Integer = 16;
  attribute parallelThreads : Integer = 4;
  
  port q1_out : RawSamplePort;
  port q2_out : RawSamplePort;
  port q3_out : RawSamplePort;
  port q4_out : RawSamplePort;
}

part def LockInDemodulationStage {
  doc /*
    Stage 2: Lock-in demodulation with phase accumulator.
    Role: Apply 3 demodulation algorithms (sin/cos, digital ±0.5, DC offset) per sample.
    Execution: Parallel per-sample; synchronized via phase accumulator.
    Output: Demodulated amplitude, phase, DC offset → position calculation stage.
  */
  attribute qpdModulationFrequencyHz : FrequencyValue = 3287.5 [SI::Hz];
  attribute lockInFilterCutoffHz : FrequencyValue = 1000 [SI::Hz];
  attribute demodulationAlgorithmCount : Integer = 3;
  attribute phaseAccumulatorDeltaPhiRadians : Real = 0.3927;
  attribute decimationFactor : Integer = 16;
  
  port q1_in : RawSamplePort;
  port q2_in : RawSamplePort;
  port q3_in : RawSamplePort;
  port q4_in : RawSamplePort;
  
  port q1_out : DemodulatedDataPort;
  port q2_out : DemodulatedDataPort;
  port q3_out : DemodulatedDataPort;
  port q4_out : DemodulatedDataPort;
}

part def PositionCalculationStage {
  doc /*
    Stage 3: Calculate position from all 4 demodulated channels.
    Role: Wait for all 4 demodulated inputs, compute x-y position and confidence.
    Execution: Single thread, waits for all 4 channels before computing.
    Synchronization: Waits for all four DemodulatedDataPort outputs.
    Output: Position, confidence, timestamp → aggregation stage.
  */
  attribute positionUpdateRateHz : FrequencyValue = 10000 [SI::Hz];
  attribute positionConfidenceMetric : String = "SNR";
  
  port q1_in : DemodulatedDataPort;
  port q2_in : DemodulatedDataPort;
  port q3_in : DemodulatedDataPort;
  port q4_in : DemodulatedDataPort;
  
  port position_out : PositionDataPort;
}

part def DataAggregationStage {
  doc /*
    Stage 4: Aggregate position and demodulated data for inter-HAT response.
    Role: Package processed data into SPI6 slave response packets.
    Execution: On-demand from PolarFire master; <100 µs latency.
    Output: SPI6 response packet → inter-HAT.
  */
  
  port position_in : PositionDataPort;
  port q1_demod_in : DemodulatedDataPort;
  port q2_demod_in : DemodulatedDataPort;
  port q3_demod_in : DemodulatedDataPort;
  port q4_demod_in : DemodulatedDataPort;
  
  port spi6_response_out : SoftwareDataOutPort;
}
```

**Step 2: Create top-level container with nested instances**

```sysml
part def QpdAcquisitionFirmware {
  doc /*
    Top-level QPD signal processing pipeline (Nucleo H753ZI MCU).
    
    Data flow: Raw samples → demodulation (3 algorithms) → position calc (waits all 4) → aggregation → response
    Synchronization: Phase accumulator synchronizes all demodulation threads; position calc waits all 4 channels.
    Latency budget: <500 µs end-to-end verified.
    
    Stages:
    (1) SpiAcquisitionStage — Parallel SPI acquisition @ 52.6 kSa/s
    (2) LockInDemodulationStage — Phase accumulator + 3 algorithms → 3.2875 kHz
    (3) PositionCalculationStage — Waits all 4 channels → >10 kHz output
    (4) DataAggregationStage — SPI6 slave response packets
  */
  
  // Container-level attributes only
  attribute hostUartBaud : Integer = 921600;
  attribute cpuCyclesPerSample : Integer = 15;
  attribute totalAcquisitionLatencyUs : Integer = 500;
  
  // Nested stage instances
  part acqStage : SpiAcquisitionStage;
  part demodStage : LockInDemodulationStage;
  part posCalcStage : PositionCalculationStage;
  part aggStage : DataAggregationStage;
  
  // Top-level output port
  port positionSignalOut : SoftwareDataOutPort;  // to UART5 / inter-HAT
  
  // Inter-stage connections
  connection linkAcqToDemod_Q1 : SoftwareDataFlow {
    end port source ::> acqStage.q1_out;
    end port sink ::> demodStage.q1_in;
  }
  connection linkAcqToDemod_Q2 : SoftwareDataFlow {
    end port source ::> acqStage.q2_out;
    end port sink ::> demodStage.q2_in;
  }
  connection linkAcqToDemod_Q3 : SoftwareDataFlow {
    end port source ::> acqStage.q3_out;
    end port sink ::> demodStage.q3_in;
  }
  connection linkAcqToDemod_Q4 : SoftwareDataFlow {
    end port source ::> acqStage.q4_out;
    end port sink ::> demodStage.q4_in;
  }
  
  connection linkDemodToPosCal_Q1 : SoftwareDataFlow {
    end port source ::> demodStage.q1_out;
    end port sink ::> posCalcStage.q1_in;
  }
  connection linkDemodToPosCal_Q2 : SoftwareDataFlow {
    end port source ::> demodStage.q2_out;
    end port sink ::> posCalcStage.q2_in;
  }
  connection linkDemodToPosCal_Q3 : SoftwareDataFlow {
    end port source ::> demodStage.q3_out;
    end port sink ::> posCalcStage.q3_in;
  }
  connection linkDemodToPosCal_Q4 : SoftwareDataFlow {
    end port source ::> demodStage.q4_out;
    end port sink ::> posCalcStage.q4_in;
  }
  
  connection linkPosCalToAgg : SoftwareDataFlow {
    end port source ::> posCalcStage.position_out;
    end port sink ::> aggStage.position_in;
  }
  
  connection linkDemodToAgg_Q1 : SoftwareDataFlow {
    end port source ::> demodStage.q1_out;
    end port sink ::> aggStage.q1_demod_in;
  }
  connection linkDemodToAgg_Q2 : SoftwareDataFlow {
    end port source ::> demodStage.q2_out;
    end port sink ::> aggStage.q2_demod_in;
  }
  connection linkDemodToAgg_Q3 : SoftwareDataFlow {
    end port source ::> demodStage.q3_out;
    end port sink ::> aggStage.q3_demod_in;
  }
  connection linkDemodToAgg_Q4 : SoftwareDataFlow {
    end port source ::> demodStage.q4_out;
    end port sink ::> aggStage.q4_demod_in;
  }
  
  connection linkAggToOutput : SoftwareDataFlow {
    end port source ::> aggStage.spi6_response_out;
    end port sink ::> positionSignalOut;
  }
}
```

## Traceability Verification

After decomposition, test these queries in SysML MCP:

```
// Query 1: Who produces DemodulatedDataPort?
getDefinition(name="DemodulatedDataPort")
→ Returns: port def in LockInDemodulationStage

// Query 2: Who consumes DemodulatedDataPort?
getReferences(name="DemodulatedDataPort")
→ Returns: PositionCalculationStage, DataAggregationStage

// Query 3: What is the full part hierarchy?
getHierarchy(name="QpdAcquisitionFirmware")
→ Returns: QpdAcquisitionFirmware { acqStage, demodStage, posCalcStage, aggStage }

// Query 4: What connects to PositionCalculationStage?
getReferences(name="PositionCalculationStage")
→ Returns: connections and aggregation stage references
```

## Real-World Project

See full implementation in Leo CubeSat Laser Comm project:
- Model: `sysml-v2-models/projects/leo-cubesat-laser-comm/models/deploy-leo-cubesat-laser-comm.sysml`
- Documentation: `sysml-v2-models/projects/leo-cubesat-laser-comm/outputs/system-design-report/02b-interconnection.md`
