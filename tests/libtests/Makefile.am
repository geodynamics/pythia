include $(top_srcdir)/check.am

TESTS = testpythia

check_PROGRAMS = testpythia

testpythia_SOURCES = \
	TestDriver.cc \
	journal/TestDiagnostics.cc \
	test_driver.cc

AM_CPPFLAGS += -I$(PYTHON_INCDIR)

testpythia_LDADD = \
	-lcppunit -ldl \
	$(PYTHON_BLDLIBRARY) $(PYTHON_LIBS) $(PYTHON_SYSLIBS)


# End of file
