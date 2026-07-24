/*
  TEMPLATE: Software/logical port and connection defs. Insert into project deploy package.
  Replace: {{InterfaceName}}, {{ConnectionRole1}}, {{ConnectionRole2}}, optional item type.
  Structure: port def OutPort; port def InPort; connection def Flow { end port role : PortType; }
*/

// === Port defs (producer / consumer) ===
port def {{InterfaceName}}OutPort;
port def {{InterfaceName}}InPort;

// === Connection def ===
connection def {{InterfaceName}}Flow {
  end port {{ConnectionRole1}} : {{InterfaceName}}OutPort;
  end port {{ConnectionRole2}} : {{InterfaceName}}InPort;
}

// Optional: add item typing when conveying a logical item (project-defined)
// port def {{InterfaceName}}OutPort { out item {{itemName}} : {{ItemType}}; }
// port def {{InterfaceName}}InPort  { in item {{itemName}} : {{ItemType}}; }
