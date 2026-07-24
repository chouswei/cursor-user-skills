/*
  TEMPLATE: Hardware part def. Insert into common lib or project package.
  Replace: {{PartName}}, doc text, ports (HardwarePorts types), attributes.
  For OTS: productCategory, partNumber. For custom/IMD: partNumber = ClickUp task ID.
  Use qualified HardwarePorts:: for port types when needed.
*/

// === Simple hardware part (board, module) ===
part def {{PartName}} {
  doc /* {{PartDoc}} */
  attribute productCategory : String;
  attribute estimatedCostUsd : Real;   // optional BOM line; omit initial value if unknown
  attribute partNumber : String;
  attribute {{optionalAttribute}} : {{Type}};   // e.g. currentDraw5VTypical : ElectricCurrentValue
  port powerIn : HardwarePorts::PowerIn5VPort;
  port {{portName}} : HardwarePorts::{{PortType}};
  // add more ports as needed
}

// === With nested port (connector from sysml-physical-port-generator) ===
// part def {{PartName}} {
//   doc /* ... */
//   port p1 : HardwarePorts::Gpio40PinPort;   // or MikroBusPort, AcquisitionMcuHatPort
//   port powerIn : HardwarePorts::PowerIn5VPort;
//   ...
// }
