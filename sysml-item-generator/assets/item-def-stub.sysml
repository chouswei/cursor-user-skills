/*
  Stub: replace PackageName, ItemName, doc, optional attributes / nested items.
  Project-local item — often in deploy-<project>.sysml or behaviour-<project>.sysml.
*/
package PackageName {
  private import ScalarValues::*;
  // For physical quantities: private import ISQ::*; private import SI::*;

  item def ItemName {
    doc /* What flows, from where to where, protocol or unit notes. */
  }

  // Example: quantity attribute (uncomment if physical)
  // item def ItemWithNominalVoltage {
  //   doc /* DC rail. */
  //   attribute nominalVoltage : ElectricPotentialDifferenceValue = 3.3 [SI::V];
  // }

  // Example: composite item
  // item def CompositeItem {
  //   doc /* Bundle of sub-flows. */
  //   item partA : ItemName;
  //   item partB : ItemName;
  // }
}
