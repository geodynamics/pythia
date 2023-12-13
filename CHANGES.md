See <https://github.com/geodynamics/pythia/commits/master> for the complete log of changes made to Pythia/Pyre.


## Version 1.1.0

* Switch from CppUnit to Catch2 for C++ testing.

## Version 1.0.0

Merged pythia and nemesis into a single repository.

* Moved MPI C source files to nemesis directory.
* Moved journal C++ files to libsrc/pythia/journal.
* Use autotools for build.
  * Use --enable-mpi to turn on installing nemesis.

## Version 0.9.0

Updates for Python 3 compatibility. Requires Python 3.6 or later.
