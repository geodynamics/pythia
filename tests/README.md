# Pyre testing

## Functionality covered by tests

* journal
* pyre
  - applications
  - components
  - inventory
  - launchers
  - odb
  - parsing
  - schedulers
  - units
* mpi

## Functionality not covered by tests

* ACIS solid modeling `acis`
* GUI `blade`
* CIG (unused? code added by Leif Strand) `cig`
* Simulation coupling `elc`
* Web/CGI application `opal`
* Simple source functions in example simulations `pulse`
* Rigid body in example simulations `rigid`

### Pyre functionality not covered in tests

### Would like to include in tests if functionality better understood

* db (object relational manager)
* services (servers that provide a service, e.g., authentication daemon)
* idd (globally unique identifiers)
* ipa (managing user sessions)
* ipc (passing messages with sockets via UDP and TCP)
* weaver (generate code templates)
* scripts (start mpi jobs)

### Not relevant to current use

* geometry
* handbook (periodic table, constants)
* simulations
