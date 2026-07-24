/*
  Template: SysML signal item and connector port definitions from EAGLE netlist.
  
  Fill in:
  1. Package name (LeoLaserComm → YourProjectName)
  2. Power items — voltage, isolation level, descriptions
  3. Signal primitives — control, data, analog signal types
  4. Connector port defs — one per external connector
  5. Connector signal maps (as item defs with attributes)
  
  Load order: After part def, before deploy.
*/
package YourProjectName {
  private import HardwarePorts::*;

  // ============================================================================
  // Power Rail Item Definitions
  // ============================================================================

  item def PowerSupply5V {
    doc /* +5V main supply. */
    attribute voltage : Real = 5.0;
    attribute unit : String = "V";
  }

  item def PowerSupply12V {
    doc /* +12V supply. */
    attribute voltage : Real = 12.0;
    attribute unit : String = "V";
  }

  item def PowerSupply3V3 {
    doc /* +3.3V local supply (derived). */
    attribute voltage : Real = 3.3;
    attribute unit : String = "V";
  }

  item def GroundSignal {
    doc /* Primary ground (DGND). */
  }

  item def GroundIsolated {
    doc /* Isolated secondary ground. */
    attribute isolationLevel : String;
  }

  // ============================================================================
  // Signal Primitive Definitions
  // ============================================================================

  item def SpiChipSelect {
    doc /* SPI chip select (!CS) — active-low. */
  }

  item def SpiClock {
    doc /* SPI clock (SCLK). */
  }

  item def SpiDataIn {
    doc /* SPI data input (MOSI). */
  }

  item def SpiDataOut {
    doc /* SPI data output (MISO). */
  }

  item def SpiChannel {
    doc /* Complete 4-signal SPI channel. */
    part cs : SpiChipSelect;
    part sclk : SpiClock;
    part sdi : SpiDataIn;
    part sdo : SpiDataOut;
  }

  item def ControlSignal {
    doc /* Control signal (reset, start, enable). */
  }

  item def AnalogSignal {
    doc /* Analog signal (ADC input, DAC output). */
  }

  // ============================================================================
  // Connector Port Definitions (Pinmap)
  // ============================================================================

  port def YourHatConnector1Port {
    doc /*
      External connector 1 (J1, X1, P1).
      Replace with actual connector label, part number, pin count.
      Example: "30-pin SPI multiplexer (5051103091 SPECIAL connector)."
    */
    // Add port for each signal group or channel
    port channel1 : HardwarePorts::SpiFourPinPort {
      port cs : HardwarePorts::GpioExpansionPort;   // Signal name (resistor ref)
      port mosi : HardwarePorts::GpioExpansionPort;
      port sclk : HardwarePorts::GpioExpansionPort;
      port miso : HardwarePorts::GpioExpansionPort;
    }
  }

  port def YourHatConnector2Port {
    doc /* External connector 2 (J5, J_Analog, etc.). */
    port analogInput : HardwarePorts::GpioExpansionPort;
    port control : HardwarePorts::GpioExpansionPort;
  }

  // ============================================================================
  // Connector Signal Map Documentation Items
  // ============================================================================

  item def ConnectorSignalMap {
    doc /*
      Connector J1 (30-pin):
      - Pins 1, 4, 7, 10, 13, 16, 19, 22, 25, 28 = GND
      - Pin 2 = CS1 (via R18)
      - Pin 3 = SDI_1 (via R17)
      - ... (complete for all pins)
      
      See EAGLE netlist .scr for full connectivity.
    */
    attribute connectorLabel : String = "J1";
    attribute connectorPartNumber : String = "5051103091";
    attribute totalPins : Integer = 30;
  }

}
