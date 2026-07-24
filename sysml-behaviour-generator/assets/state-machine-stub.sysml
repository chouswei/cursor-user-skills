/*
  Stub: replace PackageName, StateMachineName, events, states, transitions.
  File: behaviour-<project>.sysml — load after deploy-<project>.sysml, before root-<project>.sysml.
*/
package PackageNameBehaviour {
  private import ScalarValues::*;
  // private import YourProject::*;
  // private import YourProjectRequirements::*;

  attribute def ExampleEvent {
    doc /* User or system raises this; replace with real events. */
  }

  state def StateMachineName {
    doc /*
      Replace with purpose, actors, and relationship to deploy parts.
    */
    entry;
    then idle;

    state idle {
      doc /* Initial / quiescent. */
    }
    transition idle_to_active
      first idle
      accept ExampleEvent
      then active;

    state active {
      doc /* Active phase. */
    }
    transition active_to_idle
      first active
      accept ExampleEvent
      then idle;
  }
}
