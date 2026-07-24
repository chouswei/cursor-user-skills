/*
  TEMPLATE: Software part def. Insert into project deploy/behaviour package.
  Replace: {{PartName}}, doc text, ports (typed by existing port defs), optional attributes.
  For composites: add part members and connection defs.
*/

// === Simple part (thread, state machine, service) ===
part def {{PartName}} {
  doc /* {{PartDoc}} */
  attribute {{attributeName}} : {{AttributeType}} = {{value}};   // optional
  port {{portName}} : {{PortType}};
  port {{portName2}} : {{PortType2}};   // add more as needed
}

// === Composite part (nested parts + connections) ===
// part def {{CompositeName}} {
//   doc /* {{CompositeDoc}} */
//   part {{member1}} : {{PartType1}};
//   part {{member2}} : {{PartType2}};
//   connection linkX : {{ConnectionType}} {
//     end port source ::> {{member1}}.{{port}};
//     end port sink ::> {{member2}}.{{port}};
//   }
// }
