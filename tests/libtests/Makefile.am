include $(top_srcdir)/check.am

TESTS = libtest_pythia

check_PROGRAMS = libtest_pythia

libtest_pythia_SOURCES = \
	journal/TestDiagnostics.cc \
	driver_catch2.cc

AM_CPPFLAGS += -I$(PYTHON_INCDIR)
LDFLAGS += $(AM_LDFLAGS) $(PYTHON_LDFLAGS)

libtest_pythia_LDADD = \
	-lCatch2 -ldl \
	$(PYTHON_BLDLIBRARY) $(PYTHON_LIBS) $(PYTHON_SYSLIBS)


EXTRA_DIST = 

# End of file
