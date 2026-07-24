/*
  TEMPLATE: Physical connector port defs. Insert into HardwarePorts package.
  Replace placeholders: ConnectorName, Protocol names, pin assignments, doc text.
  Structure: connector { protocol1 { pin# }, protocol2 { pin# }, ... }
  Each protocol: port def ConnectorNameProtocolName : BasePortType { doc; port pinN : PinType [redefines x]; }
  Connector: port def ConnectorNamePort { doc; port protocolName : ProtocolDef; ... }
*/

// === Protocol port defs (one per protocol group) ===
// For I2C/UART: extend I2cTwoPinPort/UartTwoPinPort, use redefines on sda/scl or tx/rx
// For SPI: extend SpiPort, add pin ports
// For power/ground: use PowerOut3V3Port, PowerOut5VPort, GndPort

port def {{ConnectorName}}Protocol1 : {{BaseType1}} {
  doc /* {{Protocol1Doc}} */
  port pin{{N1}} : {{PinType1}} redefines {{Role1}};
  port pin{{N2}} : {{PinType2}} redefines {{Role2}};
}

port def {{ConnectorName}}Protocol2 : {{BaseType2}} {
  doc /* {{Protocol2Doc}} */
  port pin{{M1}} : {{PinTypeM1}};
  port pin{{M2}} : {{PinTypeM2}};
  // add more pins as needed
}

// === Connector (nests all protocols) ===
port def {{ConnectorName}}Port {
  doc /* {{ConnectorDoc}} */
  port {{protocol1Name}} : {{ConnectorName}}Protocol1;
  port {{protocol2Name}} : {{ConnectorName}}Protocol2;
  // add more protocols as needed
}
