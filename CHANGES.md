See <https://github.com/geodynamics/pythia/commits/master> for the complete log of changes made to Pythia/Pyre.

## Version 1.3.1 (2026-10-23)

* Fixed incompatibilities with Python 3.13 and later in nemesis.
* Replaced deprecated `pkg_resources` usage with `importlib.metadata`, `importlib.resources`, and `packaging` for compatibility with setuptools 81+ (where `pkg_resources` is removed).
* Updated Python requirement to version 3.10 or later.

## Version 1.3.0 (2026-08-17)

* Added pygments lexer `pyrejournal' for syntax highlighting of journal output.
* Added configure option for pip install without build isolation (`--without-build-isolation`).

## Version 1.2.0 (2026-05-30)

* Added `_flow` journal channel to Component for application flow.
* Fixed installation of color-console .cfg files.

## Version 1.1.0 (2023-12-15)

* Switch from CppUnit to Catch2 for C++ testing.
* Update Python requirement to version 3.8 or later.

## Version 1.0.0 (2022-06-06)

Merged pythia and nemesis into a single repository.

* Moved MPI C source files to nemesis directory.
* Moved journal C++ files to libsrc/pythia/journal.
* Use autotools for build.
  * Use --enable-mpi to turn on installing nemesis.

## Version 0.9.0

Updates for Python 3 compatibility. Requires Python 3.6 or later.
