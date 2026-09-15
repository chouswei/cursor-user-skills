/*
  Stub: replace package, stakeholder, and use-case names.
  Prefer project deploy-*.sysml or a dedicated context-*.sysml.
  If the validator rejects use case def, keep part def + requirement def.
*/
package PackageNameContext {
  private import ScalarValues::String;

  part def StakeholderName {
    doc /* Concern: what this actor needs from the system. */
  }

  part def UseCaseName {
    doc /*
      Actor: StakeholderName
      Pre: ...
      Main success: ...
      Post: ...
    */
  }

  // Optional: requirement def for a normative goal -- prefer sysml-requirements-generator.
}
