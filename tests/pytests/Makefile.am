include $(top_srcdir)/check.am

TESTS = test_pythia.py
if ENABLE_MPI
TESTS += test_mpi.py
endif

dist_check_SCRIPTS = test_pythia.py test_mpi.py

noinst_PYTHON = \
	__init__.py \
	journal/__init__.py \
	journal/test_channels.py \
	journal/test_devices.py \
	journal/test_facilities.py \
	mpi/__init__.py \
	mpi/MPIApp.py \
	mpi/MPICommApp.py \
	mpi/test_application.py \
	mpi/test_communicator.py \
	mpi/test_launcher.py \
	pyre/__init__.py \
	pyre/PyreApp.py \
	pyre/test_inventory.py \
	pyre/test_schedulers.py \
	pyre/test_units.py \
	pyre/test_nemesis.py


dist_noinst_DATA = \
	pyre/pyreapp_settings.pcs \
	pyre/pyreapp_settings.pml \
	pyre/pyreapp_settings.cfg \
	pyre/data.in \
	pyre/input.txt \
	pyre/__init__.py \
	pyre/TestComponents.py \
	pyre/simpletoo-facility.odb \
	pyre/complex-facility.py


# 'export' the input files by performing a mock install
export_datadir = $(top_builddir)/tests/pytests/pyre/
export-data: $(noinst_DATA)
	if [ "X$(top_srcdir)" != "X$(top_builddir)" ]; then $(install_sh) -d $(export_datadir); for f in $(dist_noinst_DATA); do $(install_sh_DATA) $(srcdir)/$$f $(export_datadir); done; fi

clean-data:
	if [ "X$(top_srcdir)" != "X$(top_builddir)" ]; then for f in $(dist_noinst_DATA); do $(RM) $(RM_FLAGS) $(export_datadir)/$$f; done; fi

BUILT_SOURCES = export-data
clean-local: clean-data


# End of file
